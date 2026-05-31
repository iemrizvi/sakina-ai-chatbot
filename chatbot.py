from typing import Annotated
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)
llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
)

# def chatbot(state: State):
#     return {"messages": [llm.invoke(state["messages"])]}

def chatbot(state: State):
    messages = [
        SystemMessage(
            content= """  
    You are a friendly Computer Science learning assistant.
    Help students understand programming, databases, AI,
    algorithms, and software development concepts.
    Keep responses short (1-2 lines) unless the user asks
    for a detailed explanation.    """

        )
    ] + state["messages"]

    return {"messages": [llm.invoke(messages)]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()

# def stream_graph_updates(user_input: str):
#     for event in graph.stream({"messages": [HumanMessage(content=user_input)]}):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content)
chat_history = []


def stream_graph_updates(user_input: str):
    chat_history.append(HumanMessage(content=user_input))

    for event in graph.stream({"messages": chat_history}):
        for value in event.values():
            response = value["messages"][-1]

            print("Assistant:", response.content)

            chat_history.append(response)


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)


article = """
Computer Science is the study of computation, algorithms, software, and data.
It powers everything from mobile apps and websites to artificial intelligence
and cybersecurity systems.

Key areas of computer science include:

- Programming and Software Development
- Data Structures and Algorithms
- Databases and Data Management
- Artificial Intelligence and Machine Learning
- Computer Networks
- Cybersecurity
- Operating Systems

A strong computer scientist focuses on problem-solving rather than memorization.
Learning how data flows through a system, how algorithms make decisions, and
how software is designed are essential skills for every developer.

Modern technologies such as cloud computing, AI agents, large language models,
and distributed systems are built upon these core computer science principles.
"""
# from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

# # Defining the system prompt (how the AI should act)
# system_prompt = SystemMessagePromptTemplate.from_template(
#     "You are an AI assistant that helps generate article titles."
# )

# # the user prompt is provided by the user, in this case however the only dynamic
# # input is the article
# user_prompt = HumanMessagePromptTemplate.from_template(
#     """You are tasked with creating a name for a article.
# The article is here for you to examine {article}

# The name should be based of the context of the article.
# Be creative, but make sure the names are clear, catchy,
# and relevant to the theme of the article.

# Only output the article name, no other explanation or
# text can be provided.""",
#     input_variables=["article"]
# )
