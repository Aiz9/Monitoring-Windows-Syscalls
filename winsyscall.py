import psutil
import subprocess
import time
import os

# Path to DTrace executable

DTRACE_PATH = r"C:\Program Files\DTrace\dtrace.exe"

# Check if DTrace is available
if not os.path.exists(DTRACE_PATH):
    print("DTrace is not installed or cannot be found.")
    exit()

# Function to start DTrace monitoring for a process by PID
def monitor_process(pid):
    print(f"Monitoring process with PID: {pid}")
    try:
        dtrace_cmd = [DTRACE_PATH, '-n', f'syscall::*:entry /pid == {pid}/ {{trace(execname); }}']

        subprocess.Popen(dtrace_cmd)
        # Run the DTrace command to monitor system calls and API calls for the given PID
        #subprocess.Popen([DTRACE_PATH, '-n', f'syscall:::{pid} == {pid}'])
    except Exception as e:
        print(f"Error starting DTrace for PID {pid}: {e}")



# Function to monitor new processes
def monitor_new_processes():
    known_pids = set()

    while True:
        for proc in psutil.process_iter(['pid', 'name']):
            pid = proc.info['pid']
            if pid not in known_pids:
                known_pids.add(pid)
                print(f"New process detected: {proc.info['name']} (PID: {pid})")
                monitor_process(pid)

        # Wait for a while before checking for new processes again
        time.sleep(1)


if __name__ == "__main__":
    print("Monitoring new processes. Press Ctrl+C to stop.")
    monitor_new_processes()
