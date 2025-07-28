from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from config.constants import WORK_DIR, TIMEOUT

def get_docker_executor():
    
    docker = DockerCommandLineCodeExecutor(
        work_dir = WORK_DIR,
        timeout = TIMEOUT
    )

    return docker

async def start_docker_container(docker):
    print("Starting docker container...")
    await docker.start()
    print("Docker Container Started")

async def stop_docker_container(docker):
    print("Stopping docker container...")
    await docker.stop()
    print("Docker Container Stopped")
