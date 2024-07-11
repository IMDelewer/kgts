from pydantic import BaseModel





class user(BaseModel):

    _id: int

    username: str
    user_id: int

    phone_number: str = None

    first_name: str
    second_name: str

    acces_lvl: int = 0

    



