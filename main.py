#!/usr/bin/env python3
import socket
import os
import time

try:
    from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_C
    from ev3dev2.sound import Sound
except ImportError as e:
    print("Failed to import ev3dev2 modules: {e}. Ensure you're running this on an EV3 brick with Python 3 and ev3dev installed.")
    print("Ensure you're running this on an EV3 brick with Python 3 and ev3dev installed.")
    exit(1)


is_ev3 = os.path.exists('/sys/class/tacho-motor')


DISTANCE_FACTOR = 36
ANGLE_FACTOR = 5.65
SOUND_ON = False
end_char = b"\0"


sound = Sound()

def say(msg):
    if SOUND_ON:
        sound.speak(msg)
    print(msg)


class MockLargeMotor:
    def on_for_degrees(self, speed, degrees):
        print("Mock Motor: Moving at speed {speed} for {degrees} degrees")

    def off(self):
        print("Mock Motor: Motor turned off.")

class MockMoveSteering:
    def __init__(self, output_a, output_c, motor_class=None):
        self.motor_c = MockLargeMotor()
        self.motor_d = MockLargeMotor()

    def on_for_degrees(self, steering, speed, degrees):
        print("Mock Steering: Steering {steering}, Speed {speed}, Degrees {degrees}")

    def off(self):
        print("Mock Steering: Motors turned off.")


steer_pair = None

if is_ev3:
    try:
            
            steering_drive = MoveSteering(OUTPUT_A, OUTPUT_C)
            steering_drive.on_for_seconds(steering=0, speed=100, seconds=5)
            
            # steering_drive.on_for_seconds(steering=50, speed=100, seconds=2)

            # steering_drive.on_for_seconds(steering=0, speed=100, seconds=5)

            steering_drive.on_for_seconds(steering=-50, speed=-100, seconds=10)

            steering_drive.on_for_seconds(steering=0, speed=-100, seconds=10)



            steering_drive.off()
            
            print("Motors (A & C) initialized successfully.")
    except Exception as e:
        print("Error initializing motors: {e}. Check motor connections.")
else:
    print("WARNING: Not running on EV3! Hardware features may not work. Please ensure you are executing this on an EV3 brick.")
    
    steer_pair = MockMoveSteering(OUTPUT_A, OUTPUT_C)

def send_to_socket(socket, message):
    msg = message.encode() + end_char
    total = 0
    while total < len(msg):
        sent = socket.send(msg[total:])
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total += sent

def receive_from_socket(socket):
    recv_buffer = b""
    while end_char not in recv_buffer:
        chunk = socket.recv(1024)
        if chunk == b"":
            raise RuntimeError("Socket connection broken")
        recv_buffer += chunk
    msg = recv_buffer.decode().strip("\0")
    return msg


def move_forward(distance):
    if steer_pair:
        print("Moving forward for {distance} cm")
        steer_pair.on_for_degrees(steering=0, speed=30, degrees=DISTANCE_FACTOR * distance)
    else:
        print("Steering motors not initialized.")

def move_backward(distance):
    if steer_pair:
        print("Moving backward for {distance} cm")
        steer_pair.on_for_degrees(steering=0, speed=-30, degrees=DISTANCE_FACTOR * distance)
    else:
        print("Steering motors not initialized.")

def rotate(angle):
    if steer_pair:
        print("Rotating for {angle} degrees")
        steer_pair.on_for_degrees(steering=-100, speed=30, degrees=ANGLE_FACTOR * angle)
    else:
        print("Steering motors not initialized.")


def establish_connection():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serversocket.bind(("0.0.0.0", 12345))  # Listen on all interfaces
    except OSError as e:
        say("Could not open a socket: {e}")
        exit(1)
    
    print("Listening on port 12345...")
    serversocket.listen(1)

    say('Ready to connect!')

    try:
        clientsocket, address = serversocket.accept()
        print("Connected to {address}")
    except Exception as e:
        print(e)
    return clientsocket


print("Establishing connection")
clientsocket = establish_connection()
print("Connection established")


with clientsocket:
    try:
        while True:
            c = receive_from_socket(clientsocket)
            print("*****")
            print("Received command: {c}")  # Debug statement
            if not c:
                break
            command, *params = c.split(" ")

            print("Processing command: {command} with params: {params}")  # Debug statement

            if command == "MOVE":
                move_forward(float(params[0]))
            elif command == "BACK":
                move_backward(float(params[0]))
            elif command == "ROTATE":
                rotate(float(params[0]))
            else:
                print("Unknown command: {command}")

    except (KeyboardInterrupt, RuntimeError, OSError) as e:
        print("Error: {e}")


say("Shutting down")
if steer_pair:
    steer_pair.off()
