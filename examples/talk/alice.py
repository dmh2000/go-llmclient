#!/usr/bin/env python3
import sys
import subprocess
import talk_tcp
import audio_utils

model = "claude-3-5-haiku-20241022"
alice_voice = "vindemiatrix"

alice_system = """
<alice_system>
- Your name is Alice. You are going to ask questions to Bob.
- based on the context, you will ask relevant questions to Bob.
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
    """Main conversation loop between alice and Bob."""
    # Get initial greeting from command line arguments
    if len(sys.argv) < 2:
        print("Usage: talk.py <initial greeting>", file=sys.stderr)
        sys.exit(1)

    initial_greeting = " ".join(sys.argv[1:])

    # Initialize conversation files
    xml_log = "alice.xml"
    context = ""

    # Create/clear the XML log file
    with open(xml_log, "w") as f:
        f.write("<conversation>\n")

    context = alice_system
    context += initial_greeting

    # Log initial greeting
    with open(xml_log, "a") as f:
        f.write(f"  <alice>{initial_greeting}</alice>\n")

    # Play initial greeting
    print(f"alice: {initial_greeting}")
    initial_mp3 = audio_utils.speak(alice_voice, initial_greeting, "alice-initial")
    audio_utils.play_mp3(initial_mp3)

    # create a TCP client here with IP 127.0.0.1 and port 9000
    # have it connect to that server
    socket = talk_tcp.talk_client("127.0.0.1", 9000)

    alice_says = initial_greeting

    # Conversation loop
    n = 0
    i = 0
    while True:
        try:
            print(f"\n--- Round {i + 1} ---")

            # send alice_says
            talk_tcp.talk_send(socket, alice_says)

            # --------- TALK BOB ---------
            # Bob responds to alice
            print("Bob thinking...")

            # wait for  a response from the server
            bob_request = talk_tcp.talk_receive(socket)

            # Log Bob's response
            with open(xml_log, "a") as f:
                f.write(f"  <Bob>{bob_request}</Bob>\n")

            # Update context with Bob's response
            context += f"Bob: {bob_request}\n"

            # --------- TALK TO BOB ---------
            # alice responds to Bob using full context
            print("alice thinking...")
            alice_says = query_llm(context)

            # Update context with alice's response
            context += alice_says

            # Log alice's response
            with open(xml_log, "a") as f:
                f.write(f"  <alice>{alice_says}</alice>\n")

            print(f"alice: {alice_says}")

            # Generate speech for alice
            n += 1
            alice_mp3 = audio_utils.speak(alice_voice, alice_says, f"alice-{n}")
            audio_utils.play_mp3(alice_mp3)
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
