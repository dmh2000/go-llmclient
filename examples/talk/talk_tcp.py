"""
Simple TCP client/server library with length-prefixed message protocol.
Messages are prefixed with a 4-byte length header (big-endian) and encoded in UTF-8.
"""

import socket
import struct
import sys


def talk_server(ip_address: str, port: int) -> socket.socket:
    """
    Create and configure a TCP server socket.

    Args:
        ip_address: IP address to bind to
        port: Port number to listen on

    Returns:
        Configured server socket ready to accept connections
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip_address, port))
        server_socket.listen(1)
        return server_socket
    except Exception as e:
        print(f"Error creating server socket: {e}", file=sys.stderr)
        sys.exit(1)


def talk_accept(server_socket: socket.socket) -> socket.socket:
    """
    Accept a single client connection.

    Args:
        server_socket: Server socket to accept connection on

    Returns:
        Connected client socket
    """
    try:
        client_socket, _ = server_socket.accept()
        return client_socket
    except Exception as e:
        print(f"Error accepting connection: {e}", file=sys.stderr)
        sys.exit(1)


def talk_client(ip_address: str, port: int) -> socket.socket:
    """
    Create and connect a TCP client socket.

    Args:
        ip_address: Server IP address to connect to
        port: Server port number

    Returns:
        Connected client socket
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip_address, port))
        return client_socket
    except Exception as e:
        print(f"Error creating client socket: {e}", file=sys.stderr)
        sys.exit(1)


def talk_send(sock: socket.socket, message: str) -> None:
    """
    Send a message with 4-byte length prefix.

    Args:
        sock: Socket to send message on
        message: String message to send
    """
    try:
        # Encode message to UTF-8
        encoded_message = message.encode('utf-8')
        message_length = len(encoded_message)

        # Create 4-byte length prefix (big-endian)
        length_prefix = struct.pack('!I', message_length)

        # Send length prefix + message
        sock.sendall(length_prefix + encoded_message)
    except Exception as e:
        print(f"Error sending message: {e}", file=sys.stderr)
        sys.exit(1)


def talk_receive(sock: socket.socket) -> str | None:
    """
    Receive a length-prefixed message.

    Args:
        sock: Socket to receive message from

    Returns:
        Received message as string, or None if connection closed
    """
    try:
        # Read 4-byte length prefix
        length_prefix = b''
        while len(length_prefix) < 4:
            chunk = sock.recv(4 - len(length_prefix))
            if not chunk:
                return None
            length_prefix += chunk

        # Unpack message length (big-endian)
        message_length = struct.unpack('!I', length_prefix)[0]

        # Read message data
        message_data = b''
        while len(message_data) < message_length:
            chunk = sock.recv(message_length - len(message_data))
            if not chunk:
                return None
            message_data += chunk

        # Decode UTF-8 and return
        return message_data.decode('utf-8')
    except Exception as e:
        print(f"Error receiving message: {e}", file=sys.stderr)
        sys.exit(1)


def talk_close(sock: socket.socket) -> None:
    """
    Close a socket.

    Args:
        sock: Socket to close
    """
    try:
        sock.close()
    except Exception as e:
        print(f"Error closing socket: {e}", file=sys.stderr)
        sys.exit(1)
