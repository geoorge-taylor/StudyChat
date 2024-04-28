import json
import logging
import socket
import threading
from typing import Any

from networking.crypto_utils import CryptoUtils, KeyType
from static.shared_types import *


# Used to connect to the server socket and receive commands
class ClientSocket:
    def __init__(self, port: int, format: str, backlog: int, 
                 header_size: int, client_private_key_path: str, 
                 server_public_key_path: str, recv_callback: Any,
                 connect_to_server: bool = True) -> None:
        
        # Initiate private and public key path attributes
        self.__server_public_key = CryptoUtils.load_key_from_file(server_public_key_path, KeyType.PUBLIC)
        self.__client_private_key = CryptoUtils.load_key_from_file(client_private_key_path, KeyType.PRIVATE)

        # Initiate socket settings
        self.port = port
        self.format = format
        self.backlog = backlog
        self.header_size = header_size
        self.connected = bool()
        self.recv_callback = recv_callback

        # Start the socket if connect to server is true
        if connect_to_server: 
            self.initiate_socket()
     

    def initiate_socket(self) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = (socket.gethostname(), self.port)
        self.start_socket()


    def start_socket(self) -> None:
        try:
            self.__socket.connect(self.__address)
            self.__debug(f'connected to {self.__address}')
            self.connected = True
            threading.Thread(target=self.listen_for_commands).start()
    
        except socket.error as err:
            self.__debug(err.strerror)
            self.close()


    def listen_for_commands(self) -> None:
        while self.connected:
            try:
                header = self.__socket.recv(self.header_size)
                if not header: 
                    raise(socket.error)
                
                data_length = int.from_bytes(header, byteorder='big')
                encrypted_command = self.__socket.recv(data_length)
                if encrypted_command: self.receive_command(encrypted_command)

            except (socket.error, json.JSONDecodeError) as err:
                self.__debug(err)
                self.close()


    def receive_command(self, encrypted_command: bytes) -> None:
        decrypted_message = CryptoUtils.decrypt_data(encrypted_command, self.__client_private_key)
        if decrypted_message is None: self.__debug(f'could not decrypt: {encrypted_command}'); return
        json_command = decrypted_message.decode()
        raw_command: SocketCommand = json.loads(json_command)
        self.__debug(f'command from server: {raw_command}')
        self.recv_callback(raw_command)


    def send_command(self, command: SocketCommand) -> None:
        if self.connected:
            json_command = json.dumps(command)
            encrypted_command = CryptoUtils.encrypt_data(json_command.encode(), self.__server_public_key)
            if not encrypted_command: self.__debug(f'Command too large: {json_command}'); return
            header = len(encrypted_command).to_bytes(self.header_size, byteorder='big')
            self.__socket.sendall(header + encrypted_command) 
            self.__debug(f'to server: {json_command}')


    def close(self) -> None:
        self.connected = False
        self.__socket.close()

            
    def __debug(self, message) -> None:
        logging.debug(f'[client] {message}')
