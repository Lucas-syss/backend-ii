

from typing import Callable

from payments.adapter import PaymentBaseAdapter
from payments.providers import MBWayPayment, Paypalpayment


class PaymentProviderFactory:
    REGISTRY:dict[str, Callable] = {
        "mbway": MBWayPayment,
        "paypal": Paypalpayment
    }
    
    def get_provider(self, name:str)->PaymentBaseAdapter:
        
        provider = self.REGISTRY.get(name,None)
        
        if not provider:
            raise ValueError("Method not supported")
        
        return provider()    
    