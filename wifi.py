import paramiko
import time

# EV3 connection details
HOST = '192.168.14.222'  # EV3's IP address
PORT = 22                  # SSH port
USERNAME = 'robot'         # Default EV3 username
PASSWORD = 'maker'         # Default EV3 password

SENSOR_DIR = "sensor1"  # Updated sensor directory based on detected sensor

def send_command():
    try:
        # Set up SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Allow unknown hosts
        # Connect to EV3
        ssh.connect(HOST, PORT, USERNAME, PASSWORD, timeout=10)

        sensor_path = f"/sys/class/lego-sensor/{SENSOR_DIR}"

        while True:
            # Read sensor mode
            stdin, stdout, stderr = ssh.exec_command(f"cat {sensor_path}/mode")
            mode = stdout.read().decode().strip()
            error_mode = stderr.read().decode().strip()

            # Read sensor decimals
            stdin, stdout, stderr = ssh.exec_command(f"cat {sensor_path}/decimals")
            decimals_str = stdout.read().decode().strip()
            error_decimals = stderr.read().decode().strip()

            # Read sensor units
            stdin, stdout, stderr = ssh.exec_command(f"cat {sensor_path}/units")
            units = stdout.read().decode().strip()
            error_units = stderr.read().decode().strip()

            # Read sensor value0
            stdin, stdout, stderr = ssh.exec_command(f"cat {sensor_path}/value0")
            value0_str = stdout.read().decode().strip()
            error_value0 = stderr.read().decode().strip()

            if error_mode or error_decimals or error_units or error_value0:
                print(f"Errors: {error_mode} {error_decimals} {error_units} {error_value0}")
            else:
                print(f"Sensor mode: {mode}")
                print(f"Sensor decimals: {decimals_str}")
                print(f"Sensor units: {units}")
                print(f"Raw sensor value: {value0_str}")

                try:
                    decimals = int(decimals_str)
                    raw_value = int(value0_str)
                    scaled_value = raw_value / (10 ** decimals) if decimals > 0 else raw_value
                    # Clamp scaled value to 0-100 range
                    scaled_value_clamped = max(0, min(100, scaled_value))
                    print(f"Scaled sensor value (0-100): {scaled_value_clamped}")
                except ValueError:
                    print("Invalid numeric value for scaling.")

            time.sleep(1)  # Wait for 1 second before the next reading

    except KeyboardInterrupt:
        print("Stopping sensor reading loop.")
    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication failed. Check username/password.")
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("Could not connect to EV3. Is SSH enabled?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ssh.close()

# Start reading sensor values
send_command()
