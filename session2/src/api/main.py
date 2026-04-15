from fastapi import FastAPI
from models import PaymentRequest
from payments.adapter import PaymentBaseAdapter
from payments.factory import PaymentProviderFactory

app = FastAPI()


@app.post("/pay")
async def pay(payload: PaymentRequest):
    provider:PaymentBaseAdapter = PaymentProviderFactory(name=payload.payment_method) 
    await provider.pay(payload=payload.payment_payload)
    
    return 1