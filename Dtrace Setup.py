import os
import subprocess
import sys
import requests
from time import sleep


def check_admin():
    """Check if the script is running with administrative privileges."""
    if not os.geteuid() == 0:
        print("This script requires administrative privileges.")
        sys.exit(1)


def download_dtrace(msi_url, download_path):
    """Download the DTrace MSI installation file."""
    print(f"Downloading DTrace MSI from {msi_url}...")

    try:
        # Send GET request to fetch the MSI
        response = requests.get(msi_url, stream=True)
        response.raise_for_status()

        # Write content to a file
        with open(download_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded DTrace MSI to {download_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading DTrace MSI: {e}")
        sys.exit(1)


def install_dtrace(msi_path):
    """Install DTrace using the MSI file."""
    try:
        print(f"Installing DTrace from {msi_path}...")
        subprocess.run(["msiexec", "/i", msi_path, "/quiet"], check=True)
        print("DTrace has been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing DTrace: {e}")
        sys.exit(1)


def update_path():
    """Update the PATH environment variable."""
    dtrace_path = r"C:\Program Files\DTrace"

    # Update system PATH for the current session
    os.environ["PATH"] += os.pathsep + dtrace_path
    print(f"Updated PATH environment variable to include: {dtrace_path}")


def enable_dtrace():
    """Enable DTrace using bcdedit."""
    try:
        print("Enabling DTrace using bcdedit...")
        subprocess.run(["bcdedit", "/set", "dtrace", "ON"], check=True)
        print("DTrace has been enabled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error enabling DTrace: {e}")
        sys.exit(1)


def main():
    """Main function to run the steps."""
    check_admin()

    # Set the URL to download the DTrace MSI file
    msi_url = "https://download.microsoft.com/download/7/9/d/79d6b79a-5836-4118-a9b7-60bc77c97bf7/DTrace.amd64.msi"
    download_path = r"C:\Users\Public\Downloads\DTrace.amd64.msi"

    # Step 1: Download DTrace MSI
    download_dtrace(msi_url, download_path)

    # Step 2: Install DTrace
    install_dtrace(download_path)

    # Step 3: Update PATH environment variable
    update_path()

    # Step 4: Enable DTrace
    enable_dtrace()

    print("DTrace installation and configuration is complete.")


if __name__ == "__main__":
    main()
