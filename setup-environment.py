import os
import sys


def install_requirements():
    os.system(f"{sys.executable} -m pip install -r requirements.txt")


def setup_docker_containers():
    os.system("docker-compose up -d")


def run_generate_data():
    os.system(f"{sys.executable} generate_data.py")


def run_migrate_data():
    os.system(f"{sys.executable} migrate.py")


def main():
    install_requirements()
    setup_docker_containers()
    run_generate_data()
    run_migrate_data()


if __name__ == "__main__":
    main()
