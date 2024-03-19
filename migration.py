import subprocess
import os


def run_migration():
    migration_dir = "migrations"
    migrations = [
        os.path.join(migration_dir, file)
        for file in os.listdir(migration_dir)
        if file.endswith(".py") and file != "__init__.py"
    ]
    for migration in migrations:
        try:
            subprocess.run(["python3", migration])
            print(f"Migration successful: {migration}")
        except subprocess.CalledProcessError as e:
            print(f"Migration failed for {migration}. Error: {e}")


if __name__ == "__main__":
    run_migration()
