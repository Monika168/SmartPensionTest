import requests
import pandas as pd
import csv
import sqlite3
import json


def fetch_exchange_rates(api, api_key, file_location):
    '''
    Below commented code will give expected result, however coudn't use it as it's paid.
    '''
    # api = 'http://api.exchangeratesapi.io/v1/timeseries'
    # start_date =  '2021-01-01'
    # end_date = '2023-01-01'
    # base = ['GBP','USD','EUR']
    # json_resp = []

    # for i in range(len(base)):
    #     response = requests.get(api+'?access_key='+api_key+'&start_date='+start_date+'&end_date='+end_date+'&base='+ base[i])
    #     if response.status_code == 200:
    #         try:
    #             json_resp.extend(response.json())

    #         except json.JSONDecodeError as e:
    #             print(f"Error decoding JSON: {e}")
    #     else:
    #         print(f"Error: {response.status_code}")

    response = requests.get(api + '?access_key=' + api_key)
    print(response)
    if response.status_code == 200:
        print('200')
        try:
            # json_resp = response.json()
            json_resp = response.text
            headers = ['success', 'timestamp', 'base', 'date', 'rates']

            df = pd.read_json(json_resp)
            # print(df)
            df.to_csv(r"/home/oem/Documents/PycharmProjects/SmartPensionTest/src/exchange_rate.csv",
                      encoding='utf-8', index=False)

            # Upload CSV file to SQLite database
            database_file = 'exchange_db.db'
            table_name = 'exchange_rate'

            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            headers = ['success', 'timestamp', 'base', 'date', 'rates']
            create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(headers)})'
            cursor.execute(create_table_query)

            with open(file_location, 'r') as file:
                csv_data = csv.reader(file)
                next(csv_data)  # Skip the header row
                cursor.executemany(f'INSERT INTO {table_name} VALUES ({", ".join(["?"] * len(headers))})', csv_data)

            conn.commit()
            conn.close()

            return ('Data has been successfully uploaded to the database.')

        except json.JSONDecodeError as e:
            return (f"Error decoding JSON: {e}")

        except requests.exceptions.RequestException as e:
            # Handle any network-related exceptions
            return ("Error occurred during the request:", e)

        except requests.exceptions.HTTPError as e:
            # Handle HTTP error (status code 4xx or 5xx)
            return ("HTTP error occurred:", e)

        except ValueError as e:
            # Handle JSON decoding error
            return ("Error occurred while decoding JSON response:", e)

        except Exception as e:
            # Handle any other exceptions that might occur
            return ("An error occurred:", e)
    else:
        return (f"Error: {response.status_code}")


def main():
    api = 'http://api.exchangeratesapi.io/v1/latest'
    api_key = '0e9b1b5292426111c8de1d35782504ab'
    file_location = r"/home/oem/Documents/PycharmProjects/SmartPensionTest/src/exchange_rate.csv"

    print(fetch_exchange_rates(api, api_key, file_location))


if __name__ == '__main__':
    main()

