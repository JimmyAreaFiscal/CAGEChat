import json
import os
import requests


def load_test_data(filename):
    test_data_path = os.path.join(os.path.dirname(__file__), 'test_data', filename)
    with open(test_data_path, 'r') as file:
        return json.load(file)


def get_llm_response(question):
    responseDict = requests.post(url='https//rahulshettyacademy.com/rag-llm/ask',
                                json = {
                                    'question': question,
                                    'chat_history': []
                                }).json()
    return responseDict