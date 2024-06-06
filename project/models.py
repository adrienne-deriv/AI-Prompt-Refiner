from pydantic import BaseModel


class RefinePromptResponse(BaseModel):
    """
    Returns the original and refined prompt alongside any pertinent metadata.
    """

    original_prompt: str
    refined_prompt: str
    refinement_status: str
