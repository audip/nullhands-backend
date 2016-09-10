from __future__ import print_function
from firebase import firebase
import requests, time, json

# Base cURL for reference
# curl -X POST -d '{"x":"100", "y":"100"}' 'https://camera-db.firebaseio.com/gyro.json?auth=1A1AEwbsKhtw6PJXmsPCAaXsfWt8QolDLDUuXXmy'
baseURL = 'https://camera-db.firebaseio.com'

def fetch_data(collection):
    current_limit, i = 500, 0
    while(i < current_limit):
        firebase = requests.get('%s/%s.json?limit' % (baseURL, collection))
        time.sleep(0.5)
    return firebase.json()

def save_data(collection):
    wink_data = {'left':'false', 'right':'false'}
    url = 'https://camera-db.firebaseio.com/wink.json'
    result = requests.put(url, data=json.dumps(wink_data))
    return result

def main():
    # print(fetch_data('gyro')['x'])
    print(save_data('wink', sample))


if __name__ == '__main__':
    main()
