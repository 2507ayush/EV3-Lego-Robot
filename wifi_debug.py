import paramiko
import time

HOST = '192.168.86.222'
PORT = 22
USERNAME = 'robot'
PASSWORD = 'maker'

def list_sensor_directories(ssh):
    stdin, stdout, stderr = ssh.exec_command("ls -d /sys/class/lego-sensor/*/")
    dirs = stdout.read().decode().strip().splitlines()
    print(f"Sensor directories found: {dirs}")
    sensor_dirs = [d.rstrip('/').split('/')[-1] for d in dirs if d]
    return sensor_dirs

def check_sensor_directory_exists(ssh, sensor_path):
    stdin, stdout, stderr = ssh.exec_command(f"test -d {sensor_path} && echo exists || echo missing")
    result = stdout.read().decode().strip()
    print(f"Check sensor directory {sensor_path}: {result}")
    return result == "exists"

def read_sensor_file(ssh, file_path):
    stdin, stdout, stderr = ssh.exec_command(f"cat {file_path}")
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if error:
        print(f"Error reading {file_path}: {error}")
    return output, error

def send_command():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {HOST}:{PORT}...")
        ssh.connect(HOST, PORT, USERNAME, PASSWORD, timeout=10)
        print("SSH connection established.")

        sensor_dirs = list_sensor_directories(ssh)
        if not sensor_dirs:
            print("No sensor directories found.")
            return

        SENSOR_DIR = sensor_dirs[0]
        sensor_path = f"/sys/class/lego-sensor/{SENSOR_DIR}"

        if not check_sensor_directory_exists(ssh, sensor_path):
            print(f"Sensor directory {sensor_path} does not exist.")
            return

        while True:
            mode, error_mode = read_sensor_file(ssh, f"{sensor_path}/mode")
            decimals_str, error_decimals = read_sensor_file(ssh, f"{sensor_path}/decimals")
            units, error_units = read_sensor_file(ssh, f"{sensor_path}/units")
            value0_str, error_value0 = read_sensor_file(ssh, f"{sensor_path}/value0")

            if error_mode or error_decimals or error_units or error_value0:
                print("Error reading sensor files.")
            else:
                try:
                    decimals = int(decimals_str)
                    raw_value = int(value0_str)
                    real_value = raw_value / (10 ** decimals) if decimals > 0 else raw_value
                    print(f"Mode: {mode}, Sensor value: {real_value} {units}")
                except ValueError:
                    print("Value conversion error.")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Interrupted by user.")
    except paramiko.ssh_exception.AuthenticationException:
        print("Authentication failed.")
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("Connection failed.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        ssh.close()

send_command()
