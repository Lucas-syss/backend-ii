from pydantic import BaseModel

class PaymentRequest(BaseModel):
    user: str
    items:list[dict]
    payment_method:str
    payment_payload:dict