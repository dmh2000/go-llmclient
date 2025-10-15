"""
Test program for talk_tcp library using two threads.
Server and client exchange messages of varying sizes.
"""

import threading
import time
from talk_tcp import talk_server, talk_accept, talk_client, talk_send, talk_receive, talk_close


def server_thread():
    """Server thread function"""
    print("Server: Starting...")

    # Create and configure server
    server_socket = talk_server("127.0.0.1", 9999)
    print("Server: Listening on 127.0.0.1:9999")

    # Accept client connection
    client_socket = talk_accept(server_socket)
    print("Server: Client connected")

    # Exchange messages
    messages_to_send = [
        "Hello from server!",
        "This is a longer message from the server with more content.",
        "Short msg",
        "A" * 1000,  # 1000 character message
        "Final server message"
    ]

    for i, msg in enumerate(messages_to_send):
        # Send message to client
        print(f"Server: Sending message {i+1} ({len(msg)} bytes)")
        talk_send(client_socket, msg)

        # Receive message from client
        received = talk_receive(client_socket)
        print(f"Server: Received message {i+1} ({len(received)} bytes): {received[:50]}...")

    # Cleanup
    talk_close(client_socket)
    talk_close(server_socket)
    print("Server: Done")


def client_thread():
    """Client thread function"""
    # Give server time to start
    time.sleep(0.5)

    print("Client: Starting...")

    # Connect to server
    client_socket = talk_client("127.0.0.1", 9999)
    print("Client: Connected to server")

    # Exchange messages
    messages_to_send = [
        "Hello from client!",
        "Client response with variable length data here.",
        "OK",
        "B" * 2000,  # 2000 character message
        "Client done"
    ]

    for i, msg in enumerate(messages_to_send):
        # Receive message from server
        received = talk_receive(client_socket)
        print(f"Client: Received message {i+1} ({len(received)} bytes): {received[:50]}...")

        # Send message to server
        print(f"Client: Sending message {i+1} ({len(msg)} bytes)")
        talk_send(client_socket, msg)

    # Cleanup
    talk_close(client_socket)
    print("Client: Done")


def main():
    """Main test function"""
    print("=== TCP Library Test ===\n")

    # Create server and client threads
    server = threading.Thread(target=server_thread)
    client = threading.Thread(target=client_thread)

    # Start threads
    server.start()
    client.start()

    # Wait for both to complete
    server.join()
    client.join()

    print("\n=== Test Complete ===")


if __name__ == "__main__":
    main()
