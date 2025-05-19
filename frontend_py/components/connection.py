from typing import List, Iterator, Dict
import requests 
import json

import sys, os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
CHAT_STREAM_URL = "http://127.0.0.1:8000/chat_stream"

def get_chat_stream(
    message: str,
    checkpoint_id: str | None = None,
    timeout: int = 30,
) -> Iterator[Dict]:
    """
    Stream chat responses from the backend, yielding one JSON event at a time.

    Each yielded dict has the structure:
        {
            "type": Literal["checkpoint", "content", "end", "search_start", "search_results"],
            "content": str,         # present if type == "content"
            "checkpoint_id": str,   # present if type == "checkpoint"
            "results": list[dict]   # present if type == "search_results"
        }
    """
    params = {"message": message}
    if checkpoint_id:
        params["checkpoint_id"] = checkpoint_id

    with requests.get(CHAT_STREAM_URL, params=params, stream=True, timeout=timeout) as resp:
        resp.raise_for_status()

        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line:          # keep-alive / heartbeat
                continue

            # Remove the SSE prefix “data: ” if present
            line = raw_line.lstrip("data:").strip()

            try:
                event = json.loads(line)

            except json.JSONDecodeError:
                # In case the JSON spans multiple lines, keep accumulating.
                # (Backend should emit one JSON per line; adjust here if needed.)
                print(line)
                raise

            if isinstance(event, dict):
                yield event
    

def post_upload_file(file_path: str, metadata: dict) -> str:
    
    assert isinstance(metadata, dict), "Metadata must be a dictionary"
    assert 'tipo_documento' in metadata, "tipo_documento must be in metadata"

    response = requests.post('http://127.0.0.1:8000/upload_file', files={'file': open(file_path, 'rb')}, data=metadata)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error in Request: {response.status_code}")
    
