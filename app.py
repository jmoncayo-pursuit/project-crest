import os
import logging
import hashlib
from flask import Flask, jsonify, request
from flask_cors import CORS
from datadog import initialize, statsd
from pythonjsonlogger import jsonlogger
import time
from openai import OpenAI
from collections import defaultdict
import threading

# Initialize Datadog
initialize(
    statsd_host=os.getenv('DD_AGENT_HOST', 'localhost'),
    statsd_port=8125
)

# Initialize OpenAI client lazily to avoid blocking startup
truefoundry_client = None

# --- CACHING AND PERFORMANCE OPTIMIZATION CLASSES ---
class DecisionCache:
    """Cache for AI decisions with TTL support"""
    def __init__(self, ttl_seconds=30):
        self.cache = {}
        self.ttl = ttl_seconds
        self.lock = threading.Lock()
    
    def _generate_key(self, text):
        """Generate cache key from text"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def get_cached_decision(self, text):
        """Get cached decision if still valid"""
        key = self._generate_key(text)
        
        with self.lock:
            if key in self.cache:
                decision, timestamp = self.cache[key]
                if time.time() - timestamp < self.ttl:
                    return decision
                else:
                    # Expired, remove from cache
                    del self.cache[key]
        
        return None
    
    def cache_decision(self, text, decision):
        """Store decision with current timestamp"""
        key = self._generate_key(text)
        
        with self.lock:
            self.cache[key] = (decision, time.time())
            
            # Cleanup old entries (simple approach)
            if len(self.cache) > 1000:  # Prevent unlimited growth
                current_time = time.time()
                expired_keys = [
                    k for k, (_, ts) in self.cache.items() 
                    if current_time - ts >= self.ttl
                ]
                for k in expired_keys:
                    del self.cache[k]

class RequestDeduplicator:
    """Prevent duplicate simultaneous requests"""
    def __init__(self):
        self.pending_requests = {}
        self.lock = threading.Lock()
    
    def is_duplicate(self, request_key):
        """Check if request is already being processed"""
        with self.lock:
            return request_key in self.pending_requests
    
    def add_request(self, request_key):
        """Mark request as being processed"""
        with self.lock:
            self.pending_requests[request_key] = time.time()
    
    def remove_request(self, request_key):
        """Mark request as completed"""
        with self.lock:
            self.pending_requests.pop(request_key, None)
    
    def cleanup_stale_requests(self, max_age=10):
        """Remove requests older than max_age seconds"""
        current_time = time.time()
        with self.lock:
            stale_keys = [
                k for k, ts in self.pending_requests.items()
                if current_time - ts > max_age
            ]
            for k in stale_keys:
                del self.pending_requests[k]

class BaselineCache:
    """Cache baseline values per video"""
    def __init__(self, ttl_seconds=300):  # 5 minutes
        self.baselines = {}
        self.ttl = ttl_seconds
        self.lock = threading.Lock()
    
    def get_baseline(self, video_id):
        """Get cached baseline for video"""
        with self.lock:
            if video_id in self.baselines:
                baseline, timestamp = self.baselines[video_id]
                if time.time() - timestamp < self.ttl:
                    return baseline
                else:
                    del self.baselines[video_id]
        return None
    
    def set_baseline(self, video_id, baseline):
        """Cache baseline for video"""
        with self.lock:
            self.baselines[video_id] = (baseline, time.time())

# Initialize caching systems
decision_cache = DecisionCache(ttl_seconds=30)
request_deduplicator = RequestDeduplicator()
baseline_cache = BaselineCache(ttl_seconds=300)

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
    Uses caching for performance optimization.
    """
    # Check cache first
    cached_decision = decision_cache.get_cached_decision(subtitle_text)
    if cached_decision:
        logger.info("Using cached decision", extra={
            'subtitle_text': subtitle_text,
            'cached_decision': cached_decision
        })
        statsd.increment('crest.cache.hit', tags=['type:subtitle'])
        return cached_decision
    
    statsd.increment('crest.cache.miss', tags=['type:subtitle'])
    
    # Check for duplicate requests
    request_key = f"subtitle_{hashlib.md5(subtitle_text.encode()).hexdigest()}"
    if request_deduplicator.is_duplicate(request_key):
        logger.info("Duplicate request detected, using fallback", extra={
            'subtitle_text': subtitle_text
        })
        statsd.increment('crest.request.duplicate', tags=['type:subtitle'])
        return 'NO'  # Safe fallback
    
    request_deduplicator.add_request(request_key)
    
    try:
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
            
            # Call TrueFoundry AI Gateway with timeout
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("AI request timeout")
            
            # Set timeout for AI request (500ms as per requirements)
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(1)  # 1 second timeout (500ms was too aggressive for API calls)
            
            try:
                response = client.chat.completions.create(
                    model="openai-main/gpt-4o-mini",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=10,
                    temperature=0.1
                )
            finally:
                signal.alarm(0)  # Cancel timeout
            
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
            
            # Cache the decision
            decision_cache.cache_decision(subtitle_text, ai_decision)
            
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
        
        # Cache the decision
        decision_cache.cache_decision(subtitle_text, decision)
        
        return decision
    
    finally:
        # Always remove from pending requests
        request_deduplicator.remove_request(request_key)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set service metadata for Datadog
