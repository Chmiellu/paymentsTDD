from enum import Enum

class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TransactionResult:
    def __init__(self, success: bool, transaction_id: str, message: str = ""):
        self.success = success
        self.transaction_id = transaction_id
        self.message = message

class NetworkException(Exception):
    pass

class PaymentException(Exception):
    pass

class RefundException(Exception):
    pass


class PaymentGateway:
    def charge(self, user_id: str, amount: float) -> TransactionResult:
        raise NotImplementedError("This method should be implemented by subclasses")

    def refund(self, transaction_id: str) -> TransactionResult:
        raise NotImplementedError("This method should be implemented by subclasses")

    def get_status(self, transaction_id: str) -> TransactionStatus:
        raise NotImplementedError("This method should be implemented by subclasses")


class PaymentProcessor:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def process_payment(self, user_id: str, amount: float) -> TransactionResult:
        if not user_id or amount <= 0:
            raise ValueError("Invalid user_id or amount")

        try:
            result = self.gateway.charge(user_id, amount)
            return result
        except (NetworkException, PaymentException) as e:
            print(f"Error processing payment: {e}")
            return TransactionResult(False, "", str(e))

    def refund_payment(self, transaction_id: str) -> TransactionResult:
        pass

    def get_payment_status(self, transaction_id: str) -> TransactionStatus:
        pass



