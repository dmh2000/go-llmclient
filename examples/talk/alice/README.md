# Alice - WebSocket Audio Player

A web application that displays "Alice" and plays MP3 files when they are created or modified.

## Architecture

- **Frontend**: Vanilla TypeScript Vite app that connects to a WebSocket server
- **Backend**: Node.js server with WebSocket support and file watching

## How it Works

1. The frontend connects to a WebSocket server on port 8080
2. The backend watches for changes to `public/audio.mp3`
3. When the file is created or modified, the backend sends the MP3 URL to all connected clients
4. The frontend receives the URL and plays the audio automatically

## Running the Application

### Terminal 1: Start the backend server

```bash
npm run server
```

This starts:
- WebSocket server on port 8080
- HTTP server on port 5173 (for serving MP3 files)
- File watcher for `public/audio.mp3`

### Terminal 2: Start the frontend dev server

```bash
npm run dev
```

This starts the Vite dev server (usually on port 5173, or the next available port).

### Terminal 3: Test the application

Copy or create an MP3 file to trigger playback:

```bash
cp /path/to/your/audio.mp3 public/audio.mp3
```

Or modify the existing file:

```bash
touch public/audio.mp3
```

The audio will play automatically in the browser!

## File Structure

```
alice/
├── public/           # Directory for MP3 files
│   └── audio.mp3    # The watched audio file
├── src/
│   ├── main.ts      # Frontend WebSocket client and audio player
│   └── style.css    # Styling
├── server.js        # Backend WebSocket server with fs.watch
├── index.html       # Main HTML file
└── package.json     # Dependencies and scripts
```

## Features

- Real-time WebSocket connection with auto-reconnect
- Automatic audio playback when files change
- Status indicator (Connected/Disconnected/Error)
- Display of last played file URL
- Clean, modern UI
