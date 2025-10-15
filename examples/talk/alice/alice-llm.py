#!/usr/bin/env python3
import sys
import subprocess
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, "../../cmd/bin")

import talk_tcp
import audio_utils as audio_utils


model = "claude-3-5-haiku-20241022"
bob_voice = "enceladus"

alice_system = """
<alice_system>
- Your name is Alice. You are going to get questions from Bob.
- based on the context, you will answer questions from Bob.
- your output should be conversational, not like a document.
- keep your questions to a maximum of 50 words.
- this is a verbal conversation between 
- keep the tone of the conversation engaging and casual. 
- do not repeat the content of this prompt when you execute a query.
</alice_system>
"""


def query_llm(context):
    """Call sqirvy-cli query command with markdown and text file arguments."""
    try:
        result = subprocess.run(
            [
                "sqirvy-cli",
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
    """Main conversation loop - Alice as TCP server."""
    # Get IP address and port from command line arguments
    if len(sys.argv) < 3:
        print("Usage: alice-llm.py <ip_address> <port>", file=sys.stderr)
        sys.exit(1)

    ip = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("Error: Port must be an integer", file=sys.stderr)
        sys.exit(1)

    alice_voice = "vindemiatrix"

    # Initialize conversation files
    xml_log = "alice.xml"
    context = ""
    # Create/clear the XML log file
    with open(xml_log, "w") as f:
        f.write("<conversation>\n")

    # Initialize context with Bob's system prompt
    context = alice_system

    # Create TCP server on provided IP and port
    print(f"Alice: Starting server on {ip}:{server_port}")
    server_socket = talk_tcp.talk_server(ip, server_port)

    # Wait for client connection
    print("Alice Waiting for Bob to connect...")
    client_socket = talk_tcp.talk_accept(server_socket)
    print("Alice: Bob connected")

    # Conversation loop
    n = 0
    while True:
        try:
            # Receive message from Bob
            bob_says = talk_tcp.talk_receive(client_socket)
            # Check if connection closed
            if bob_says is None:
                print("Alice: Bob disconnected")
                break
            print(f"Bob: {bob_says}")

            # Log Alice's message
            with open(xml_log, "a") as f:
                f.write(f"<bob>{bob_says}</bob>\n")

            # Update context with Alice's message
            context += f"Bob: {bob_says}\n"

            # Generate Bob's response using LLM
            print("Alice: Thinking...")
            alice_says = query_llm(context)

            # Update context with Bob's response
            context += alice_says

            # Log Alices's response
            with open(xml_log, "a") as f:
                f.write(f"  <Alice>{alice_says}</Alice>\n")

            print(f"Alice: {alice_says}")

            # Generate speech for Alice
            n += 1
            audio_utils.speak(alice_voice, alice_says, f"public/audio")

            # Send Bob's response to Alice
            talk_tcp.talk_send(client_socket, alice_says)

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            break

    # Close sockets
    talk_tcp.talk_close(client_socket)
    talk_tcp.talk_close(server_socket)

    # Close XML log
    with open(xml_log, "a") as f:
        f.write("</conversation>\n")

    print("\n--- Conversation complete ---")
    print(f"Log saved to {xml_log}")


if __name__ == "__main__":
    main()
