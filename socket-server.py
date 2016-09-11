import socket
import requests
import json

class Storage(object):
    def __init__(self, raw_data=None):
        self.base_parser(raw_data)
        self.gyro = ""
        self.wink = ""
        self.speech = ""
        self.loc = ""

    def base_parser(self, raw_data=None):
        if raw_data == None:
            return
        break_point = raw_data.index(':')
        list_type, string_data = raw_data[:break_point], raw_data[break_point+1:]
        self.list_type = string_data

    # def parse_data(self, list_type, data):
    #     # Sample: gyro: x=120, y=100
    #     temp_set = data.strip().split(',')
    #     new_dict = {}
    #     for itemset in temp_set:
    #         key, value = [str(item) for item in itemset.split('=')]
    #         new_dict[key] = value
    #     return new_dict
    #
    #
    # def parse_speech(self, list_type, data):
    #     # Sample: "speech: alexa this is a test string!"
    #     new_dict = {}
    #     string_data = data.strip().split(' ')
    #     power_word = string_data[0]
    #     club_string = " ".join(string_data[i] for i in range(1, len(string_data)))
    #     new_dict[power_word] = club_string
    #     return new_dict

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def socket_main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # serversocket = socket.socket()
    # host = socket.gethostbyname(socket.getfqdn())
    host = ''
    server_ip = socket.gethostbyname(socket.gethostname())
    payload = {'ip': server_ip}
    requests.put('https://camera-db.firebaseio.com/server.json', data=json.dumps(payload))
    print payload
    port = 25000

    if host == "127.0.1.1":
        import commands
        host = commands.getoutput("hostname -I")
    print "host = " + host

    #Prevent socket.error: [Errno 98] Address already in use
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serversocket.bind((host, port))
    serversocket.listen(10)
    # s = Storage("speech: Alexa This is a text string")
    c, addr = serversocket.accept()
    try:
        while True:
            data = c.recv(1024)
            data = data.replace("\r\n", '') #remove new line character
            inputStr = "Received " + data + " from " + addr[0]
            print data
            s = Storage(data)
            # print inputStr
            c.send("Hello from python server!\nYou sent: " + data + "\nfrom: " + addr[0] + "\n")

            if data == "Quit": break
        c.send("Server stopped\n")
        print "Server stopped"
        c.close()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    socket_main()
