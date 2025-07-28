import asyncio
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

def get_code_executor_agent(code_executor):
    code_executor_agent = CodeExecutorAgent(
        name = "Code_Executor",
        code_executor = code_executor
    )

    return code_executor_agent

async def main():

    docker = DockerCommandLineCodeExecutor(
    work_dir='temp',
    timeout = 1200
    )

    await docker.start()

    code_executor_agent = get_code_executor_agent(docker)

    task = TextMessage(
        content = ''' Here is the Python code which you have to run.
```python
print("Hello World")```
''',
    source="user"
    )

    try:
        res = await code_executor_agent.on_messages(
            messages=[task],
            cancellation_token=CancellationToken()
        )
        print(f"The result is {res}")

    except Exception as e:
        print(e)

    finally:
        await docker.stop()

if __name__ == "__main__":
    asyncio.run(main())