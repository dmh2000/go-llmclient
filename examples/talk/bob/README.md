# Bob - WebSocket Audio Player with Text Input

A web application that displays "Bob", accepts text input, and plays MP3 files when they are created or modified.

## Architecture

- **Frontend**: Vanilla TypeScript Vite app with text input form and WebSocket client
- **Backend**: Node.js server with Express (POST endpoint), WebSocket support, and file watching

## How it Works

1. The user enters text in the input field and submits it
2. The text is POSTed to the backend `/submit` endpoint
3. After successful submission, the frontend connects to the WebSocket server on port 8081
4. The backend watches for changes to `public/audio.mp3`
5. When the file is created or modified, the backend sends the MP3 URL to all connected clients
6. The frontend receives the URL and plays the audio automatically with a visual indicator

## Running the Application

### Terminal 1: Start the backend server

```bash
npm run server
```

This starts:
- Express HTTP server on port 5174 (for serving MP3 files and handling POST requests)
- WebSocket server on port 8081
- File watcher for `public/audio.mp3`

### Terminal 2: Start the frontend dev server

```bash
npm run dev
```

This starts the Vite dev server (usually on port 5173, or the next available port).

### Terminal 3: Test the application

1. Open the app in your browser
2. Enter some text in the input field and click "Submit"
3. Copy or create an MP3 file to trigger playback:

```bash
cp /path/to/your/audio.mp3 public/audio.mp3
```

Or modify the existing file:

```bash
touch public/audio.mp3
```

The audio will play automatically with an animated visualizer!

## File Structure

```
bob/
├── public/           # Directory for MP3 files
│   └── audio.mp3    # The watched audio file
├── src/
│   ├── main.ts      # Frontend with text form, WebSocket client, and audio player
│   └── style.css    # Styling with input form and visualizer
├── server.js        # Backend Express + WebSocket server with fs.watch
├── index.html       # Main HTML file
└── package.json     # Dependencies and scripts
```

## Features

- Text input form that submits to backend endpoint
- Placeholder function `handleTextSubmission()` for custom text processing
- Real-time WebSocket connection with auto-reconnect
- Automatic audio playback when files change
- Animated audio visualizer (5 waveform bars)
- Status indicator (Connected/Disconnected/Error)
- Display of last played file URL
- Clean, modern UI with dark/light mode support

## Backend Endpoint

### POST `/submit`

Receives text submissions from the frontend.

**Request Body:**
```json
{
  "text": "user entered text"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Text received"
}
```

The `handleTextSubmission(text)` function in [server.js](server.js#L36-L46) is a placeholder that you can implement with your own logic (e.g., LLM processing, audio generation, etc.).
