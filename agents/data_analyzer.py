from autogen_agentchat.agents import AssistantAgent
from prompts.analyzer_prompt import DATA_ANALYZER_PROMPT

def get_data_analyzer_agent(model_client):
    data_analyzer_agent = AssistantAgent(
        name = "Data_Analyzer",
        description="An agent which helps with solving data analysis tasks and gives the code as well.",
        model_client = model_client,
        system_message=DATA_ANALYZER_PROMPT
    )

    return data_analyzer_agent