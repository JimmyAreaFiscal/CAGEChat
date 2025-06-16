from fastapi import FastAPI, Query, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
from uuid import uuid4
import tempfile
import os
import json
from langchain_core.messages import HumanMessage, AIMessageChunk
from modules.graphs.graph import chat_graph, upload_graph, memory

from config import Settings, settings
from modules.database.database import QaADatabase
import uvicorn

FINAL_NODES = settings.GraphSettings.FINAL_NODES

app = FastAPI()

app.add_middleware(
    **settings.ApiSettings.CORS_CONFIG
)

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

@app.get("/health")
def read_health():
   return {"status": "ok"}


async def get_single_chat_response(message: str):
    """
    This function is responsible for getting a single chat response.
    """

    thread_id = str(uuid4())
    config = {"configurable": {'thread_id': thread_id}}
    response = await chat_graph.ainvoke(
        {"question": HumanMessage(content=message)},
        config=config
    )

    DB_URI = settings.DatabaseSettings.DATABASE_URL
    with memory:

        # Delete the checkpoint from the MemorySaver
        await memory.adelete_thread(thread_id)
    
    return response


async def get_last_checkpoint_id(thread_id: str):

    DB_URI = settings.DatabaseSettings.DATABASE_URL 
    with memory:
        history = await memory.get_tuples(thread_id)
        return history[-1][0]


@app.get('/chat/chat_stream/')
async def chat_stream(message: str = Query(...), checkpoint_id: Optional[str] = Query(None)):
    """
    GET endpoint for answer generation using chat_graph. Streams responses.
    """
    return StreamingResponse(
        generate_chat_responses(message, checkpoint_id),
        media_type='text/event-stream',
    )


@app.get('/chat/get_documents/')
async def get_documents(thread_id: str = Query(...)):
    """
    GET endpoint for getting the documents from the object storage.
    """
    return JSONResponse(status_code=500, content={"error": "Not implemented"})


@app.delete('/chat/delete_chat/')
async def delete_chat(thread_id: str = Form(...)):
    """
    DELETE endpoint for deleting a chat.
    """
    with memory:
        await memory.delete_thread(thread_id)
    return JSONResponse(status_code=200, content={"status": "success", "thread_id": thread_id})
    

@app.get('/test/single_chat/')
async def test_chat(message: str = Query(...)):
    """
    GET endpoint for testing the chat. This returns a single chat response, without streaming.
    Also, it returns in the SDK format, with the documents and the answer. 
    """

    response = await get_single_chat_response(message)
    return JSONResponse(status_code=200, content={"answer": response['answer'], "documents": response['retrieved_documents']})




@app.post('/upload_file/')
def upload_file(file: UploadFile = File(...), metadata: str = Form({'tipo_documento': 'manuais'}), password: str = Form(...)):
    """
    POST endpoint for document insert using upload_graph. Accepts PDF/Word file, metadata (as JSON string), and a password.
    """
    
    # Check password
    upload_password = os.getenv("UPLOAD_PASSWORD", "changeme")
    if password != upload_password:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid password.")
    try:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[-1]) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        # Parse metadata
        if metadata is None:
            return JSONResponse(status_code=400, content={"error": "Missing metadata"})
        try:
            metadata_dict = json.loads(metadata)
        except Exception as e:
            return JSONResponse(status_code=400, content={"error": f"Invalid metadata JSON: {str(e)}"})

        # Prepare state for upload_graph
        state = {"file_path": tmp_path, "metadata": metadata_dict}
        # Call upload_graph (synchronous, not streaming)
        upload_graph.invoke(state)

        # Clean up temp file
        os.remove(tmp_path)

        return JSONResponse(status_code=200, content={"status": "success"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    
