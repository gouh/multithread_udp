#!/usr/bin/env python3

import sys
import socket
from time import sleep

PORT = 80
PACKET_TYPE=0
HOST = sys.argv[1] 
TOTAL_PACKETS = int(sys.argv[2])
MESSAGE_CLIENT = sys.argv[3]

client_socket = None
success_reply=[]
error_reply=[]

def print_result():
    print(f'{TOTAL_PACKETS} transmitidos, {len(success_reply)} recibidos, {len(error_reply)} con error')
    print('========================================')
    print(f'> {len(success_reply)} Paquetes recibidos')
    print(*success_reply, sep='\n- ')
    print(f'\n> {len(error_reply)} Paquetes con error')
    print(*error_reply, sep='\n- ')
    print('========================================')

def create_packet(seq, message, packet_type=PACKET_TYPE):
    packet = f'type={packet_type};seq={seq};message={message}'
    return packet.encode('utf-8')

def check_bytes():
    bytes_packages=len(str(TOTAL_PACKETS).encode('utf-8'))
    bytes_message=len(MESSAGE_CLIENT.encode('utf-8'))
    
    if(bytes_packages > 2):
        raise Exception(f'Su secuencia de paquetes supera el número de bytes establecido (2bytes)')

    if(bytes_message > 40):
        raise Exception(f'Su mensaje supera el número de bytes establecido(40 bytes)') 
    
    print(f'Paquetes a enviar en bytes: {bytes_packages}')
    print(f'Mensaje a enviar  en bytes: {bytes_message}')

def main():
    try:
        check_bytes()
    except Exception as e:
        print(e)
        sys.exit()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(0.4)
    
    for seq in range(TOTAL_PACKETS):
        packet = create_packet(seq+1, MESSAGE_CLIENT)
        client_socket.sendto(packet, (HOST, PORT))

        try:
            data, server_addr = client_socket.recvfrom(1024)
            if(seq==0):
                print(f'> {HOST} dice: {data.decode("utf-8")}')
                sys.stdout.flush()
            success_reply.append(data.decode('utf-8'))
        except socket.timeout:
            packet = create_packet(seq+1, MESSAGE_CLIENT, 2)
            error_reply.append(packet.decode('utf-8'))
            continue

        sleep(0.2)

    print_result()

main()