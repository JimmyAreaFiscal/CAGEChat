"""

This module is responsible for handling the subgraph uses for the answer generation.

The answer generation is done by the generate_answer node. However, it uses the main AgentState. 

In order to be able to use subgraph's states, we need to create an adapter for the main workflow state.
"""


from backend.modules.utils.schemas import AgentState, RetrievalState


def retrieval_qa_adapter(state: AgentState) -> AgentState:
    """
    This function is responsible for adapting the main workflow state to the retrieval workflow state, using the Retrieval


    """

    return state

