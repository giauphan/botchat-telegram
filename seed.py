import subprocess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def run_migration():
    migrations = [
       "seed/ChatSeed.py",
    ]

    for migration in migrations:
        try:
            subprocess.run(["python3",  migration])
            print(f"Migration successful: {migration}")
        except subprocess.CalledProcessError as e:
            print(f"Migration failed for {migration}. Error: {e}")

if __name__ == "__main__":
    run_migration()