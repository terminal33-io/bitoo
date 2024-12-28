from datetime import datetime

from pydantic import BaseModel, field_validator


class StreamRequest(BaseModel):
    question: str