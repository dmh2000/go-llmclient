import sys
import os
import subprocess
from google import genai
from google.genai import types
import wave


# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


if __name__ == "__main__":
    try:
        # get two arguments, voice and text from command line
        voice = str(sys.argv[1])

        # read from sys.argv[2]
        with open(sys.argv[2], "r") as f:
            input_text = f.read()

        # get file number
        n = sys.argv[3]

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
    except Exception as e:
        print(e)
        sys.exit(1)

    data = response.candidates[0].content.parts[0].inline_data.data

    file_name = f"out-{n}.wav"
    wave_file(file_name, data)  # Saves the file to current directory

    # subprocess.call(
    #     ["ffplay", "-nodisp", "-autoexit", file_name]
    # )  # Run ffplay -nodisp -autoexit file.wav
