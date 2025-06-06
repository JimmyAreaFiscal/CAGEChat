"""

This module is responsible for the workflow of the agents.

It uses the langgraph library to create the workflow, and the schemas module to define the state and agent state.

"""
from dotenv import load_dotenv
load_dotenv()


from langgraph.checkpoint.memory import InMemorySaver
from modules.graphs.subgraph_builder import retrieval_workflow_builder
from modules.graphs.graph_builder import chat_workflow_builder, upload_documents_workflow_builder
from config import settings


DB_URI = settings.DatabaseSettings.DATABASE_URL

# Use the latest LangGraph PostgresSaver API (as of 2024-06)
# You do NOT need to create a psycopg Connection or pass connection_kwargs.
# Instead, use PostgresSaver.from_conn_string and pass the database URL directly.

# Remove connection_kwargs and Connection usage entirely.
# Example:
# memory = PostgresSaver.from_conn_string(DB_URI)

# (The rest of the code should use `memory` as the checkpointer.)

memory = InMemorySaver()


# Building the graphs
chat_workflow = chat_workflow_builder()
chat_graph = chat_workflow.compile(checkpointer=memory)

retrieval_workflow = retrieval_workflow_builder()
retrieval_graph = retrieval_workflow.compile()


# Document upload workflow
upload_workflow = upload_documents_workflow_builder()
upload_graph = upload_workflow.compile()

