import os

from openai import OpenAI
from pydantic import BaseModel

from dotenv import load_dotenv
from project.prompts import gpt_4_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class RefinePromptResponse(BaseModel):
    """
    Returns the original and refined prompt alongside any pertinent metadata.
    """

    original_prompt: str
    refined_prompt: str
    refinement_status: str


async def refine_prompt(prompt: str) -> RefinePromptResponse:
    """
    Accepts a language model prompt from the user and returns a refined version. Utilizes the OpenAI API to process
    and refine the input prompt via GPT-4 with specific instructions for improvement.

    Args:
        prompt (str): The raw language model prompt input by the user for refinement.

    Returns:
        RefinePromptResponse: Returns the original and refined prompt alongside any pertinent metadata, including
        the success or failure status of the refinement process.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"{gpt_4_prompt}"},
                {"role": "system", "content": f"User's message: {prompt}"}
            ],
            temperature=0.5,
            max_tokens=2048
        )
        print(f"\n\nResponse is: {response}\n\n\n")
        refined_prompt = (
            response.choices[0].message.content.strip() if response.choices else ""
        )
        return RefinePromptResponse(
            original_prompt=prompt,
            refined_prompt=refined_prompt,
            refinement_status="COMPLETED" if refined_prompt else "FAILED",
        )
    except Exception as e:
        return RefinePromptResponse(
            original_prompt=prompt,
            refined_prompt="",
            refinement_status=f"FAILED due to an internal error: {e}",
        )
