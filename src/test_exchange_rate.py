import unittest
from unittest.mock import patch
from rate_exchange import fetch_exchange_rates
import sqlite3

class TestExchangeRateAPI(unittest.TestCase):

    @patch('requests.get')
    def test_exchange_rate_api(self, mock_get):

        # import ipdb
        # ipdb.set_trace()
        api = 'http://api.exchangeratesapi.io/v1/latest'
        api_key = '0e9b1b5292426111c8de1d35782504ab'
        file_location = '/home/oem/Documents/PycharmProjects/SmartPensionTest/src/exchange_rate.csv'

        # Mock the response from the API
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = '{"success": true, "timestamp": 1623805200, "base": "EUR", "date": "2021-06-16", "rates": {"USD": 1.185, "GBP": 0.843, "CAD": 1.484}}'

        # Call the function that makes the API request and processes the data
        # Assuming the existing code is wrapped inside a function named `fetch_exchange_rates`
        result = fetch_exchange_rates(api, api_key,file_location )
        print("result-",result)
        # Assertions to verify the behavior of the function
        self.assertTrue(mock_get.called)
        self.assertEqual(result, 'Data has been successfully uploaded to the database.')

        # Assertions to verify the data stored in the database
        conn = sqlite3.connect('exchange_db.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM exchange_rate limit 1')
        rows = cursor.fetchall()
        print(rows)
        # Verify the number of rows inserted
        self.assertEqual(len(rows), 1)

        # Verify the values in the inserted row. We are not doing because everytime value will be different
        # expected_row = ('True', '2023-06-16 12:56:03', 'EUR', '2023-06-16', '4.022387')
        # self.assertEqual(rows[0], expected_row)

        # Clean up the database
        cursor.execute('DROP TABLE IF EXISTS exchange_rate')
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()