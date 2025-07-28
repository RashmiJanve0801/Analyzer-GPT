import streamlit as st
import asyncio
import os

from teams.analyzer_team import get_analyzer_gpt_team
from agents.data_analyzer import get_data_analyzer_agent
from agents.code_executor import get_code_executor_agent
from config.google_model_client import get_model_client
from config.docker_utils import get_docker_executor, start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

st.title("Analyzer GPT - Digital Data Analyzer")

uploaded_file = st.file_uploader("Upload your CSV file", type='csv')

if "messages" not in st.session_state:
    st.session_state.messages = []
if "autogen_team_state" not in st.session_state:
    st.session_state.autogen_team_state = None

# task = st.text_input("Enter your task", value="Can you give me the number of columns in my data ?")

task = st.chat_input("Enter your task.")

async def run_analyzer_gpt(docker, google_model_client, task):

    try:
        await start_docker_container(docker)

        team = get_analyzer_gpt_team(docker, google_model_client)

        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state)

        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print(msg := f"{message.source} : {message.content}")
                # yield msg
                if msg.startswith('user'):
                    with st.chat_message('user', avatar='👨'):
                        st.markdown(msg)
                elif msg.startswith('Data_Analyzer'):
                    with st.chat_message('Data Analyst', avatar='🤖'):
                        st.markdown(msg)
                elif msg.startswith('Code_Executor'):
                    with st.chat_message('Code Runner',avatar='🧑🏻‍💻'):
                        st.markdown(msg)
                st.session_state.messages.append(msg)

            elif isinstance(message, TaskResult):
                print(msg := f"Stop Reason:{message.stop_reason}")
                # yield msg
                st.markdown(msg)
                st.session_state.messages.append(msg)
    
        st.session_state.autogen_team_state = await team.save_state()
    
    except Exception as e:
        print(e)

    finally:
        await stop_docker_container(docker)

if st.session_state.messages:
    for msg in st.session_state.messages:
        st.markdown(msg)

if task:
    if uploaded_file is not None and task:

        if not os.path.exists('temp'):
            os.makedirs('temp')

        with open('temp/data.csv', 'wb') as f:
            f.write(uploaded_file.getbuffer())

    google_model_client = get_model_client()
    docker = get_docker_executor()

    asyncio.run(run_analyzer_gpt(docker, google_model_client, task))

    if os.path.exists('temp/output.png'):
        st.image('temp/output.png', caption='Analysis File')

if not uploaded_file:
    st.warning("Please upload the CSV file.")

