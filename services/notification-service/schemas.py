from pydantic import BaseModel

class NotificationCreate(BaseModel):
    user_id: int
    type: str
    title: str
    message: str