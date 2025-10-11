import './style.css'

// WebSocket connection
let ws: WebSocket;
let audio: HTMLAudioElement | null = null;
let isStarted = false;

function connectWebSocket() {
  const wsUrl = `ws://${window.location.hostname}:8081`;
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
  const inputView = document.querySelector('#input-view');
  const mainView = document.querySelector('#main-view');

  if (inputView && mainView) {
    inputView.classList.add('hidden');
    mainView.classList.remove('hidden');
  }
}

async function handleSubmit(event: Event) {
  event.preventDefault();

  const input = document.querySelector<HTMLInputElement>('#text-input');
  const submitBtn = document.querySelector<HTMLButtonElement>('#submit-button');

  if (!input || !submitBtn) return;

  const text = input.value.trim();
  if (!text) {
    alert('Please enter some text');
    return;
  }

  // Disable input and button while submitting
  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';

  try {
    // Post text to backend endpoint
    const response = await fetch(`http://${window.location.hostname}:5174/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text }),
    });

    if (!response.ok) {
      throw new Error('Failed to submit text');
    }

    console.log('Text submitted successfully');

    // Mark as started and show main view
    isStarted = true;
    showMainView();
    connectWebSocket();

  } catch (error) {
    console.error('Error submitting text:', error);
    alert('Failed to submit text. Please try again.');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Submit';
  }
}

// Setup UI
document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div class="container">
    <h1>Bob</h1>

    <div id="input-view" class="view">
      <form id="text-form" class="input-form">
        <input
          type="text"
          id="text-input"
          class="text-input"
          placeholder="Enter your message..."
          autocomplete="off"
        />
        <button type="submit" id="submit-button" class="submit-button">Submit</button>
      </form>
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
`

// Attach event listener to form
const form = document.querySelector<HTMLFormElement>('#text-form');
if (form) {
  form.addEventListener('submit', handleSubmit);
}
