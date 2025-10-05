import subprocess
import sys
import os

def install_requirements():
    """Install required packages from requirements.txt"""
    try:
        # Check if requirements.txt exists
        if not os.path.exists('requirements.txt'):
            print("requirements.txt not found!")
            return False
        
        # Install packages
        print("Installing required packages...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              check=True, capture_output=True, text=True)
        
        print("All packages installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    install_requirements()
