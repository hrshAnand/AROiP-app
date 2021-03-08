#!/usr/bin/env python

import socket
import time
import os
import ntplib

class Client:

    def start(self):
        
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        SLEEP_TIME = 2

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))

        fileName = "latencyAdminTCP.txt"
        f = open(fileName, 'w')
        try:
            while True:
                client_time = time.time()
                MESSAGE = "" + str(client_time) + ":" + "Data"
                s.send(MESSAGE.encode("utf8"))
                data = s.recv(1024)
                t = float(data.split(":")[0])
                curr_time = time.time()
                line = str(curr_time - client_time) + " " + str(curr_time - t) + " " + str(t - client_time) + "\n"
                print(line)
                f.write(line)
                time.sleep(SLEEP_TIME)


        except KeyboardInterrupt:
            f.close()
            s.close() # On pressing ctrl + c, we close all connections
            quit() # Then we shut down the server


if __name__ == '__main__':
    try:
        client = ntplib.NTPClient()
        response = client.request('in.pool.ntp.org')
        os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
    except:
        print('Could not sync with time server.')
    client = Client()
    client.start()