from fastapi import FastAPI, Query, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
from uuid import uuid4
import tempfile
import os
import json
from langchain_core.messages import HumanMessage, AIMessageChunk
from modules.graphs.graph import chat_graph, upload_graph
from config import settings
from modules.database.database import QaADatabase
import uvicorn

FINAL_NODES = settings.FINAL_NODES

app = FastAPI()

app.add_middleware(
    **settings.CORS_CONFIG
)

def serialise_ai_message_chunk(chunk):
    if (isinstance(chunk, AIMessageChunk)):
        return chunk.content 
    else:
        raise TypeError(
            f'Object of type {type(chunk).__name__} is not correctly formatted for serialisation'
        ) 

async def generate_chat_responses(message: str, checkpoint_id: Optional[str] = None):
    is_new_conversation = checkpoint_id is None
    if is_new_conversation:
        new_checkpoint_id = str(uuid4())
        config = {"configurable": {'thread_id': new_checkpoint_id}}
        events = chat_graph.astream_events(
            {"question": HumanMessage(content=message)},
            version='v2',
            config=config,
        )
        payload = {"type": "checkpoint", "checkpoint_id": new_checkpoint_id}
        yield f"data: {json.dumps(payload)}\n\n"
    else:
        config = {"configurable": {'thread_id': checkpoint_id}}
        events = chat_graph.astream_events(
            {"question": HumanMessage(content=message)},
            version='v2',
            config=config,

        )
    
    final_agent = None 

    async for event in events:
        event_type = event['event']
        
        name_agent = event['name']

        output = event['data'].get('output', {})
        if output and isinstance(output, dict):
            if output.get('tags', {}).get('avoid_spam', False):
                continue

        if output and name_agent == 'LangGraph':
            continue
        
        if not final_agent and event_type == 'on_chain_start':  
            # Only streams tokens when it is the final node. Otherwise, return agent_thinking
            if event['name'] in FINAL_NODES:
                final_agent = event['name']

        if not final_agent and event_type == 'on_chain_end' and isinstance(event['data']['output'], dict) and 'agent_think' in event['data']['output'].keys():
            msg = event['data']['output']['agent_think']
            name_agent = event['name']

            safe_content = msg.replace("'", "\\").replace("\n", "\\n")

            payload = {"type": "thoughts", "agent": name_agent, "content": safe_content}
            

            if name_agent == 'retrieve':

                docs_metadatas = f"{[doc.metadata for doc in event['data']['output']['documents']]}"
                docs_metadatas = docs_metadatas.replace("\n", "\\n")

                payload = {"type": "thoughts", "agent": name_agent, "content": msg, 'retrieval_results': docs_metadatas}
                

            yield f"data: {json.dumps(payload)}\n\n"

        
            
        if final_agent and event_type == 'on_chat_model_stream':
            
            chunk_content = serialise_ai_message_chunk(event['data']['chunk'])
            safe_content = chunk_content.replace("'", "\\").replace("\n", "\\n")

            payload = {"type": "final_answer", "agent": name_agent, "content": safe_content}
            yield f"data: {json.dumps(payload)}\n\n"

    yield f'data: {{"type": "end"}} \n\n'


@app.get('/get_chat_history/')
def get_chat_history(user_id: str = Query(...)):
    """
    GET endpoint for getting the chat history.
    """
    raise NotImplementedError("This endpoint is not implemented yet.")
    
@app.get('/chat_stream/')
async def chat_stream(message: str = Query(...), checkpoint_id: Optional[str] = Query(None)):
    """
    GET endpoint for answer generation using chat_graph. Streams responses.
    """
    return StreamingResponse(
        generate_chat_responses(message, checkpoint_id),
        media_type='text/event-stream',
    )


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
    

@app.get('/get_all_questions_from_user/')
def get_all_questions_from_user(user_id: str = Query(...)):
    """
    GET endpoint for getting all questions from a user.
    """
    db = QaADatabase()
    return db.get_all_questions_from_user(user_id)


@app.post('/add_question/')
def add_question(question: str = Form(...), answer: str = Form(...), document: str = Form(None), author: str = Form(None)):
    """
    POST endpoint for adding a question and answer to the database.
    Receives: question, answer, document (nullable), and author.
    """
    try:
        db = QaADatabase()
        db.add_question(question, answer, document, author)
        return JSONResponse(status_code=200, content={"status": "success"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Listening on port {port}")
    uvicorn.run("server.api:app", host="0.0.0.0", port=port)