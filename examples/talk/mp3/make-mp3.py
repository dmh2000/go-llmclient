#!/usr/bin/env python3
"""
TCP server that receives text messages and generates MP3 audio files.
Listens on a specified port and converts incoming messages to speech using Google Gemini TTS.
"""
import sys
import argparse
from talk_tcp import talk_server, talk_accept, talk_receive, talk_close
from audio_utils import speak


def main():
    """Main function to run the MP3 generation server."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="TCP server that generates MP3 files from text messages"
    )
    parser.add_argument("port", type=int, help="Port number to listen on")
    parser.add_argument(
        "output_path", type=str, help="Output file path for generated MP3 files"
    )
    parser.add_argument(
        "--voice", type=str, default="Puck", help="Voice name for TTS (default: Puck)"
    )
    parser.add_argument(
        "--ip",
        type=str,
        default="127.0.0.1",
        help="IP address to bind to (default: 127.0.0.1)",
    )

    args = parser.parse_args()

    print(f"Starting MP3 generation server on {args.ip}:{args.port}")
    print(f"Output file: {args.output_path}")
    print(f"Voice: {args.voice}")

    # Create TCP server socket
    server_socket = talk_server(args.ip, args.port)
    print(f"Server listening on {args.ip}:{args.port}")

    try:
        while True:
            # Wait for client connection
            print("Waiting for client connection...")
            client_socket = talk_accept(server_socket)
            print("Client connected!")

            # Message counter for unique file numbering

            file_number = 1

            try:
                while True:
                    # Wait for message from client
                    print(f"\nWaiting for message #{file_number}...")
                    message = talk_receive(client_socket)

                    # Check if connection closed
                    if message is None:
                        print("Client disconnected")
                        break

                    print(
                        f"Received: {message[:50]}..."
                        if len(message) > 50
                        else f"Received: {message}"
                    )

                    # Generate MP3 file from message
                    print(f"Generating MP3 with voice '{args.voice}'...")
                    temp_file = speak(args.voice, message, file_number)

                    # Write/copy MP3 file to specified output path
                    import shutil

                    shutil.copy(temp_file, args.output_path)
                    print(f"MP3 file written to: {args.output_path}")

                    # Clean up temporary file
                    import os

                    os.remove(temp_file)

                    file_number += 1

            except Exception as e:
                print(f"Error in main loop: {e}", file=sys.stderr)
            finally:
                # Clean up connections
                talk_close(client_socket)

    except Exception as e:
        print(f"Error in main loop: {e}", file=sys.stderr)
    finally:
        # Clean up server socket
        talk_close(server_socket)


if __name__ == "__main__":
    main()
