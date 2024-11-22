import subprocess
import sys
from mainMenu import main_menu


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


if __name__ == "__main__":
    install_packages()
    main_menu()

