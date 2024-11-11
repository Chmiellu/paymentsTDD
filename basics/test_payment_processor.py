import unittest
from unittest.mock import MagicMock
from payment_processor import PaymentProcessor, PaymentGateway, TransactionResult, TransactionStatus, NetworkException, PaymentException

class TestPaymentProcessor(unittest.TestCase):
    def setUp(self):
        self.gateway = MagicMock(spec=PaymentGateway)
        self.processor = PaymentProcessor(self.gateway)

    def test_process_payment_success(self):

        user_id = "userXD"
        amount = 123456.0
        transaction_id = "tranXD"
        self.gateway.charge.return_value = TransactionResult(True, transaction_id)

        result = self.processor.process_payment(user_id, amount)

        self.assertTrue(result.success)
        self.assertEqual(result.transaction_id, transaction_id)
        self.gateway.charge.assert_called_once_with(user_id, amount)


    def test_process_payment_insufficient_funds(self):

        user_id = "userXD"
        amount = 1000.0
        transaction_id = "tranXD"

        self.gateway.charge.return_value = TransactionResult(
            success=False,
            transaction_id=transaction_id,
            message="Insufficient funds"
        )

        result = self.processor.process_payment(user_id, amount)

        self.assertFalse(result.success)
        self.assertEqual(result.message, "Insufficient funds")
        self.gateway.charge.assert_called_once_with(user_id, amount)

