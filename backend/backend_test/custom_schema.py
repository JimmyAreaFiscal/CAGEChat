"""

This module is responsible for creating custom schemas for the test workflow

"""

from typing import TypedDict, Annotated
from langgraph.channels import LastValue
from ragas import SingleTurnSample

class TestState(TypedDict):
    question: Annotated[str, LastValue]
    reference: Annotated[str, LastValue]
    
    sample: Annotated[SingleTurnSample, LastValue]

    context_precision_score: Annotated[float, LastValue]
    context_entity_recall_score: Annotated[float, LastValue]
    faithfulness_score: Annotated[float, LastValue]
    response_relevancy_score: Annotated[float, LastValue]
    answer_relevancy_score: Annotated[float, LastValue]
    response_groundness_score: Annotated[float, LastValue]
    context_relevancy_score: Annotated[float, LastValue]
    answer_accuracy_score: Annotated[float, LastValue]
