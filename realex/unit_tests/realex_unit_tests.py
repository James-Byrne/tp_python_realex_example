import unittest
from realex.realex import Realex


class RealexUnitTests(unittest.TestCase):
    def test_value_error_raised_when_realex_shared_secret_not_set(self):
        Realex.REALEX_SHARED_SECRET = None
        Realex.REALEX_URL = None
        Realex.REALEX_MERCHANT_ID = None
        with self.assertRaises(ValueError) as ve:
            Realex.create_charge(
                amount=100.00,
                currency='EUR',
                card_holder_name='Joe Blogs',
                card_number='4111 1111 1111 1111',
                cvv='333',
                expiry_month='09',
                expiry_year='2012',
                card_type='VISA',
            )
        self.assertEqual('REALEX_SHARED_SECRET must be configured', ve.exception.args[0])

    def test_value_error_raised_when_realex_url_not_set(self):
        Realex.REALEX_SHARED_SECRET = 'something'
        Realex.REALEX_URL = None
        Realex.REALEX_MERCHANT_ID = None
        with self.assertRaises(ValueError) as ve:
            Realex.create_charge(
                amount=100.00,
                currency='EUR',
                card_holder_name='Joe Blogs',
                card_number='4111 1111 1111 1111',
                cvv='333',
                expiry_month='09',
                expiry_year='2012',
                card_type='VISA',
            )
        self.assertEqual('REALEX_URL must be configured', ve.exception.args[0])

    def test_value_error_raised_when_realex_merchant_id_not_set(self):
        Realex.REALEX_SHARED_SECRET = 'something'
        Realex.REALEX_URL = 'something'
        Realex.REALEX_MERCHANT_ID = None
        with self.assertRaises(ValueError) as ve:
            Realex.create_charge(
                amount=100.00,
                currency='EUR',
                card_holder_name='Joe Blogs',
                card_number='4111 1111 1111 1111',
                cvv='333',
                expiry_month='09',
                expiry_year='2012',
                card_type='VISA',
            )
        self.assertEqual('REALEX_MERCHANT_ID must be configured', ve.exception.args[0])

if __name__ == '__main__':
    unittest.main()

