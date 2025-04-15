import paramiko
import time

# EV3 connection details
HOST = '192.168.201.222'  # EV3's IP address
PORT = 22                  # SSH port
USERNAME = 'robot'         # Default EV3 username
PASSWORD = 'maker'         # Default EV3 password

def send_command(command):
    try:
        # Set up SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Allow unknown hosts
        # Connect to EV3
        ssh.connect(HOST, PORT, USERNAME, PASSWORD, timeout=10)

        while True:
            # Execute command
            stdin, stdout, stderr = ssh.exec_command(command)

            # Read response
            response = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if error:
                print(f"Error: {error}")
            else:
                print(f"Received UV value: {response}")

            time.sleep(1)  # Wait for 1 second before the next reading

        # Close connection (this line will not be reached in an infinite loop)
        ssh.close()

    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication failed. Check username/password.")
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("Could not connect to EV3. Is SSH enabled?")
    except Exception as e:
        print(f"An error occurred: {e}")

# Command to read UV sensor value (modify this for your EV3 setup)
uv_sensor_command = "cat /sys/class/lego-sensor/sensor0/value0"  # Adjust sensor index if needed
# Command to read UV sensor value with dynamic range
uv_sensor_command_with_range = "cat /sys/class/lego-sensor/sensor0/value0 --range 30.0"  # Adjust sensor index and range as needed


send_command(uv_sensor_command)
