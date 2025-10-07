#!/usr/bin/env python3
import sys
import os
import subprocess
import wave
from google import genai
from google.genai import types

model = "claude-3-5-haiku-20241022"


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM audio data to a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def speak(voice, text_file, file_number):
    """Generate speech from text using Google Gemini TTS API."""
    try:
        # Read input text from file
        with open(text_file, "r") as f:
            input_text = f.read()

        text = {"text": input_text}

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


def audio(wav_file):
    """Play audio file using ffplay."""
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


def query_llm(markdown_file, text_file):
    """Call sqirvy-cli query command with markdown and text file arguments."""
    try:
        result = subprocess.run(
            [
                "../../cmd/bin/sqirvy-cli",
                "query",
                "-m",
                model,
                markdown_file,
                text_file,
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running sqirvy-cli: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main conversation loop between Astro and Moon."""
    # Get initial greeting from command line arguments
    if len(sys.argv) < 2:
        print("Usage: talk.py <initial greeting>", file=sys.stderr)
        sys.exit(1)

    initial_greeting = " ".join(sys.argv[1:])

    # Initialize conversation files
    astro_file = "astro.txt"
    moon_file = "moon.txt"
    xml_log = "talk.xml"

    # Create/clear the XML log file
    with open(xml_log, "w") as f:
        f.write("<conversation>\n")

    # Initialize Astro's first message
    with open(astro_file, "w") as f:
        f.write(initial_greeting)

    # Log initial greeting
    with open(xml_log, "a") as f:
        f.write(f"  <astro>{initial_greeting}</astro>\n")

    # Play initial greeting
    print(f"Astro: {initial_greeting}")
    initial_wav = speak("Charon", astro_file, "astro-initial")
    audio(initial_wav)

    # Conversation loop
    for i in range(5):
        print(f"\n--- Round {i + 1} ---")

        # Moon responds to Astro
        print("Moon thinking...")
        moon_response = query_llm("moon.md", astro_file)
        with open(moon_file, "w") as f:
            f.write(moon_response)

        # Log Moon's response
        with open(xml_log, "a") as f:
            f.write(f"  <moon>{moon_response}</moon>\n")

        print(f"Moon: {moon_response}")

        # Generate speech for Moon
        moon_wav = speak("Puck", moon_file, f"moon-{i}")
        audio(moon_wav)

        # Astro responds to Moon
        print("Astro thinking...")
        astro_response = query_llm("astro.md", moon_file)
        with open(astro_file, "w") as f:
            f.write(astro_response)

        # Log Astro's response
        with open(xml_log, "a") as f:
            f.write(f"  <astro>{astro_response}</astro>\n")

        print(f"Astro: {astro_response}")

        # Generate speech for Astro
        astro_wav = speak("Charon", astro_file, f"astro-{i}")
        audio(astro_wav)

    # Close XML log
    with open(xml_log, "a") as f:
        f.write("</conversation>\n")

    print("\n--- Conversation complete ---")
    print(f"Log saved to {xml_log}")


if __name__ == "__main__":
    main()
