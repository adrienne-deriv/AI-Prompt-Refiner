import logging

from typing import Union, Annotated, Optional, List

from project.prompt_refiner_service import PromptRefinerService
from project.models import RefinePromptResponse
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

logger = logging.getLogger(__name__)

app = FastAPI(
    title="prompt refiner",
)


@app.post(
    "/refine-gpt-prompt", response_model=RefinePromptResponse
)
async def api_post_refine_prompt(
        service: Annotated[PromptRefinerService, Depends()],
        prompt: str,
) -> Union[Response, RefinePromptResponse]:
    """
    Accepts a language model prompt from the user and returns a refined version.
    """
    try:
        res = await service.refine_prompt_gpt_4(prompt)
        logging.info(f"Response: {res}")
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/refine-claude-prompt", response_model=RefinePromptResponse
)
async def refine_prompt_claude(
        service: Annotated[PromptRefinerService, Depends()],
        prompt: str,
        variables: Optional[List[str]] = None
) -> Union[Response, RefinePromptResponse]:
    """
    Accepts a language model prompt from the user and returns a refined version.
    """
    try:
        res = await service.refine_prompt_claude_3(prompt=prompt, variables=variables)
        logging.info(f"Response: {res}")
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/refine-gemini-prompt", response_model=RefinePromptResponse
)
async def refine_prompt_claude(
        service: Annotated[PromptRefinerService, Depends()],
        prompt: str,
) -> Union[Response, RefinePromptResponse]:
    """
    Accepts a language model prompt from the user and returns a refined version.
    """
    try:
        res = await service.refine_prompt_gemini(prompt=prompt)
        logging.info(f"Response: {res}")
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )