from pydantic import BaseModel


class InvocationRequest(BaseModel):
    identifier: str
