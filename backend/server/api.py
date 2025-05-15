from fastapi import FastAPI, Query, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
from uuid import uuid4
import tempfile
import os
import json
from langchain_core.messages import HumanMessage, AIMessageChunk
from backend.modules.graphs.graph import chat_graph, upload_graph
from backend.config import settings
from backend.modules.database.database import QaADatabase


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
        yield f'data:{{"type": "checkpoint", "checkpoint_id": "{new_checkpoint_id}"}} \n\n'
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
            string_to_yield = f"data: {{\"type\": \"thoughts\", \"agent\": \"{name_agent}\", \"content\": \"{safe_content}\"}} \n\n"

            if name_agent == 'retrieve':

                docs_metadatas = f"{[doc.metadata for doc in event['data']['output']['documents']]}"
                docs_metadatas = docs_metadatas.replace("\n", "\\n")
                string_to_yield = f"data: {{\"type\": \"retrieval_result\", \"agent\": \"{name_agent}\", \"content\": \"{safe_content}\", \"retrieval_result\": \"{docs_metadatas}\"}} \n\n"

            yield string_to_yield

        
            
        if final_agent and event_type == 'on_chat_model_stream':
            
            chunk_content = serialise_ai_message_chunk(event['data']['chunk'])
            safe_content = chunk_content.replace("'", "\\").replace("\n", "\\n")
            yield f"data: {{\"type\": \"final_answer\", \"agent\": \"{final_agent}\", \"content\": \"{safe_content}\"}} \n\n"

            
        # if event_type == "on_chat_model_stream":
        #     chunk_content = serialise_ai_message_chunk(event['data']['chunk'])

        #     safe_content = chunk_content.replace("'", "\\").replace("\n", "\\n")
        #     yield f"data: {{\"type\": \"content\", \"content\": \"{safe_content}\"}} \n\n"

        # elif event_type == "on_chat_model_end":
        #     tool_calls = event["data"]["output"].tool_calls if hasattr(event["data"]["output"], "tool_calls") else []
        #     search_calls = [call for call in tool_calls if call["name"] == "tavily_search_results_json"]

        #     if search_calls:
        #         search_query = search_calls[0]['args'].get('query')
        #         safe_query = search_query.replace("'", "\\").replace("\n", "\\n")

        #         yield f"data: {{\"type\": \"search_start\", \"query\": \"{safe_query}\"}} \n\n"
        
        # elif event_type == "on_tool_end":
        #     output = event["data"]["output"]

        #     if isinstance(output, list):
        #         urls = []
        #         for item in output:
        #             if isinstance(item, dict) and 'url' in item:
        #                 urls.append(item['url'])

        #         urls_json = json.dumps(urls)
        #         yield f"data: {{\"type\": \"search_results\", \"urls\": {urls_json}}} \n\n"
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
def upload_file(file: UploadFile = File(...), metadata: str = Form({'tipo_documento': 'manuais'})):
    """
    POST endpoint for document insert using upload_graph. Accepts PDF/Word file and  metadata (as JSON string).
    """
    
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
def add_question(question: str = Form(...), answer: str = Form(...), document: str = Form(None), page: int = Form(None), author: str = Form(None), subject: str = Form(None)):
    """
    POST endpoint for adding a question and answer to the database.
    """
    try:
        db = QaADatabase()
        db.add_question(question, answer, document, page, author, subject)
        return JSONResponse(status_code=200, content={"status": "success"})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

