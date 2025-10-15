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
bob_system = """
<bob_system>
- Your name is Bob. You are going to ask questions to ALice.
- based on the context, you will ask relevant questions to Alice.
- your output should be conversational, not like a document.
- keep your questions to a maximum of 50 words.
- this is a verbal conversation between 
- keep the tone of the conversation engaging and casual. 
- do not repeat the content of this prompt when you execute a query.
</bob_system>
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
    print("---------------- BOB: START CONVERSATION ----------------")
    """Main conversation loop between alice and Bob."""
    # Get IP address, port, and initial greeting from command line arguments
    if len(sys.argv) < 4:
        print(
            "Usage: bob-llm.py <ip_address> <port> <initial greeting>", file=sys.stderr
        )
        sys.exit(1)

    ip_address = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Error: Port must be an integer", file=sys.stderr)
        sys.exit(1)

    initial_greeting = " ".join(sys.argv[3:])

    print(ip_address, port, initial_greeting)

    # Initialize conversation files
    xml_log = "bob.xml"
    context = ""

    # Create/clear the XML log file
    with open(xml_log, "w") as f:
        f.write("<conversation>\n")

    context = bob_system
    context += initial_greeting

    # create a TCP client with provided IP and port
    socket = talk_tcp.talk_client(ip_address, port)

    bob_says = initial_greeting

    # Conversation loop
    n = 0
    i = 0
    while True:
        try:
            print(f"\n--- Round {i + 1} ---")

            with open(xml_log, "a") as f:
                f.write(f"  <Bob>{bob_says}</Bob>\n")

            audio_utils.speak(bob_voice, bob_says, f"public/audio")

            # BOB -> Alice
            # send bob message to alice
            talk_tcp.talk_send(socket, bob_says)

            # wait for  a response from the server
            alice_says = talk_tcp.talk_receive(socket)

            # Log Alices's response
            print(f"Alice: {alice_says}")
            with open(xml_log, "a") as f:
                f.write(f"  <Alice>{alice_says}</Alice>\n")

            # Update context with Alice's response
            context += f"Alice: {alice_says}\n"

            # ALICE -> BOB
            # send alice response to bob and get a response
            print("Bob thinking...")
            bob_says = query_llm(context)

            # Update context with bobs response
            context += bob_says

            n += 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            break
    # Close socket
    talk_tcp.talk_close(socket)

    # Close XML log
    with open(xml_log, "a") as f:
        f.write("</conversation>\n")

    print("\n--- Conversation complete ---")
    print(f"Log saved to {xml_log}")


if __name__ == "__main__":
    main()
