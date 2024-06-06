import logging

from typing import Union

import project
from project.prompt_refiner_service import RefinePromptResponse
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

logger = logging.getLogger(__name__)


app = FastAPI(
    title="prompt refiner",
)


@app.post(
    "/refine-prompt", response_model=RefinePromptResponse
)
async def api_post_refine_prompt(
    prompt: str,
) -> Union[Response, RefinePromptResponse]:
    """
    Accepts a language model prompt from the user and returns a refined version.
    """
    try:
        res = await project.prompt_refiner_service.refine_prompt(prompt)
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
