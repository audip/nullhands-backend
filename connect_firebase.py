from __future__ import print_function
from firebase import firebase

# Base cURL for reference
# curl -X POST -d '{"x":"100", "y":"100"}' 'https://camera-db.firebaseio.com/gyro.json?auth=1A1AEwbsKhtw6PJXmsPCAaXsfWt8QolDLDUuXXmy'
def connect_db():
    return firebase.FirebaseApplication('https://camera-db.firebaseio.com', None)

def fetch_data(collection, *args):
    firebase = connect_db()
    response = firebase.get('gyro', 'x')
    return response

def save_data(wink_data):
    firebase = connect_db()
    result = firebase.post('wink', wink_data)
    return result

def main():
    data = {'x', 'y'}
    # fetch_data('gyro', data)
    # sample = {'left':False, 'right':False}
    fetch_data('gyro')
    save_data(sample)

if __name__ == '__main__':
    main()
