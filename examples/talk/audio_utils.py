#!/usr/bin/env python3
"""Audio utilities for text-to-speech and audio playback."""
import sys
import os
import subprocess
import wave
from google import genai
from google.genai import types
from pydub import AudioSegment


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM audio data to a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def speak(voice, text, file_number):
    """Generate speech from text using Google Gemini TTS API."""
    try:
        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice,
                        )
                    )
                ),
            ),
        )

        data = response.candidates[0].content.parts[0].inline_data.data

        file_name = f"out-{file_number}.wav"
        wave_file(file_name, data)

        return file_name

    except Exception as e:
        print(f"Error in speak: {e}", file=sys.stderr)
        sys.exit(1)


def play_wave(wav_file):
    """Play WAV audio file using ffplay."""
    try:
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", wav_file],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running ffplay: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def play_mp3(mp3_file):
    """Play MP3 audio file using ffplay."""
    try:
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", mp3_file],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running ffplay: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def pcm_to_mp3(pcm_data, output_filename, channels=1, sample_width=2, frame_rate=24000):
    """
    Convert PCM audio data to MP3 format and save to file.

    Args:
        pcm_data: Raw PCM audio data (bytes)
        output_filename: Path to save the MP3 file
        channels: Number of audio channels (default: 1 for mono)
        sample_width: Sample width in bytes (default: 2 for 16-bit)
        frame_rate: Sample rate in Hz (default: 24000)

    Returns:
        str: Path to the created MP3 file
    """
    try:
        # Create AudioSegment from raw PCM data
        audio_segment = AudioSegment(
            data=pcm_data,
            sample_width=sample_width,
            frame_rate=frame_rate,
            channels=channels
        )

        # Export as MP3
        audio_segment.export(output_filename, format="mp3")

        return output_filename

    except Exception as e:
        print(f"Error converting PCM to MP3: {e}", file=sys.stderr)
        sys.exit(1)
