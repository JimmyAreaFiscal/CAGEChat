"""

This is a private pipeline for uploading documents to the database. 
This is only a extraction and request process, without really data engineering.

"""

import os 
import json 
import requests 

file = 'arquivos/metadados_iniciais.json'
# Files to be uploaded 
metadatas_to_upload = json.load(open(file))
# Get upload password from environment variable or use default
upload_password = os.environ.get("UPLOAD_PASSWORD", "changeme")

# Get server URL and port from environment variables or use defaults
server_url = os.environ.get("SERVER_URL", "http://127.0.0.1")
server_port = os.environ.get("PORT", "10000")
upload_endpoint = f"{server_url}:{server_port}/upload_file/"

for metadata in metadatas_to_upload:
    file_path = metadata['file_path']
    
    # Create a clean metadata dictionary, handling optional fields
    new_metadata = {
        'nome_documento': metadata.get('nome_documento', ''),
        'tipo_documento': metadata.get('tipo_documento', ''),
        'assunto': metadata.get('assunto', ''),
        'tema': metadata.get('tema', '')
    }
    
    # Add optional fields only if they exist in the original metadata
    if 'edição' in metadata:
        new_metadata['edição'] = metadata['edição']
    if 'ano_publicação' in metadata:
        new_metadata['ano_publicação'] = metadata['ano_publicação']
    
    # Prepare multipart form data
    files = {'file': open(file_path, 'rb')}
    form_data = {
        'metadata': json.dumps(new_metadata),
        'password': upload_password
    }
    
    try:
        response = requests.post(
            url=upload_endpoint,
            files=files,
            data=form_data
        )
        
        if response.status_code == 200:
            print(f"File {file_path} uploaded successfully")
        else:
            print(f"Error uploading {file_path}: {response.status_code}")
            print(f"Response: {response.text}")
            raise Exception(f"File {file_path} failed to upload: {response.text}")
    except Exception as e:
        print(f"Exception during upload of {file_path}: {str(e)}")
        raise
    finally:
        # Ensure file is closed
        files['file'].close()


