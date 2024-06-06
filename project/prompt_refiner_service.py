import os
import re
from typing import Optional, List

from openai import AsyncOpenAI

from dotenv import load_dotenv
from project.prompts import gpt_4_prompt, claude_3_prompt
from project.models import RefinePromptResponse

load_dotenv()


class PromptRefinerService:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def refine_prompt_gpt_4(self, prompt: str) -> RefinePromptResponse:
        """
        Accepts a language model prompt from the user and returns a refined version. Utilizes the OpenAI API to process
        and refine the input prompt via GPT-4 with specific instructions for improvement. This is Used with GPT-4

        Args:
            prompt (str): The raw language model prompt input by the user for refinement.

        Returns:
            RefinePromptResponse: Returns the original and refined prompt alongside any pertinent metadata, including
            the success or failure status of the refinement process.
        """
        try:
            response = await self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"{gpt_4_prompt}"},
                    {"role": "system", "content": f"User's message: {prompt}"}
                ],
                temperature=0.5,
                max_tokens=2048
            )

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

    async def refine_prompt_claude_3(self, prompt: str, variables: Optional[List]) -> RefinePromptResponse:
        """
        Accepts a language model prompt from the user and returns a refined version. Utilizes the OpenAI API to precess
        and refine the input prompt via GPT-4o with specific instructions for improvements. This prompt is to be used
        to prompt Claude Models

        Args:
            :param prompt: (str): The raw language model prompt input by the user for refinement.
            :param variables: (list): The List of variables that AI has to insert in the application

        Returns:
            RefinePromptResponse: Returns the original and refined prompt alongside any pertinent metadata, including
            the success or failure status of the refinement process.

        """
        try:
            variable_string = ""
            for variable in variables:
                variable_string += "\n{$" + variable.upper() + "}"

            metaprompt = claude_3_prompt.replace("{{TASK}}", prompt)
            assistant_partial = "<INPUTS>"
            if variable_string:
                assistant_partial += variable_string + "\n</Inputs>\n<Instructions Structure>"

            response = await self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": metaprompt},
                    {"role": "assistant", "content": assistant_partial}
                ],
                temperature=0.5,
                max_tokens=2048
            )
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

    def extract_between_tags(self, tag: str, string: str, strip: bool = False) -> List[str]:
        ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
        if strip:
            ext_list = [e.strip() for e in ext_list]
        return ext_list

    def remove_empty_tags(self, text):
        return re.sub(r'\n<(\w+)>\s*</\1>\n', '', text, flags=re.DOTALL)

    def strip_last_sentence(self, text):
        sentences = text.split('. ')
        if sentences[-1].startswith("Let me know"):
            sentences = sentences[:-1]
            result = '. '.join(sentences)
            if result and not result.endswith('.'):
                result += '.'
            return result
        else:
            return text

    def extract_prompt(self, metaprompt_response):
        between_tags = self.extract_between_tags("Instructions", metaprompt_response)[0]
        return between_tags[:1000] + self.strip_last_sentence(
            self.remove_empty_tags(self.remove_empty_tags(between_tags[1000:]).strip()).strip())

    def extract_variables(self, prompt):
        pattern = r'{([^}]+)}'
        variables = re.findall(pattern, prompt)
        return set(variables)
