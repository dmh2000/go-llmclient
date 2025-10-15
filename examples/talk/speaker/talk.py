#!/usr/bin/env python3
import sys
import os
import subprocess
import wave
from google import genai
from google.genai import types

model = "claude-3-5-haiku-20241022"
astro_voice = "algenib"
moon_voice = "Rasalgethi"


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM audio data to a WAV file."""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def synthesize_text(voice, text, file_number):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    text = "Hello there."
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.WAV
    )

    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config,
    )

    # The response's audio_content is binary.
    file_name = f"out-{file_number}.wav"
    with open(file_name, "wb") as out:
        out.write(response.audio_content)

    return file_name


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


def query_llm(context):
    """Call sqirvy-cli query command with markdown and text file arguments."""
    try:
        result = subprocess.run(
            [
                "../../cmd/bin/sqirvy-cli",
                "query",
                "-m",
                model,
            ],
            input=context,
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
    xml_log = "talk.xml"
    context = ""

    # Create/clear the XML log file
    with open(xml_log, "w") as f:
        f.write("<conversation>\n")

    # Initialize context with the initial greeting
    with open("astro.xml", "r") as f:
        astro = f.read()

    with open("moon.xml", "r") as f:
        moon = f.read()

    context += astro
    context += moon
    context = f"Astro: {initial_greeting}\n"

    # Log initial greeting
    with open(xml_log, "a") as f:
        f.write(f"  <astro>{initial_greeting}</astro>\n")

    # Play initial greeting
    print(f"Astro: {initial_greeting}")
    initial_wav = speak(astro_voice, initial_greeting, "astro-initial")
    audio(initial_wav)

    # Conversation loop
    n = 0
    for i in range(5):
        print(f"\n--- Round {i + 1} ---")

        # Moon responds to Astro using full context
        print("Moon thinking...")
        context += "<silent>answer a question from astro about the topic</silent>"
        moon_response = query_llm(context)

        # Update context with Moon's response
        context += f"Moon: {moon_response}\n"

        # Log Moon's response
        with open(xml_log, "a") as f:
            f.write(f"  <moon>{moon_response}</moon>\n")

        print(f"Moon: {moon_response}")

        # Generate speech for Moon
        n += 1
        moon_wav = speak(moon_voice, moon_response, f"{n}")

        audio(moon_wav)

        # Astro responds to Moon using full context
        print("Astro thinking...")
        context += "<silent>ask a question to moon about the topic</silent>"
        astro_response = query_llm(context)

        # Update context with Astro's response
        context += f"Astro: {astro_response}\n"

        # Log Astro's response
        with open(xml_log, "a") as f:
            f.write(f"  <astro>{astro_response}</astro>\n")

        print(f"Astro: {astro_response}")

        # Generate speech for Astro
        n += 1
        astro_wav = speak(astro_voice, astro_response, f"{n}")
        audio(astro_wav)

    # Close XML log
    with open(xml_log, "a") as f:
        f.write("</conversation>\n")

    print("\n--- Conversation complete ---")
    print(f"Log saved to {xml_log}")


if __name__ == "__main__":
    main()
