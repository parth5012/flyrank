from pydantic import BaseModel, Field
from typing import Annotated, Literal

class ChatRequest(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=2000)]

class ChatResponse(BaseModel):
    category: Literal["billing","bug","feature","other"]
    urgency: Literal["high","normal","low"]
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    reason: Annotated[str, Field(min_length=1, max_length=256)]
