import { WebSocketServer } from "ws";
import { watch } from "fs";
import express from "express";
import { readFileSync, writeFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import cors from "cors";
import spawn_llm from "./spawn-llm.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Configuration
const WS_PORT = 9002;
const HTTP_PORT = 9003;
const WATCH_FILE = join(__dirname, "public", "audio.mp3");

// Create Express app
const app = express();
app.use(cors());
app.use(express.json());

// Serve static files from public directory
app.use(express.static(join(__dirname, "public")));

// POST endpoint to receive text submissions
app.post("/submit", (req, res) => {
  const { text } = req.body;

  console.log("Received text submission:", text);

  // TODO: Placeholder function - implement your logic here
  handleTextSubmission(text);

  res.json({ success: true, message: "Text received" });
});

// Placeholder function for handling text submissions
function handleTextSubmission(text) {
  // start the bob serveer
  console.log("initial greeting", text);
  spawn_llm("bob-llm.py", "127.0.0.1", "10000", text);
}

// Start HTTP server
app.listen(HTTP_PORT, () => {
  console.log(`HTTP server listening on port ${HTTP_PORT}`);
});

// Create WebSocket server
const wss = new WebSocketServer({ port: WS_PORT });

// Store connected clients
const clients = new Set();

wss.on("connection", (ws) => {
  console.log("Client connected");
  clients.add(ws);

  ws.on("close", () => {
    console.log("Client disconnected");
    clients.delete(ws);
  });

  ws.on("error", (error) => {
    console.error("WebSocket error:", error);
    clients.delete(ws);
  });
});

console.log(`WebSocket server listening on port ${WS_PORT}`);

// Watch for file changes
console.log(`Watching file: ${WATCH_FILE}`);

watch(WATCH_FILE, (eventType, filename) => {
  if (eventType === "change") {
    console.log(`File ${eventType}: ${filename}`);

    // Broadcast MP3 URL to all connected clients
    const mp3Url = `http://localhost:${HTTP_PORT}/audio.mp3`;

    clients.forEach((client) => {
      if (client.readyState === 1) {
        // WebSocket.OPEN
        client.send(mp3Url);
        console.log(`Sent MP3 URL to client: ${mp3Url}`);
      }
    });
  }
});

console.log(
  "Server ready. Place or update audio.mp3 in the public directory to trigger playback."
);
