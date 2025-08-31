"""

This module is responsible for generating a response with the intermediate thinking. 
In another words, the response will be streamed, and will include the thoughts of the AI.

"""
from typing import Optional
from uuid import uuid4
import json
from langchain_core.messages import HumanMessage, AIMessageChunk
from modules.graphs.graph import chat_graph, memory

from config import Settings, settings
import uvicorn

FINAL_NODES = settings.GraphSettings.FINAL_NODES


def serialise_ai_message_chunk(chunk):
    if (isinstance(chunk, AIMessageChunk)):
        return chunk.content 
    else:
        raise TypeError(
            f'Object of type {type(chunk).__name__} is not correctly formatted for serialisation'
        ) 

async def generate_chat_responses(message: str, thread_id: Optional[str] = None, checkpoint_id: Optional[str] = None):
    is_new_conversation = thread_id is None
    
    if is_new_conversation:
        new_thread_id = str(uuid4())
        config = {"configurable": {'thread_id': new_thread_id}}
        
        events = chat_graph.astream_events(
            {"question": HumanMessage(content=message)},
            version='v2',
            config=config,
        )
        payload = {"type": "thread", "thread_id": new_thread_id}
        yield f"data: {json.dumps(payload)}\n\n"
    
    else:

        config = {"configurable": {'thread_id': thread_id}}
        if checkpoint_id:
            config["configurable"]["checkpoint_id"] = checkpoint_id
        events = chat_graph.astream_events(
            {"question": HumanMessage(content=message)},
            version='v2',
            config=config,

        )
    
    final_agent = None 

    async for event in events:
        event_type = event['event']
        
        name_agent = event['name']
        final_agent = event['name'] in FINAL_NODES
        output = event['data'].get('output', {})
        if output and isinstance(output, dict):
            if output.get('tags', {}).get('avoid_spam', False):
                continue

        elif output and name_agent == 'LangGraph':
            continue
        
        # elif not final_agent and event_type == 'on_chain_start':  
            # Only streams tokens when it is the final node. Otherwise, return agent_thinking

        elif not final_agent and event_type == 'on_chain_end' and isinstance(event['data']['output'], dict) and 'agent_think' in event['data']['output'].keys():
            msg = event['data']['output']['agent_think']
            name_agent = event['name']

            safe_content = msg.replace("'", "\\").replace("\n", "\\n")

            payload = {"type": "thoughts", "agent": name_agent, "content": safe_content}
            

            if name_agent == 'retrieve':

                docs_metadatas = f"{[doc.metadata for doc in event['data']['output']['documents']]}"
                docs_metadatas = docs_metadatas.replace("\n", "\\n")

                payload = {"type": "thoughts", "agent": name_agent, "content": msg, 'retrieval_results': docs_metadatas}
                

            yield f"data: {json.dumps(payload)}\n\n"

        
            
        elif final_agent and event_type == 'on_chat_model_stream':
            
            chunk_content = serialise_ai_message_chunk(event['data']['chunk'])
            safe_content = chunk_content.replace("'", "\\").replace("\n", "\\n")

            payload = {"type": "final_answer", "agent": name_agent, "content": safe_content, "streaming": True}
            yield f"data: {json.dumps(payload)}\n\n"

        elif final_agent and event_type == 'on_chain_stream':
            msg = event['data']['chunk']['messages'][-1].content
            name_agent = event['name']

            safe_content = msg.replace("'", "\\").replace("\n", "\\n")

            payload = {"type": "final_answer", "agent": name_agent, "content": safe_content, "streaming": False}
            
            yield f"data: {json.dumps(payload)}\n\n"

    yield f'data: {{"type": "end"}} \n\n'