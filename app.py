import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from datadog import initialize, statsd
from pythonjsonlogger import jsonlogger
import time
from openai import OpenAI

# Initialize Datadog
initialize(
    statsd_host=os.getenv('DD_AGENT_HOST', 'localhost'),
    statsd_port=8125
)

# Initialize OpenAI client lazily to avoid blocking startup
truefoundry_client = None

def get_truefoundry_client():
    """Get or create TrueFoundry client on demand"""
    global truefoundry_client
    if truefoundry_client is None and os.getenv('TRUEFOUNDRY_API_KEY') and os.getenv('TRUEFOUNDRY_BASE_URL'):
        truefoundry_client = OpenAI(
            api_key=os.getenv('TRUEFOUNDRY_API_KEY'),
            base_url=os.getenv('TRUEFOUNDRY_BASE_URL')
        )
    return truefoundry_client

# Configure structured JSON logging
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create JSON formatter
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    
    # Create handler
    handler = logging.StreamHandler()
    handler.setFormatter(json_formatter)
    
    # Clear existing handlers and add our JSON handler
    logger.handlers.clear()
    logger.addHandler(handler)
    
    return logger

logger = setup_logging()

def analyze_subtitle_for_loud_events(subtitle_text):
    """
    Analyze subtitle text to determine if it describes a loud event.
    Returns 'YES' or 'NO' based on AI analysis (Live Mode) or rule-based logic (Mock Mode).
    """
    # Check if we have credentials to run in "Live Mode"
    client = get_truefoundry_client()
    if client and os.getenv("TRUEFOUNDRY_API_KEY"):
        # LIVE MODE - Use TrueFoundry AI Gateway
        try:
            logger.info("Running in LIVE mode", extra={
                'subtitle_text': subtitle_text,
                'ai_provider': 'truefoundry'
            })
            
            # Increment AI request counter
            statsd.increment('crest.ai.requests.total', tags=['provider:truefoundry'])
            
            ai_start_time = time.time()
            
            # Create prompt for loud event detection
            prompt = f"Does the following text describe a loud noise: '{subtitle_text}'? Respond only with YES or NO."
            
            # Call TrueFoundry AI Gateway
            response = client.chat.completions.create(
                model="openai-main/gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            ai_duration = time.time() - ai_start_time
            
            # Extract the response
            ai_decision = response.choices[0].message.content.strip().upper()
            
            # Validate response
            if ai_decision not in ['YES', 'NO']:
                logger.warning("AI returned unexpected response", extra={
                    'ai_response': ai_decision,
                    'expected': 'YES or NO'
                })
                ai_decision = 'NO'  # Default to safe option
            
            # Log AI response
            logger.info("OpenAI decision", extra={
                'decision': ai_decision,
                'ai_duration_ms': ai_duration * 1000,
                'subtitle_text': subtitle_text
            })
            
            # Record metrics
            statsd.histogram('crest.ai.duration', ai_duration, tags=['provider:truefoundry'])
            statsd.increment(f'crest.openai.decision.{ai_decision.lower()}', tags=['provider:truefoundry'])
            
            return ai_decision
            
        except Exception as e:
            logger.error("OpenAI API call failed", extra={
                'error': str(e),
                'error_type': type(e).__name__,
                'subtitle_text': subtitle_text
            })
            
            # Increment error counter
            statsd.increment('crest.openai.error', tags=[
                'provider:truefoundry',
                f'error_type:{type(e).__name__}'
            ])
            
            # Return safe default
            return 'NO'
    
    else:
        # MOCK MODE - Use rule-based logic
        logger.warning("Running in MOCK mode (no API key found)", extra={
            'subtitle_text': subtitle_text,
            'mode': 'mock'
        })
        
        # Simple rule-based detection
        text_to_check = subtitle_text.strip().lower()
        
        # Define loud event keywords
        loud_keywords = [
            '[explosion]', '[gunshot]', '[dramatic music]', '[thunder]', 
            '[crash]', '[bang]', '[boom]', '[screaming]', '[shouting]',
            'explosion', 'gunshot', 'thunder', 'crash', 'bang', 'boom'
        ]
        
        # Check if any loud keywords are present
        decision = 'NO'
        for keyword in loud_keywords:
            if keyword in text_to_check:
                decision = 'YES'
                break
        
        logger.info("Mock decision completed", extra={
            'decision': decision,
            'subtitle_text': subtitle_text,
            'mode': 'mock'
        })
        
        # Record mock metrics
        statsd.increment(f'crest.mock_decision.{decision.lower()}', tags=['mode:mock'])
        
        return decision

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set service metadata for Datadog
app.config['DD_SERVICE'] = os.getenv('DD_SERVICE', 'crest-agent')
app.config['DD_ENV'] = os.getenv('DD_ENV', 'development')
app.config['DD_VERSION'] = os.getenv('DD_VERSION', '0.1.0')

@app.route('/data', methods=['GET', 'POST'])
def data():
    start_time = time.time()
    
    # Log request
    logger.info("Processing /data request", extra={
        'method': request.method,
        'endpoint': '/data',
        'user_agent': request.headers.get('User-Agent', ''),
        'content_type': request.headers.get('Content-Type', '')
    })
    
    # Increment request counter
    statsd.increment('crest.requests.total', tags=[
        f'method:{request.method}',
        f'endpoint:/data'
    ])
    
    try:
        if request.method == 'POST':
            # Handle subtitle text processing
            data = request.get_json()
            subtitle_text = data.get('text', '') if data else ''
            
            if not subtitle_text:
                logger.warning("Empty subtitle text received")
                statsd.increment('crest.requests.empty_text')
                return jsonify({"error": "No text provided"}), 400
            
            logger.info("Received subtitle text for processing", extra={
                'subtitle_length': len(subtitle_text),
                'subtitle_preview': subtitle_text[:50] + '...' if len(subtitle_text) > 50 else subtitle_text
            })
            
            # Increment subtitle processing counter
            statsd.increment('crest.subtitle.received')
            
            # Analyze subtitle with AI
            ai_decision = analyze_subtitle_for_loud_events(subtitle_text)
            
            # Determine response based on AI decision
            if ai_decision == 'YES':
                # Loud event detected - send volume reduction command
                logger.info("Loud event detected - recommending volume reduction", extra={
                    'subtitle_text': subtitle_text,
                    'ai_decision': ai_decision
                })
                
                # Increment loud event detection metric
                statsd.increment('crest.loud_event.detected')
                
                response_data = {
                    "action": "LOWER_VOLUME",
                    "level": 0.3,
                    "duration": 5000,
                    "confidence": ai_decision,
                    "subtitle_text": subtitle_text,
                    "processed": True
                }
            else:
                # No loud event - maintain current volume
                logger.info("No loud event detected - maintaining volume", extra={
                    'subtitle_text': subtitle_text,
                    'ai_decision': ai_decision
                })
                
                response_data = {
                    "action": "NONE",
                    "confidence": ai_decision,
                    "subtitle_text": subtitle_text,
                    "processed": True
                }
            
            # Record processing time
            processing_time = time.time() - start_time
            statsd.histogram('crest.processing.duration', processing_time, tags=['endpoint:/data'])
            
            logger.info("Subtitle processing completed", extra={
                'processing_time_ms': processing_time * 1000,
                'action': response_data.get('action', 'UNKNOWN'),
                'ai_decision': ai_decision
            })
            
            return jsonify(response_data)
        else:
            # GET request - return simple hello
            response_data = {"message": "Hello"}
            
            processing_time = time.time() - start_time
            statsd.histogram('crest.processing.duration', processing_time, tags=['endpoint:/data'])
            
            return jsonify(response_data)
            
    except Exception as e:
        # Log error
        logger.error("Error processing request", extra={
            'error': str(e),
            'error_type': type(e).__name__
        })
        
        # Increment error counter
        statsd.increment('crest.errors.total', tags=[
            f'endpoint:/data',
            f'error_type:{type(e).__name__}'
        ])
        
        return jsonify({"error": "Internal server error"}), 500

@app.route('/audio-data', methods=['POST'])
def handle_audio_data():
    """Process real-time audio analysis data"""
    start_time = time.time()
    
    logger.info("Processing audio analysis request", extra={
        'method': request.method,
        'endpoint': '/audio-data'
    })
    
    statsd.increment('crest.requests.total', tags=[
        'method:POST',
        'endpoint:/audio-data'
    ])
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        volume = data.get('volume', 0)
        baseline = data.get('baseline', 0)
        spike = data.get('spike', 0)
        
        logger.info("Audio analysis data received", extra={
            'volume': volume,
            'baseline': baseline,
            'spike': spike,
            'analysis_type': 'real_time_audio'
        })
        
        # AI-enhanced audio analysis
        ai_decision = analyze_audio_for_loud_events(volume, baseline, spike)
        
        if ai_decision == 'YES':
            logger.info("Loud audio event confirmed by AI", extra={
                'volume': volume,
                'spike': spike,
                'ai_decision': ai_decision
            })
            
            statsd.increment('crest.loud_event.audio_detected')
            
            response_data = {
                "action": "LOWER_VOLUME",
                "level": 0.25,  # Lower volume more aggressively for audio spikes
                "duration": 3000,  # Longer duration for audio events
                "confidence": ai_decision,
                "trigger": "audio_analysis",
                "volume_data": {
                    "current": volume,
                    "baseline": baseline,
                    "spike": spike
                }
            }
        else:
            response_data = {
                "action": "NONE",
                "confidence": ai_decision,
                "trigger": "audio_analysis"
            }
        
        processing_time = time.time() - start_time
        statsd.histogram('crest.processing.duration', processing_time, tags=['endpoint:/audio-data'])
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error("Error processing audio data", extra={
            'error': str(e),
            'error_type': type(e).__name__
        })
        
        statsd.increment('crest.errors.total', tags=[
            'endpoint:/audio-data',
            f'error_type:{type(e).__name__}'
        ])
        
        return jsonify({"error": "Internal server error"}), 500

def analyze_audio_for_loud_events(volume, baseline, spike):
    """
    Analyze audio data to determine if it represents a loud event.
    Uses AI + heuristics for better accuracy.
    """
    # Get AI client
    client = get_truefoundry_client()
    
    if client and os.getenv("TRUEFOUNDRY_API_KEY"):
        try:
            logger.info("Running audio analysis in LIVE mode", extra={
                'volume': volume,
                'baseline': baseline,
                'spike': spike,
                'ai_provider': 'truefoundry'
            })
            
            statsd.increment('crest.ai.requests.total', tags=['provider:truefoundry', 'type:audio'])
            
            ai_start_time = time.time()
            
            # Create prompt for audio analysis
            prompt = f"""Analyze this audio data for loud events:
            Current Volume: {volume:.3f}
            Baseline Volume: {baseline:.3f} 
            Volume Spike: {spike:.3f}
            
            This represents real-time audio analysis. A spike > 0.3 usually indicates sudden loud sounds like explosions, gunshots, crashes, or dramatic music.
            
            Should the volume be lowered? Respond only with YES or NO."""
            
            response = client.chat.completions.create(
                model="openai-main/gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.1
            )
            
            ai_duration = time.time() - ai_start_time
            ai_decision = response.choices[0].message.content.strip().upper()
            
            if ai_decision not in ['YES', 'NO']:
                logger.warning("AI returned unexpected audio response", extra={
                    'ai_response': ai_decision,
                    'expected': 'YES or NO'
                })
                ai_decision = 'NO'
            
            logger.info("OpenAI audio decision", extra={
                'decision': ai_decision,
                'ai_duration_ms': ai_duration * 1000,
                'volume': volume,
                'spike': spike
            })
            
            statsd.histogram('crest.ai.duration', ai_duration, tags=['provider:truefoundry', 'type:audio'])
            statsd.increment(f'crest.openai.audio_decision.{ai_decision.lower()}', tags=['provider:truefoundry'])
            
            return ai_decision
            
        except Exception as e:
            logger.error("OpenAI audio analysis failed", extra={
                'error': str(e),
                'error_type': type(e).__name__,
                'volume': volume,
                'spike': spike
            })
            
            statsd.increment('crest.openai.error', tags=[
                'provider:truefoundry',
                'type:audio',
                f'error_type:{type(e).__name__}'
            ])
    
    # Fallback to heuristic analysis
    logger.info("Using heuristic audio analysis", extra={
        'volume': volume,
        'baseline': baseline,
        'spike': spike,
        'mode': 'heuristic'
    })
    
    # Heuristic rules for loud events
    if spike > 0.4:  # Very large spike
        decision = 'YES'
    elif spike > 0.25 and volume > 0.6:  # Medium spike with high volume
        decision = 'YES'
    else:
        decision = 'NO'
    
    logger.info("Heuristic audio decision", extra={
        'decision': decision,
        'volume': volume,
        'spike': spike,
        'mode': 'heuristic'
    })
    
    statsd.increment(f'crest.heuristic_audio_decision.{decision.lower()}', tags=['mode:heuristic'])
    
    return decision

@app.route('/feedback', methods=['POST'])
def handle_feedback():
    """Receives user feedback and logs it as a custom metric."""
    logger.info("User correction event received", extra={
        'event_type': 'user_correction',
        'feedback_source': 'chrome_extension'
    })
    
    # This metric is the key for the "creative eval" judging criterion
    statsd.increment('crest.user_correction.count', tags=[
        'source:chrome_extension',
        'event:volume_correction'
    ])
    
    # Also log as a general feedback metric
    statsd.increment('crest.feedback.received', tags=[
        'type:user_correction'
    ])
    
    return jsonify({"status": "ok"})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for monitoring"""
    logger.info("Health check requested")
    statsd.increment('crest.health.checks')
    
    return jsonify({
        "status": "healthy",
        "service": app.config['DD_SERVICE'],
        "version": app.config['DD_VERSION'],
        "environment": app.config['DD_ENV']
    })

if __name__ == '__main__':
    logger.info("Starting Crest Flask server", extra={
        'service': app.config['DD_SERVICE'],
        'version': app.config['DD_VERSION'],
        'environment': app.config['DD_ENV'],
        'port': 5003
    })
    
    app.run(debug=True, host='0.0.0.0', port=5003)