from typing import Protocol

class PaymentBaseAdapter(Protocol):
    
    async def pay(self, payload:dict)->bool:
        ...