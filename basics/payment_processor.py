import logging
from enum import Enum


logging.basicConfig(level=logging.INFO)

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
            if result.success:
                logging.info(f"Payment processed successfully for user {user_id}. Transaction ID: {result.transaction_id}")
            else:
                logging.warning(f"Payment failed for user {user_id}. Reason: {result.message}")
            return result
        except (NetworkException, PaymentException) as e:
            logging.error(f"Error processing payment for user {user_id}: {e}")
            return TransactionResult(False, "", str(e))

    def refund_payment(self, transaction_id: str) -> TransactionResult:
        if not transaction_id:
            raise ValueError("Invalid transaction_id")

        try:
            result = self.gateway.refund(transaction_id)
            if result.success:
                logging.info(f"Refund processed successfully for transaction ID: {transaction_id}")
            else:
                logging.warning(f"Refund failed for transaction ID: {transaction_id}. Reason: {result.message}")
            return result
        except (RefundException, NetworkException) as e:
            logging.error(f"Error processing refund for transaction ID {transaction_id}: {e}")
            return TransactionResult(False, transaction_id, str(e))

    def get_payment_status(self, transaction_id: str) -> TransactionStatus:
        if not transaction_id:
            raise ValueError("Invalid transaction_id")

        try:
            status = self.gateway.get_status(transaction_id)
            logging.info(f"Payment status for transaction ID {transaction_id}: {status.value}")
            return status
        except NetworkException as e:
            logging.error(f"Error retrieving payment status for transaction ID {transaction_id}: {e}")
            return TransactionStatus.FAILED
