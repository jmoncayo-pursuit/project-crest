# Testing Instructions for Task 1

## Setup and Testing

### 1. Install Flask Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask Server
```bash
python app.py
```
The server should start on http://localhost:5000

### 3. Test Server Endpoint Manually
Open a browser and visit: http://localhost:5000/data
You should see: `{"message": "Hello"}`

### 4. Load Chrome Extension
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `chrome-extension` folder
5. The extension should appear in your extensions list

### 5. Test Extension Communication
1. Navigate to any YouTube video (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)
2. Open Chrome DevTools (F12)
3. Check the Console tab
4. You should see:
   - "Project Crest content script loaded on YouTube"
   - "Service worker loaded" (in the service worker console)
   - "Server connection successful: {message: 'Hello'}"
   - "✅ Server communication test successful"
5. A green notification should appear on the page: "✅ Crest: Server Connected"

### Expected Results
- ✅ Flask server responds with "Hello" message
- ✅ Chrome extension loads without errors
- ✅ Extension successfully fetches data from localhost:5000
- ✅ No CORS errors in console
- ✅ Visual confirmation appears on YouTube page

### Troubleshooting
- If CORS errors occur, ensure flask-cors is installed and CORS(app) is called
- If extension doesn't load, check manifest.json syntax
- If server connection fails, ensure Flask server is running on port 5000