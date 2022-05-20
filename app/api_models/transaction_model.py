from pydantic import BaseModel
from datetime import datetime


class TransactionModel(BaseModel):
    id: int
    created_at: datetime
    status: int
    total: int
