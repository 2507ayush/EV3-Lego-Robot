import socket

EV3_IP = '192.168.105.222'
EV3_PORT = 22
END_CHAR = b'\0'

def send_command(sock, command):
    msg = command.encode() + END_CHAR
    sock.sendall(msg)

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((EV3_IP, EV3_PORT))
            print(f"Connected to EV3 at {EV3_IP}:{EV3_PORT}")

            commands = [
                "MOVE 20",
                "BACK 20",
                "ROTATE 90",
                "MOTORB 50 360"
            ]

            for cmd in commands:
                print(f"Sending command: {cmd}")
                send_command(sock, cmd)
                input("Press Enter to send next command...")

    except ConnectionRefusedError:
        print(f"Connection to EV3 at {EV3_IP}:{EV3_PORT} refused. Is the main.py server running on the EV3 brick?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
