import ctypes
import sys
import subprocess
import time

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

def run_as_admin():
    """Restart the script with administrative privileges."""
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except Exception as e:
        print(f"Failed to restart as admin: {e}")
        sys.exit(1)

def kill_svchost():
    """Terminate svchost.exe processes."""
    try:
        subprocess.run(["taskkill", "/F", "/IM", "svchost.exe"], check=True)
        print("svchost.exe processes have been terminated.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to terminate svchost.exe: {e}")

if __name__ == "__main__":
    if not is_admin():
        run_as_admin()
        sys.exit()

    time.sleep(2)

    kill_svchost()

    print("Script is running with administrative privileges.")
