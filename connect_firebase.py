from __future__ import print_function
from firebase import firebase
import requests

# Base cURL for reference
# curl -X POST -d '{"x":"100", "y":"100"}' 'https://camera-db.firebaseio.com/gyro.json?auth=1A1AEwbsKhtw6PJXmsPCAaXsfWt8QolDLDUuXXmy'
baseURL = 'https://camera-db.firebaseio.com'

def fetch_data(collection):
    firebase = requests.get('%s/%s.json' % (baseURL, collection))
    return firebase.json()

def save_data(wink_data):
    firebase = connect_db()
    result = firebase.post('wink', wink_data)
    return result

def main():
    print(fetch_data('gyro')['x'])


if __name__ == '__main__':
    main()
