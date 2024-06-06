from typing import Optional, List
from pydantic import BaseModel


class RequestDto(BaseModel):
    prompt: str
    variables: Optional[List[str]] = None
