#!/usr/bin/env python3

import socketserver
import sys
import time

PACKET_TYPE=1
PORT = 80
HOST = '0.0.0.0'

class RequestHandler(socketserver.BaseRequestHandler):

    seq=0
    client_message=''
    gretting='Hola desde el servidor'

    def get_values_packet(self, client_message_protocol):
        split_message=client_message_protocol.split(sep=';')
        seq=split_message[1].split(sep='=')[1]
        client_message=split_message[2].split(sep='=')[1]

        self.seq=int(seq)
        self.client_message=client_message

    def print_message_client(self, client_address):
        client_ip = str(client_address[0])
        if(self.seq==1):
            print('Nuevo mensaje recibido de ' + client_ip)
            print('> ' + client_ip + ' dice: ' + self.client_message)
            print('========================================')
            sys.stdout.flush()

    def create_packet(self):
        packet = f'type={PACKET_TYPE};seq={self.seq};message={self.gretting}'
        return packet.encode('utf-8')

    def reply(self, server):
        if((self.seq%2)==0):
            time.sleep(500)
        server.sendto(self.create_packet(), self.client_address)

    def handle(self):
        data,server=self.request
        client_message_protocol=data.decode('utf-8')

        self.get_values_packet(client_message_protocol)
        self.print_message_client(self.client_address)
        self.reply(server)

s = socketserver.ThreadingUDPServer((HOST, PORT), RequestHandler, bind_and_activate=True)
s.serve_forever()