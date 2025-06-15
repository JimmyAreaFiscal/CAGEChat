"""

This file contains the test pipeline for the CAGEChat backend system.

It uses the modules of the CAGEChat backend to rebuild the graph and add it into a LangGraph test workflow.
Inside the test workflow, it adds N nodes based on the amount of test classes. 

"""
import asyncio
import json
import random
import sys, os

# Add the CAGEChat directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Adding backend diretory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))



from config import Settings, settings
from modules.graphs.graph_builder import chat_workflow_builder
from modules.utils.general_utils import config_nodes

from modules.utils.schemas import AgentState
from backend_test.custom_schema import TestState

from langgraph.graph import StateGraph, END 

from langchain_core.messages import HumanMessage
from ragas import SingleTurnSample
from uuid import uuid4
message = "Quais são os procedimentos administrativos no Estado do Rio Grande do Sul?"

from backend_test.evaluation_modules.context_precision import evaluate_context_precision
from backend_test.evaluation_modules.context_entity_recall import evaluate_context_entity_recall
from backend_test.evaluation_modules.faithfulness import evaluate_faithfulness
from backend_test.evaluation_modules.response_relevancy import evaluate_response_relevancy
from backend_test.evaluation_modules.response_groundedness import evaluate_response_groundness
from backend_test.evaluation_modules.answer_accuracy import evaluate_answer_accuracy
from backend_test.evaluation_modules.context_relevance import evaluate_context_relevancy





async def aggregate_scores(state: TestState) -> TestState:
    """
    This function is responsible for aggregating the scores of the test
    """
    return state


def test_workflow_builder(config: Settings = settings, workflow: StateGraph = chat_workflow_builder().compile()) -> StateGraph:
    """
    This workflow is responsible for building a offline test workflow for CAGEChat Webservice backend system

    Optionally accepts a Settings parameter to allow configuration of LLMs and other components.
    
            ...
    """
    # Generating the answer from the chat workflow
    async def retrieve_chat_answer(state: TestState) -> TestState:
        """
        This function is responsible for retrieving the chat answer from the chat workflow

        This should use the same AgentState as the main component of the CAGEChat backend
        """
        thread_id = "123"
        config = {"configurable": {'thread_id': thread_id}}
        response = await workflow.ainvoke(
            {"question": HumanMessage(content=state['question'])},
            config=config
        )

        sample = SingleTurnSample(
            user_input=state['question'],
            response=response['messages'][-1].content,
            retrieved_contexts=[response['retrieved_documents'][n].page_content for n in range(len(response['retrieved_documents']))],
            reference=state['reference'], 
        )
        state['sample'] = sample
        

        return state

    # Building the test workflow
    test_workflow_builder = StateGraph(TestState)

    # Retrieving the chat answer
    test_workflow_builder.add_node("retrieve_chat_answer", retrieve_chat_answer)
    
    # Applying the evaluations
    test_workflow_builder.add_node("evaluate_context_precision", evaluate_context_precision)
    test_workflow_builder.add_node("evaluate_faithfulness", evaluate_faithfulness)
    test_workflow_builder.add_node("evaluate_response_relevancy", evaluate_response_relevancy)
    test_workflow_builder.add_node("evaluate_response_groundness", evaluate_response_groundness)
    test_workflow_builder.add_node("evaluate_answer_accuracy", evaluate_answer_accuracy)
    test_workflow_builder.add_node("evaluate_context_relevancy", evaluate_context_relevancy)
    test_workflow_builder.add_node("aggregate_scores", aggregate_scores)

    # Adding the edges
    test_workflow_builder.add_edge("retrieve_chat_answer", "evaluate_context_precision")
    test_workflow_builder.add_edge("retrieve_chat_answer", "evaluate_faithfulness")
    test_workflow_builder.add_edge("retrieve_chat_answer", "evaluate_response_relevancy")
    test_workflow_builder.add_edge("retrieve_chat_answer", "evaluate_response_groundness")
    test_workflow_builder.add_edge("retrieve_chat_answer", "evaluate_answer_accuracy")
    test_workflow_builder.add_edge("retrieve_chat_answer", "evaluate_context_relevancy")

    test_workflow_builder.add_edge("evaluate_context_precision", "aggregate_scores")
    test_workflow_builder.add_edge("evaluate_faithfulness", "aggregate_scores")
    test_workflow_builder.add_edge("evaluate_response_relevancy", "aggregate_scores")
    test_workflow_builder.add_edge("evaluate_response_groundness", "aggregate_scores")
    test_workflow_builder.add_edge("evaluate_answer_accuracy", "aggregate_scores")
    test_workflow_builder.add_edge("evaluate_context_relevancy", "aggregate_scores")


    test_workflow_builder.add_edge("aggregate_scores", END)

    test_workflow_builder.set_entry_point("retrieve_chat_answer")



    return test_workflow_builder



async def execute_test_pipeline(folder_path: str, amount_of_test_cases: int = 10):
    test_workflow = test_workflow_builder().compile() 

    scores = {
        "question": [],
        "reference": [],
        "retrieved_contexts": [],
        "context_precision": [],
        "faithfulness": [],
        "response_relevancy": [],
        "response_groundness": [],
        "answer_accuracy": [],
        "context_relevancy": []
    }

    list_of_test_files = os.listdir(folder_path)
    test_data = []
    for test_file in list_of_test_files:
        chunk = json.load(open(os.path.join(folder_path, test_file)))

        if isinstance(chunk, list):
            test_data.extend(chunk)
        else:
            test_data.append(chunk)
    
    random_sample = random.sample(test_data, amount_of_test_cases)
    if random_sample:
        for test_case in random_sample:
            scores["question"].append(test_case["question"])
            scores["reference"].append(test_case["reference"])
            
            try:
                response = await test_workflow.ainvoke({"question": test_case["question"], "reference": test_case["reference"]})
                scores["retrieved_contexts"].append(response["retrieved_documents"])
                scores["context_precision"].append(response["context_precision"])
                scores["faithfulness"].append(response["faithfulness"])
                scores["response_relevancy"].append(response["response_relevancy"])
                scores["response_groundness"].append(response["response_groundness"])
                scores["answer_accuracy"].append(response["answer_accuracy"])
                scores["context_relevancy"].append(response["context_relevancy"])
            except Exception as e:
                print(f"Error on test case {test_case['question']}: {e}")
                continue
            
    return scores 


if __name__ == "__main__":
    scores = asyncio.run(execute_test_pipeline())
    print(scores)
            
            
        
        
    
    
    


