# Pytest 
import requests
from backend_test.utils import load_test_data, get_llm_response
from ragas import SingleTurnSample
from ragas.metrics import LLMContextPrecisionWithoutReference
from ragas.llms import LangchainLLMWrapper
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import pytest

load_dotenv()


@pytest.mark.asyncio
@pytest.mark.parametrize("getData", 
                         [ 
                            load_test_data('test_data.json')
                         ], indirect=True )

async def test_context_precision(llm_wrapper, getData):
    # Create object of class for that specific metric 
    context_precision = LLMContextPrecisionWithoutReference(llm=llm_wrapper)
    # Score
    score = await context_precision.single_turn_ascore(getData)
    assert score >=0.75, f"Score is too low: {score}"
    print(score)


@pytest.fixture
def getData(request):

    test_data = request.param
    responseDict = get_llm_response(test_data['question'])

    # Feed data 
    sample = SingleTurnSample(
                user_input=test_data['question'],
                retrieved_contexts=[responseDict['retrieved_docs'][n]['page_content'] for n in responseDict['retrieved_docs']],
                reference=test_data['reference']
            )
    return sample 

