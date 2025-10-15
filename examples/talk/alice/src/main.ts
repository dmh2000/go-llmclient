import './style.css';

// WebSocket connection
let ws: WebSocket;
let audio: HTMLAudioElement | null = null;
let isStarted = false;
let WS_PORT = 8002;


function connectWebSocket() {
  const wsUrl = `ws://${window.location.hostname}:${WS_PORT}`;
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log('WebSocket connected');
    updateStatus('Connected');
  };

  ws.onmessage = (event) => {
    console.log('Received message:', event.data);
    playAudio(event.data);
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
    updateStatus('Error');
  };

  ws.onclose = () => {
    console.log('WebSocket closed');
    updateStatus('Disconnected');
    // Attempt to reconnect after 3 seconds
    setTimeout(connectWebSocket, 3000);
  };
}

function playAudio(url: string) {
  if (!isStarted) {
    console.log('Not started yet, skipping audio playback');
    return;
  }

  // Stop current audio if playing
  if (audio) {
    audio.pause();
    audio.currentTime = 0;
  }

  // Create new audio element and play
  console.log('Playing audio:', url);
  audio = new Audio(url);

  // Show playing indicator when audio starts
  audio.addEventListener('play', () => {
    showPlayingIndicator();
  });

  // Hide playing indicator when audio ends or is paused
  audio.addEventListener('ended', () => {
    hidePlayingIndicator();
  });

  audio.addEventListener('pause', () => {
    hidePlayingIndicator();
  });

  audio.addEventListener('error', () => {
    hidePlayingIndicator();
  });

  audio.play().catch(error => {
    console.error('Error playing audio:', error);
    hidePlayingIndicator();
  });

  updateLastPlayed(url);
}

function updateStatus(status: string) {
  const statusEl = document.querySelector('#status');
  if (statusEl) {
    statusEl.textContent = status;
    statusEl.className = `status ${status.toLowerCase()}`;
  }
}

function updateLastPlayed(url: string) {
  const lastPlayedEl = document.querySelector('#last-played');
  if (lastPlayedEl) {
    lastPlayedEl.textContent = url;
  }
}

function showPlayingIndicator() {
  const indicator = document.querySelector('#playing-indicator');
  if (indicator) {
    indicator.classList.add('active');
  }
}

function hidePlayingIndicator() {
  const indicator = document.querySelector('#playing-indicator');
  if (indicator) {
    indicator.classList.remove('active');
  }
}

function showMainView() {
  const startView = document.querySelector('#start-view');
  const mainView = document.querySelector('#main-view');

  if (startView && mainView) {
    startView.classList.add('hidden');
    mainView.classList.remove('hidden');
  }
}

function handleStart() {
  isStarted = true;
  showMainView();
  connectWebSocket();
}

// Setup UI
document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div class="container">
    <h1>Alice</h1>

    <div id="start-view" class="view">
      <p class="start-message">Click the button below to start</p>
      <button id="start-button" class="start-button">Start</button>
    </div>

    <div id="main-view" class="view hidden">
      <div id="playing-indicator" class="audio-visualizer">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </div>
      <div class="status-container">
        <p>Status: <span id="status" class="status">Connecting...</span></p>
      </div>
      <div class="info-container">
        <p>Last played: <span id="last-played">None</span></p>
      </div>
    </div>
  </div>
`;

// Attach event listener to start button
const startButton = document.querySelector<HTMLButtonElement>('#start-button');
if (startButton) {
  startButton.addEventListener('click', handleStart);
}
