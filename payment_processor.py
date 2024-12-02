"""
This module defines classes and methods for processing payments and refunds
using a PaymentGateway interface.

It handles transactions, retrieves their statuses, and logs the operations.
"""

import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)

class TransactionStatus(Enum):
    """Enum representing the possible statuses of a transaction."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TransactionResult:
    """
    Represents the result of a transaction.

    Attributes:
        success (bool): Whether the transaction was successful.
        transaction_id (str): The ID of the transaction.
        message (str): Additional message or error details.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, success: bool, transaction_id: str, message: str = ""):
        self.success = success
        self.transaction_id = transaction_id
        self.message = message

class NetworkException(Exception):
    """Exception raised for network-related errors."""

class PaymentException(Exception):
    """Exception raised for payment processing errors."""

class RefundException(Exception):
    """Exception raised for refund processing errors."""

class PaymentGateway:
    """Interface for implementing payment gateway operations."""
    def charge(self, user_id: str, amount: float):
        """Charge a user with the specified amount."""
        raise NotImplementedError("This method should be implemented by subclasses")

    def refund(self, transaction_id: str):
        """Refund a transaction based on its ID."""
        raise NotImplementedError("This method should be implemented by subclasses")

    def get_status(self, transaction_id: str):
        """Retrieve the status of a transaction."""
        raise NotImplementedError("This method should be implemented by subclasses")

class PaymentProcessor:
    """
    Handles payment and refund operations using a PaymentGateway instance.

    Attributes:
        gateway (PaymentGateway): The payment gateway to process transactions.
    """
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def process_payment(self, user_id: str, amount: float) -> TransactionResult:
        """
        Process a payment for a user.

        Args:
            user_id (str): The ID of the user making the payment.
            amount (float): The payment amount.

        Returns:
            TransactionResult: The result of the payment transaction.
        """
        if not user_id or amount <= 0:
            raise ValueError("Invalid user_id or amount")

        try:
            result = self.gateway.charge(user_id, amount)
            if result.success:
                logging.info(
                    "Payment processed successfully for user %s. Transaction ID: %s",
                    user_id, result.transaction_id
                )
            else:
                logging.warning(
                    "Payment failed for user %s. Reason: %s",
                    user_id, result.message
                )
            return result
        except (NetworkException, PaymentException) as e:
            logging.error(
                "Error processing payment for user %s: %s", user_id, str(e)
            )
            return TransactionResult(False, "", str(e))

    def refund_payment(self, transaction_id: str) -> TransactionResult:
        """
        Process a refund for a transaction.

        Args:
            transaction_id (str): The ID of the transaction to refund.

        Returns:
            TransactionResult: The result of the refund transaction.
        """
        if not transaction_id:
            raise ValueError("Invalid transaction_id")

        try:
            result = self.gateway.refund(transaction_id)
            if result.success:
                logging.info(
                    "Refund processed successfully for transaction ID: %s",
                    transaction_id
                )
            else:
                logging.warning(
                    "Refund failed for transaction ID: %s. Reason: %s",
                    transaction_id, result.message
                )
            return result
        except (RefundException, NetworkException) as e:
            logging.error(
                "Error processing refund for transaction ID %s: %s",
                transaction_id, str(e)
            )
            return TransactionResult(False, transaction_id, str(e))

    def get_payment_status(self, transaction_id: str) -> TransactionStatus:
        """
        Retrieve the status of a transaction.

        Args:
            transaction_id (str): The ID of the transaction.

        Returns:
            TransactionStatus: The status of the transaction.
        """
        if not transaction_id:
            raise ValueError("Invalid transaction_id")

        try:
            status = self.gateway.get_status(transaction_id)
            logging.info(
                "Payment status for transaction ID %s: %s",
                transaction_id, status.value
            )
            return status
        except NetworkException as e:
            logging.error(
                "Error retrieving payment status for transaction ID %s: %s",
                transaction_id, str(e)
            )
            return TransactionStatus.FAILED
