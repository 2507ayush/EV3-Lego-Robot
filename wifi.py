import paramiko
import time

HOST = '192.168.35.222'
PORT = 22
USERNAME = 'robot'
PASSWORD = 'maker'

def list_sensor_directories(ssh):
    stdin, stdout, stderr = ssh.exec_command("ls -d /sys/class/lego-sensor/*/")
    dirs = stdout.read().decode().strip().splitlines()
    sensor_dirs = [d.rstrip('/').split('/')[-1] for d in dirs if d]
    return sensor_dirs

def check_sensor_directory_exists(ssh, sensor_path):
    stdin, stdout, stderr = ssh.exec_command(f"test -d {sensor_path} && echo exists || echo missing")
    result = stdout.read().decode().strip()
    return result == "exists"

def read_sensor_file(ssh, file_path):
    stdin, stdout, stderr = ssh.exec_command(f"cat {file_path}")
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    return output, error

def send_command():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, PORT, USERNAME, PASSWORD, timeout=10)

        sensor_dirs = list_sensor_directories(ssh)
        if not sensor_dirs:
            return

        SENSOR_DIR = sensor_dirs[0]
        sensor_path = f"/sys/class/lego-sensor/{SENSOR_DIR}"

        if not check_sensor_directory_exists(ssh, sensor_path):
            return

        while True:
            mode, error_mode = read_sensor_file(ssh, f"{sensor_path}/mode")
            decimals_str, error_decimals = read_sensor_file(ssh, f"{sensor_path}/decimals")
            units, error_units = read_sensor_file(ssh, f"{sensor_path}/units")
            value0_str, error_value0 = read_sensor_file(ssh, f"{sensor_path}/value0")

            if error_mode or error_decimals or error_units or error_value0:
                pass
            else:
                try:
                    decimals = int(decimals_str)
                    raw_value = int(value0_str)
                    scaled_value = raw_value / (10 ** decimals) if decimals > 0 else raw_value
                    scaled_value_clamped = max(0, min(100, scaled_value))
                    print(f"sensor value: {scaled_value_clamped}")
                except ValueError:
                    pass

            time.sleep(1)

    except KeyboardInterrupt:
        pass
    except paramiko.ssh_exception.AuthenticationException:
        pass
    except paramiko.ssh_exception.NoValidConnectionsError:
        pass
    except Exception:
        pass
    finally:
        ssh.close()

send_command()
