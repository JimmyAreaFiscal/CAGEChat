"""

This module is responsible for the workflow of the agents.

It uses the langgraph library to create the workflow, and the schemas module to define the state and agent state.

"""
from dotenv import load_dotenv
load_dotenv()


from langgraph.checkpoint.memory import InMemorySaver
from modules.graphs.subgraph_builder import retrieval_workflow_builder
from modules.graphs.graph_builder import chat_workflow_builder, upload_documents_workflow_builder
from config import Settings, settings


memory = InMemorySaver()


# Building the graphs
chat_workflow = chat_workflow_builder(settings)
chat_graph = chat_workflow.compile(checkpointer=memory)

retrieval_workflow = retrieval_workflow_builder(settings)
retrieval_graph = retrieval_workflow.compile()


# Document upload workflow
upload_workflow = upload_documents_workflow_builder(settings)
upload_graph = upload_workflow.compile()

