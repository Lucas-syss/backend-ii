from payments.adapter import PaymentBaseAdapter


class MBWayPayment(PaymentBaseAdapter):
    
    async def pay(self, payload:dict)->bool:
        print("MBway payment successful")
        return True
    
    
class Paypalpayment(PaymentBaseAdapter):
    
    async def pay(self, payload:dict)->bool:
        print("Paypal payment successful")
        return True