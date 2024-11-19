import subprocess
import sys

def install_packages():
    """Install required packages using pip."""
    required_packages = ['pygame', 'arabic-reshaper', 'python-bidi']
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please install it manually.")
            sys.exit(1)

def run_main():
    """Run the main.py file."""
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except FileNotFoundError:
        print("main.py not found. Ensure it is in the same directory.")
        sys.exit(1)

if __name__ == "__main__":
    install_packages()
    run_main()
