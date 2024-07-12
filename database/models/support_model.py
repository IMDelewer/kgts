from pydantic import BaseModel
from typing import List




class NewSupport(BaseModel):

    request: str
    status: str
    support_name: str

    userid: int
    operid: int
    
    rate: int

    cancels: int
    cancel_ids: List[int]
