"""

This module is responsible for generating a response with only the final answer.

This is specifically used for general testing and whatsapp conversations, where the system can't use streaming.

"""
from typing import Optional
from uuid import uuid4
import json
from langchain_core.messages import HumanMessage
from modules.graphs.graph import chat_graph, memory

from config import Settings, settings


async def get_single_chat_response(message: str, checkpoint_id: Optional[str] = None):
    """
    This function is responsible for getting a single chat response.
    """

    checkpoint_id = checkpoint_id or str(uuid4())
    config = {"configurable": {'thread_id': checkpoint_id}}
    response = await chat_graph.ainvoke(
        {"question": HumanMessage(content=message)},
        config=config
    )

    return response