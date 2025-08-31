from fastapi import FastAPI, Query, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
from uuid import uuid4
import tempfile
import os
import json
from langchain_core.messages import HumanMessage
from modules.graphs.graph import chat_graph, memory
from server.short_answer import get_single_chat_response
from server.full_answer import generate_chat_responses
from config import settings


FINAL_NODES = settings.GraphSettings.FINAL_NODES

app = FastAPI()

app.add_middleware(
    **settings.ApiSettings.CORS_CONFIG
)


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
async def single_chat(message: str = Query(...)):
    """
    GET endpoint for returning only the final answer of a chat. This returns a single chat response, without streaming.
    Also, it returns in the SDK format, with the documents and the answer. 
    """

    response = await get_single_chat_response(message)
    return JSONResponse(status_code=200, content={"answer": response['answer'], "documents": response['retrieved_documents']})


