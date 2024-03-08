import subprocess

def install_packages():
    packages = [
        "telebot",  
        "python-dotenv",
        "pytz",
        "databases",
         "orm",
         "aiosqlite"
    ]

    for package in packages:
        try:
            subprocess.run(["pip", "install", package], check=True)
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")

if __name__ == "__main__":
    install_packages()
    