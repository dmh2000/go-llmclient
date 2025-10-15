#!/usr/bin/env python3
"""
Simple file watcher that plays audio.mp3 when it changes.
Uses watchdog to monitor file changes and pygame to play audio.
"""

import os
import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pygame


class AudioFileHandler(FileSystemEventHandler):
    """Handler for audio file change events."""

    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.last_played = 0
        self.debounce_time = 0.5  # Prevent multiple plays from rapid changes

        # Initialize pygame mixer
        pygame.mixer.init()

    def play_audio(self):
        """Play the audio file."""
        current_time = time.time()

        # Debounce: don't play if we just played recently
        if current_time - self.last_played < self.debounce_time:
            return

        try:
            print(f"Playing {self.audio_file}...")
            pygame.mixer.music.load(str(self.audio_file))
            pygame.mixer.music.play()

            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            print("Playback finished.")
            self.last_played = current_time

        except Exception as e:
            print(f"Error playing audio: {e}")

    def on_modified(self, event):
        """Called when a file is modified."""
        if not event.is_directory and Path(event.src_path).name == self.audio_file.name:
            print(f"Detected change to {self.audio_file}")
            self.play_audio()

    def on_created(self, event):
        """Called when a file is created."""
        if not event.is_directory and Path(event.src_path).name == self.audio_file.name:
            print(f"Detected creation of {self.audio_file}")
            self.play_audio()


def main():
    """Main function to set up file watching."""
    # Define the audio file to watch
    audio_file = Path("public/audio.mp3")

    if not audio_file.parent.exists():
        print(f"Directory {audio_file.parent} does not exist!")
        sys.exit(1)

    print(f"Watching for changes to {audio_file.absolute()}")
    print("Press Ctrl+C to stop...")

    # Create event handler and observer
    event_handler = AudioFileHandler(audio_file)
    observer = Observer()
    observer.schedule(event_handler, path=str(audio_file.parent), recursive=False)

    # Start watching
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file watcher...")
        observer.stop()

    observer.join()
    pygame.mixer.quit()
    print("Done.")


if __name__ == "__main__":
    main()
