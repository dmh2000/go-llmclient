#!/usr/bin/env python3
import sys
import subprocess
import talk_tcp
import audio_utils

model = "claude-3-5-haiku-20241022"
bob_voice = "enceladus"

bob_system = """
<bob_system>
- Your name is Bob. You are going to get questions from Alice.
- based on the context, you will answer questions from Alice.
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
    """Main conversation loop - Bob as TCP server."""
    # Initialize conversation files
    xml_log = "bob.xml"
    context = ""

    # Create/clear the XML log file
    with open(xml_log, "w") as f:
        f.write("<conversation>\n")

    # Initialize context with Bob's system prompt
    context = bob_system

    # Create TCP server on IP 127.0.0.1 and port 9000
    print("Bob: Starting server on 127.0.0.1:9000")
    server_socket = talk_tcp.talk_server("127.0.0.1", 9000)

    # Wait for client connection
    print("Bob: Waiting for Alice to connect...")
    client_socket = talk_tcp.talk_accept(server_socket)
    print("Bob: Alice connected")

    # Conversation loop
    n = 0
    while True:
        # Receive message from Alice
        print("\nBob: Waiting for message from Alice...")
        alice_message = talk_tcp.talk_receive(client_socket)

        # Check if connection closed
        if alice_message is None:
            print("Bob: Alice disconnected")
            break

        # Log Alice's message
        with open(xml_log, "a") as f:
            f.write(f"  <alice>{alice_message}</alice>\n")

        print(f"Alice: {alice_message}")

        # Update context with Alice's message
        context += f"Alice: {alice_message}\n"

        # Generate Bob's response using LLM
        print("Bob: Thinking...")
        bob_response = query_llm(context)

        # Update context with Bob's response
        context += bob_response

        # Log Bob's response
        with open(xml_log, "a") as f:
            f.write(f"  <bob>{bob_response}</bob>\n")

        print(f"Bob: {bob_response}")

        # Generate speech for Bob
        n += 1
        bob_wav = audio_utils.speak(bob_voice, bob_response, f"bob-{n}")
        audio_utils.play_wave(bob_wav)

        # Send Bob's response to Alice
        talk_tcp.talk_send(client_socket, bob_response)

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
