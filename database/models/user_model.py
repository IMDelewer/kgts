from pydantic import BaseModel





class NewUser(BaseModel):

    username: str
    user_id: int

    phone_number: str | None = None

    first_name: str
    second_name: str | None = None

    access_lvl: int = 1

    


