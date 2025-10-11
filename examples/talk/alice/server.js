import { WebSocketServer } from 'ws';
import { watch } from 'fs';
import { createServer } from 'http';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Configuration
const WS_PORT = 8080;
const HTTP_PORT = 5173;
const WATCH_FILE = join(__dirname, 'public', 'audio.mp3');

// Create HTTP server for static files
const httpServer = createServer((req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // Serve MP3 files from public directory
  if (req.url && req.url.endsWith('.mp3')) {
    try {
      const filePath = join(__dirname, 'public', req.url);
      const file = readFileSync(filePath);
      res.setHeader('Content-Type', 'audio/mpeg');
      res.writeHead(200);
      res.end(file);
    } catch (err) {
      res.writeHead(404);
      res.end('File not found');
    }
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

httpServer.listen(HTTP_PORT, () => {
  console.log(`HTTP server listening on port ${HTTP_PORT}`);
});

// Create WebSocket server
const wss = new WebSocketServer({ port: WS_PORT });

// Store connected clients
const clients = new Set();

wss.on('connection', (ws) => {
  console.log('Client connected');
  clients.add(ws);

  ws.on('close', () => {
    console.log('Client disconnected');
    clients.delete(ws);
  });

  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
    clients.delete(ws);
  });
});

console.log(`WebSocket server listening on port ${WS_PORT}`);

// Watch for file changes
console.log(`Watching file: ${WATCH_FILE}`);

watch(WATCH_FILE, (eventType, filename) => {
  if (eventType === 'change' || eventType === 'rename') {
    console.log(`File ${eventType}: ${filename}`);

    // Broadcast MP3 URL to all connected clients
    const mp3Url = `http://localhost:${HTTP_PORT}/audio.mp3`;

    clients.forEach((client) => {
      if (client.readyState === 1) { // WebSocket.OPEN
        client.send(mp3Url);
        console.log(`Sent MP3 URL to client: ${mp3Url}`);
      }
    });
  }
});

console.log('Server ready. Place or update audio.mp3 in the public directory to trigger playback.');
