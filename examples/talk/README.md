make_mp3.py

Features
Command-line arguments:
port (required): Port number to listen on
output_path (required): File path where MP3 files will be written
--voice (optional): Voice name for TTS (default: "Puck")
--ip (optional): IP address to bind to (default: "127.0.0.1")
TCP Server:
Uses talk_tcp module to create server and accept connections
Binds to specified IP and port
Waits for a single client connection
Message Processing Loop:
Receives messages using talk_receive()
Generates MP3 files using speak() from audio_utils
Copies the generated MP3 to the specified output path
Cleans up temporary files
Handles connection closure gracefully
Error Handling:
Keyboard interrupt (Ctrl+C) for clean shutdown
Proper socket cleanup in finally block
Connection closed detection
Usage Example

# Basic usage

./make-mp3.py 8080 /tmp/output.mp3

# With custom voice

./make-mp3.py 8080 /tmp/output.mp3 --voice Charon

# With custom IP binding

./make-mp3.py 8080 /tmp/output.mp3 --ip 0.0.0.0
The server will continuously listen for messages and overwrite the output file with each new message received. Each message is converted to speech using Google Gemini TTS and saved as an MP3 file.
