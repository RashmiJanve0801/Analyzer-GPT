import asyncio
from teams.analyzer_team import get_analyzer_gpt_team
from agents.data_analyzer import get_data_analyzer_agent
from agents.code_executor import get_code_executor_agent
from config.google_model_client import get_model_client
from config.docker_utils import get_docker_executor, start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

async def main():
    google_model_client = get_model_client()
    docker = get_docker_executor()

    team = get_analyzer_gpt_team(docker, google_model_client)

    try:
        task = "Can you give me a graph of survived and died in my data titanic.csv and save it as output.png ?"

        await start_docker_container(docker)

        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print(message.source, ":", message.content)
            elif isinstance(message, TaskResult):
                print("Stop Reason:", message.stop_reason)

    except Exception as e:
        print(e)

    finally:
        await stop_docker_container(docker)

if __name__ == "__main__":
    asyncio.run(main())


