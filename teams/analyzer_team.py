from agents.code_executor import get_code_executor_agent
from agents.data_analyzer import get_data_analyzer_agent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

def get_analyzer_gpt_team(docker, model_client):
    code_executor = get_code_executor_agent(docker)

    data_analyzer = get_data_analyzer_agent(model_client)

    termination_condition = TextMentionTermination('STOP')

    team = RoundRobinGroupChat(
        participants=[data_analyzer, code_executor],
        max_turns=30,
        termination_condition=termination_condition
    )

    return team
