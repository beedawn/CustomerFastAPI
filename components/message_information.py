from pydantic import BaseModel


class MessageInformation(BaseModel):
    source: str  # required
