from pydantic import BaseModel
from typing import List




class NewSupport(BaseModel):

    request: str
    status: str = 'opened'
    support_name: str | None = None

    userid: int
    operid: int = 0
    
    rate: int = 0

    cancels: int = 0
    cancel_ids: list[int] = []