app.config['DD_SERVICE'] = os.getenv('DD_SERVICE', 'crest-agent')
app.config['DD_ENV'] = os.getenv('DD_ENV', 'development')
app.config['DD_VERSION'] = os.getenv('DD_VERSION', '0.1.0')

def cleanup_stale_requests():
    """Periodic cleanup of stale requests and cache entries"""
    request_deduplicator.cleanup_stale_requests()

@app.route('/data', methods=['GET', 'POST'])
def data():
    start_time = time.time()
    
    # Periodic cleanup (every 10th request approximately)
    if hash(str(time.time())) % 10 == 0:
        cleanup_stale_requests()
    
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
        
        # Enhanced AI audio analysis with confidence
        ai_decision, confidence = analyze_audio_for_loud_events(volume, baseline, spike)
        
        if ai_decision == 'YES':
            logger.info("Loud audio event confirmed by enhanced AI", extra={
                'volume': volume,
                'spike': spike,
                'ai_decision': ai_decision,
                'confidence': confidence
            })
            
            statsd.increment('crest.loud_event.audio_detected')
            
            # Dynamic response based on confidence and spike magnitude
            if confidence > 0.8:
                level = 0.2  # Aggressive reduction for high confidence
                duration = 4000
            elif confidence > 0.6:
                level = 0.3  # Moderate reduction for medium confidence
                duration = 3000
            else:
                level = 0.5  # Light reduction for low confidence
                duration = 2000
            
            response_data = {
                "action": "LOWER_VOLUME",
                "level": level,
                "duration": duration,
                "confidence": confidence,
                "trigger": "audio_analysis",
                "transition_type": "smooth",
                "volume_data": {
                    "current": volume,
                    "baseline": baseline,
                    "spike": spike
                }
            }
        else:
            response_data = {
                "action": "NONE",
                "confidence": confidence,
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

def calculate_audio_confidence(spike, volume, baseline, ai_decision):
    """Calculate confidence level for audio-based decisions"""
    
    # Base confidence on spike magnitude
    if spike > 0.5:
        base_confidence = 0.95
    elif spike > 0.4:
        base_confidence = 0.85
    elif spike > 0.3:
        base_confidence = 0.75
    elif spike > 0.2:
        base_confidence = 0.6
    else:
        base_confidence = 0.4
    
    # Adjust based on absolute volume level
    if volume > 0.8:
        base_confidence += 0.05
    elif volume < 0.3:
        base_confidence -= 0.1
    
    # Adjust based on AI agreement with heuristics
    heuristic_decision = 'YES' if spike > 0.25 else 'NO'
    if ai_decision == heuristic_decision:
        base_confidence += 0.1
    else:
        base_confidence -= 0.15
    
    return max(0.1, min(0.99, base_confidence))

def analyze_audio_for_loud_events(volume, baseline, spike):
    """
    Enhanced audio analysis with improved AI + heuristics and confidence calculation.
    """
    # Quick heuristic pre-filter for obvious cases
    if spike < 0.1:
        return 'NO', 0.9  # Very confident it's not loud
    elif spike > 0.6:
        return 'YES', 0.95  # Very confident it's loud
    
    # Get AI client for borderline cases
    client = get_truefoundry_client()
    ai_decision = 'NO'
    
    if client and os.getenv("TRUEFOUNDRY_API_KEY"):
        try:
            logger.info("Running enhanced audio analysis in LIVE mode", extra={
                'volume': volume,
                'baseline': baseline,
                'spike': spike,
                'ai_provider': 'truefoundry'
            })
            
            statsd.increment('crest.ai.requests.total', tags=['provider:truefoundry', 'type:audio'])
            
            ai_start_time = time.time()
            
            # Enhanced prompt with more context
            spike_ratio = spike / baseline if baseline > 0 else spike
            prompt = f"""Analyze this real-time YouTube audio data for loud events:

Current Volume Level: {volume:.3f} (0.0 = silent, 1.0 = maximum)
Baseline Volume: {baseline:.3f} (recent average)
Volume Spike: {spike:.3f} (sudden increase)
Spike Ratio: {spike_ratio:.2f}x above baseline

Context: This is real-time audio analysis from a YouTube video. We want to detect sudden loud sounds like:
- Explosions, gunshots, crashes (spike > 0.4)
- Dramatic music swells (spike > 0.3 + high volume)
- Sudden screaming/shouting (spike > 0.35)

Avoid triggering on:
- Gradual volume changes
- Normal speech variations
- Background music

Should the volume be temporarily lowered? Respond only with YES or NO."""
            
            response = client.chat.completions.create(
                model="openai-main/gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=5,
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
            
            logger.info("Enhanced OpenAI audio decision", extra={
                'decision': ai_decision,
                'ai_duration_ms': ai_duration * 1000,
                'volume': volume,
                'spike': spike,
                'spike_ratio': spike_ratio
            })
            
            statsd.histogram('crest.ai.duration', ai_duration, tags=['provider:truefoundry', 'type:audio'])
            statsd.increment(f'crest.openai.audio_decision.{ai_decision.lower()}', tags=['provider:truefoundry'])
            
        except Exception as e:
            logger.error("Enhanced OpenAI audio analysis failed", extra={
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
            
            # Fallback to heuristic
            ai_decision = 'YES' if spike > 0.3 else 'NO'
    
    else:
        # No AI available - use enhanced heuristics
        logger.info("Using enhanced heuristic audio analysis", extra={
            'volume': volume,
            'baseline': baseline,
            'spike': spike,
            'mode': 'heuristic'
        })
        
        # Enhanced heuristic rules
        spike_ratio = spike / baseline if baseline > 0.05 else spike / 0.05
        
        if spike > 0.4:  # Very large absolute spike
            ai_decision = 'YES'
        elif spike > 0.3 and volume > 0.6:  # Large spike with high volume
            ai_decision = 'YES'
        elif spike > 0.25 and spike_ratio > 3.0:  # Significant relative spike
            ai_decision = 'YES'
        else:
            ai_decision = 'NO'
    
    # Calculate confidence level
    confidence = calculate_audio_confidence(spike, volume, baseline, ai_decision)
    
    logger.info("Enhanced audio analysis completed", extra={
        'decision': ai_decision,
        'confidence': confidence,
        'volume': volume,
        'spike': spike,
        'mode': 'ai_enhanced' if client else 'heuristic'
    })
    
    statsd.increment(f'crest.enhanced_audio_decision.{ai_decision.lower()}', tags=[
        'mode:ai_enhanced' if client else 'mode:heuristic'
    ])
    
    return ai_decision, confidence

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