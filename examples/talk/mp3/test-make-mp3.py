#!/usr/bin/env python3
"""
Simple test client for make-mp3.py server.
Connects to the server and sends a test message.
"""
import sys
import argparse
from talk_tcp import talk_client, talk_send, talk_close


def main():
    """Send a test message to the make-mp3 server."""
    parser = argparse.ArgumentParser(description="Test client for make-mp3 server")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Server hostname (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Server port (default: 8080)"
    )
    parser.add_argument(
        "message",
        type=str,
        nargs="?",
        default="hello world",
        help="Message to send (default: 'hello world')",
    )

    args = parser.parse_args()

    print(f"Connecting to {args.host}:{args.port}...")

    try:
        # Connect to server
        client_socket = talk_client(args.host, args.port)
        print("Connected!")

        # Send message (talk_send handles the length prefix protocol)
        print(f"Sending message: '{args.message}'")
        talk_send(client_socket, args.message)
        print("Message sent successfully!")

        import time

        time.sleep(5)

        # Close connection
        talk_close(client_socket)
        print("Connection closed")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
