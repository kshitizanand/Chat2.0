from pydantic import BaseModel

class Message(BaseModel):
    query: str
    reply: str

class Conversation(BaseModel):
    content: list[Message]