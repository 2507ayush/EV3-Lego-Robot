#!/usr/bin/env python3
import socket
import os
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_B, OUTPUT_C

# Initialize Motors
steer_pair = MoveSteering(OUTPUT_B, OUTPUT_C)

# Server Setup
HOST = "192.168.82.222"  # Listen on all interfaces
PORT = 22

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"EV3 Server listening on port {PORT}...")

# Accept Connection
client_socket, addr = server_socket.accept()
print(f"Connected to {addr}")

def move_forward(distance):
    print(f"Moving forward: {distance} cm")
    steer_pair.on_for_degrees(0, 30, distance * 36)

def move_backward(distance):
    print(f"Moving backward: {distance} cm")
    steer_pair.on_for_degrees(0, -30, distance * 36)

def handle_command(command):
    parts = command.strip().split()
    if len(parts) < 2:
        return

    action, value = parts[0], float(parts[1])

    if action == "MOVE":
        move_forward(value)
    elif action == "BACK":
        move_backward(value)
    else:
        print(f"Unknown command: {action}")

# Receive and Process Commands
try:
    while True:
        command = client_socket.recv(1024).decode().strip()
        if not command:
            break
        print(f"Received: {command}")
        handle_command(command)
except KeyboardInterrupt:
    print("Shutting down server.")
finally:
    client_socket.close()
    server_socket.close()
