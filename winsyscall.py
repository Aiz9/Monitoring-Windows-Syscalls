import psutil
import subprocess
import time
import os
import signal

# Path to DTrace executable
DTRACE_PATH = r"C:\Program Files\DTrace\dtrace.exe"

# Log file for all monitored processes
LOG_FILE = "syscall_log.log"

# Check if DTrace is available
if not os.path.exists(DTRACE_PATH):
    print("DTrace is not installed or cannot be found.")
    exit()


def monitor_process(pid):
    """
    Starts a DTrace monitor for the given process (PID) and appends the output to a log file.
    """
    print(f"Starting DTrace monitoring for PID: {pid}")
    try:
        # DTrace script to monitor system calls for the process
        dtrace_script = f''' syscall:::entry /pid == {pid}/ {{printf("%d, %Y, %s, %s, %s\\n", pid, walltimestamp, execname, probefunc, copyinstr(arg0)); }}'''
        # Open the log file in append mode
        with open(LOG_FILE, "a") as logfile:
            dtrace_cmd = [DTRACE_PATH, "-n", dtrace_script]
            subprocess.Popen(dtrace_cmd, stdout=logfile, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(f"Error starting DTrace for PID {pid}: {e}")


def monitor_new_processes():
    """
    Continuously monitors new processes and starts DTrace monitoring for each new process.
    """
    known_pids = set()

    print(f"Monitoring new processes. Logs will be saved to '{LOG_FILE}'. Press Ctrl+C to stop.")

    try:
        while True:
            # Iterate through all running processes
            for proc in psutil.process_iter(['pid', 'name']):
                pid = proc.info['pid']
                # Skip processes already being monitored
                if pid not in known_pids:
                    known_pids.add(pid)
                    print(f"New process detected: {proc.info['name']} (PID: {pid})")
                    monitor_process(pid)

            # Wait for a short period before checking again
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user. Exiting...")
    except Exception as e:
        print(f"An error occurred during monitoring: {e}")


if __name__ == "__main__":
    # Ensure the log file exists
    open(LOG_FILE, "a").close()

    # Start monitoring for new processes
    monitor_new_processes()
