import os
import platform
import subprocess

def install_terraform(version="1.11.3"):  # Hardcoded version based on successful test.
    """
    Installs Terraform on the system.

    Args:
        version (str): The Terraform version to install. Defaults to the version confirmed to work.
    """

    system = platform.system()
    architecture = platform.machine()

    if system == "Windows":
        if architecture.endswith("64"):
            arch = "windows_amd64"
        else:
            arch = "windows_386"
    elif system == "Linux":
        if architecture.endswith("64"):
            arch = "linux_amd64"
        elif architecture.startswith("arm64") or architecture.startswith("aarch64"):
            arch = "linux_arm64"
        else:
            arch = "linux_386"
    elif system == "Darwin":  # macOS
        if architecture.endswith("64"):
            arch = "darwin_amd64"
        elif architecture.startswith("arm64") or architecture.startswith("aarch64"):
            arch = "darwin_arm64"
        else:
            arch = "darwin_386"
    else:
        print(f"Unsupported operating system: {system}")
        return

    terraform_executable = "terraform.exe" if system == "Windows" else "terraform"
    terraform_path = os.path.join(os.getcwd(), terraform_executable)

    # In this version we assume the terraform.exe or terraform binary is already in the same directory as the script.
    if os.path.exists(terraform_executable):
        os.environ["PATH"] += os.pathsep + os.getcwd() # Add the current dir to path.

        print(f"Terraform executable found at: {os.getcwd()}")

        try:
            subprocess.run(["terraform", "--version"], check=True)
            print("Terraform version check successful.")
        except subprocess.CalledProcessError:
            print("Error checking Terraform version.")
    else:
        print(f"Terraform executable not found. Please download version {version} manually and place it in the same directory as this script.")

if __name__ == "__main__":
    install_terraform()