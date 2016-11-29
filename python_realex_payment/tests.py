import unittest
from django.test import Client


class RealexIntegrationTests(unittest.TestCase):
    def test_main_index_page_returns_status_code_200(self):
        self.assertEqual(Client().get('/').status_code, 200)

    def test_create_charge_of_success_with_http_status_code_of_200(self):
        response = self._invoke_post_request('250.00')
        self.assertEqual(200, response.status_code)
        self.assertEqual('SUCCESS', self.extract_response_content(response))

    def _invoke_post_request(self, amount):
        return Client().post('/donations', data=self.generate_dummy_data(amount=amount))

    @unittest.skip("Realex: Cent amount of .01 is incorrectly returning partial response ...")
    def test_create_3d_secure_verification_needed_with_status_code_of_200(self):
        response = self._invoke_post_request('250.01')
        self.assertEqual(200, response.status_code)
        self.assertEqual('100_3dsecure', self.extract_response_content(response))

    def test_create_declined_by_bank_with_status_code_of_200(self):
        response = self._invoke_post_request('250.10')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Bank Declined', self.extract_response_content(response))

    def test_create_transaction_declined_offline_with_status_code_of_200(self):
        response = self._invoke_post_request('250.11')
        self.assertEqual(200, response.status_code)
        self.assertEqual('DECLINED', self.extract_response_content(response))

    def test_create_card_reported_lost_or_stolen_with_status_code_of_200(self):
        response = self._invoke_post_request('250.12')
        self.assertEqual(200, response.status_code)
        self.assertEqual('DECLINED', self.extract_response_content(response))

    def test_create_fraud_checks_blocked_transaction_with_status_code_of_200(self):
        response = self._invoke_post_request('250.13')
        self.assertEqual(200, response.status_code)
        self.assertEqual('DECLINED', self.extract_response_content(response))

    def test_create_generic_error_600_with_status_code_of_200(self):
        response = self._invoke_post_request('250.14')
        self.assertEqual(200, response.status_code)
        self.assertEqual( 'ERROR', self.extract_response_content(response))

    def test_create_account_deactivated_status_code_of_200(self):
        response = self._invoke_post_request('250.15')
        self.assertEqual(200, response.status_code)
        self.assertEqual('ERROR', self.extract_response_content(response))

    def test_create_bank_communication_error_status_code_of_200(self):
        response = self._invoke_post_request('250.16')
        self.assertEqual(200, response.status_code)
        self.assertEqual('ERROR', self.extract_response_content(response))

    def test_create_card_and_currency_mismatch_status_code_of_200(self):
        response = self._invoke_post_request('250.17')
        self.assertEqual(200, response.status_code)
        self.assertEqual('CLIENT_DEACTIVATED', self.extract_response_content(response))

    def test_create_card_expired_status_code_of_200(self):
        response = self._invoke_post_request('250.23')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Card expiry date invalid', self.extract_response_content(response))

    def test_create_invalid_card_holder_name_status_code_of_200(self):
        response = self._invoke_post_request('250.24')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Invalid cardholder name', self.extract_response_content(response))

    def test_create_cvv_not_matched_status_code_of_200(self):
        response = self._invoke_post_request('250.30')
        self.assertEqual(200, response.status_code)
        self.assertEqual('CVV not matched', self.extract_response_content(response))

    def test_create_cvv_not_checked_status_code_of_200(self):
        response = self._invoke_post_request('250.31')
        self.assertEqual(200, response.status_code)
        self.assertEqual('CVV not checked due to circumstances', self.extract_response_content(response))

    def test_create_cvv_issuer_not_certified_status_code_of_200(self):
        response = self._invoke_post_request('250.32')
        self.assertEqual(200, response.status_code)
        self.assertEqual('CVV issuer not certified', self.extract_response_content(response))

    def test_create_cvv_not_processed_status_code_of_200(self):
        response = self._invoke_post_request('250.33')
        self.assertEqual(200, response.status_code)
        self.assertEqual('CVV not processed', self.extract_response_content(response))

    @unittest.skip("Throwing 500 error")
    def test_timeout_status_code_of_200(self):
        response = self._invoke_post_request('250.40')
        self.assertEqual(200, response.status_code)
        self.assertEqual('timeout', self.extract_response_content(response))

    @staticmethod
    def extract_response_content(response):
        return response.content.decode('utf-8')

    @staticmethod
    def generate_dummy_data(amount):
        return {'amount': amount,
                'currency': 'EUR',
                'card_holder_name': 'John Doe',
                'card_number': '4111 1111 1111 1111',
                'cvv': '333',
                'card_type': 'VISA',
                'expiry_month': '09',
                'expiry_year': '19'}

if __name__ == '__main__':
    unittest.main()
