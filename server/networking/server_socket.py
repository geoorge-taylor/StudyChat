import json
import logging
import socket
import threading
from typing import Any, Union

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from networking.crypto_utils import CryptoUtils, KeyType
from static.commands import *
from static.shared_types import SocketCommand, UserDetails


class ServerSocket:
    def __init__(self, server_private_key_path: str, client_public_key_path: str, 
                 port: int, format: str, backlog: int, header_size: int, recv_callback: Any,
                 user_disconnect_callback: Any) -> None:
        
        # Initiate attributes
        self.backlog = backlog
        self.port = port
        self.format = format
        self.header_size = header_size

        # Load the keys for encryption 
        self.__client_public_key: RSAPublicKey = CryptoUtils.load_key_from_file(client_public_key_path, KeyType.PUBLIC)
        self.__server_private_key: RSAPrivateKey = CryptoUtils.load_key_from_file(server_private_key_path, KeyType.PRIVATE)

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__address = (socket.gethostname(), port)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.recv_callback = recv_callback
        self.user_disconnect_callback = user_disconnect_callback
        self.user_connections: dict[tuple, User] = dict()
        self.initiate_socket()


    def initiate_socket(self) -> None:
        try:
            self.__socket.bind(self.__address)
            self.__socket.listen(self.backlog)
            self.__debug(f"listening on port {self.port}")
            threading.Thread(target=self.listen_for_connections).start()

        except socket.error as err:
            self.__debug(err.strerror)
            self.__socket.close()


    def listen_for_connections(self) -> None:
        while True:
            try:
                connection, address = self.__socket.accept()
                user = User(
                    address=address,
                    header_size=self.header_size,
                    client_public_key=self.__client_public_key,
                    server_private_key=self.__server_private_key,
                    client_socket=connection,
                    close_callback=self.close_connection,
                    recv_callback=self.recv_callback,
                )
                user.start()
                self.user_connections[address] = user
                self.__debug(f"current connections: {threading.active_count()-2}")

            except socket.error as err:
                self.__debug(err.strerror)


    def close_connection(self, address: tuple) -> None:
        user = self.user_connections.get(address)
        self.user_disconnect_callback(user)
        self.user_connections.pop(address)


    def __debug(self, message: str) -> None:
        logging.debug(f"[server socket]: {message}")



class User(threading.Thread):
    def __init__(self, header_size: int, address: tuple, client_socket: socket.socket,
        client_public_key: RSAPublicKey, server_private_key: RSAPrivateKey,
        close_callback: Any, recv_callback: Any) -> None:

        super().__init__()
        # Keys for crypto utils
        self.client_public_key = client_public_key
        self.server_private_key = server_private_key
        self.header_size = header_size
        self.close_callback = close_callback
        self.recv_callback = recv_callback
        self.client_socket = client_socket
        self.address = address

        # User attributes
        self.cached_user_details: Union[UserDetails, None] = None
        self.session_active: bool = False
        self.user_status: str = str()
        self.user_id: int = int()
    

    def cache_user_details(self, user_details: UserDetails) -> None:
        self.cached_user_details = user_details


    def activate_user(self, user_id: int, user_details: UserDetails) -> None:
        self.user_id = user_id
        self.user_details = user_details
        self.session_active = True
        self.cached_user_details = None


    def run(self) -> None:
        while True:
            try:
                header = self.client_socket.recv(self.header_size)
                if not header:
                    raise (socket.error)
                command_length = int.from_bytes(header, byteorder="big")
                encrypted_command = self.client_socket.recv(command_length)
                if encrypted_command: self.__receive_command(encrypted_command)

            except socket.error as err:
                self.close_user()
                self.__debug(err.strerror)
                break


    def __receive_command(self, encrypted_command: bytes) -> None:
        decrypted_command = CryptoUtils.decrypt_data(encrypted_command, self.server_private_key)
        if not decrypted_command: self.__debug(f"could not decrypt: {decrypted_command}"); return

        raw_command: SocketCommand = json.loads(decrypted_command.decode())
        self.__debug(raw_command)
        self.recv_callback(self, raw_command)


    def send_command(self, command: SocketCommand) -> None:
        json_command = json.dumps(command)
        encrypted_command = CryptoUtils.encrypt_data(json_command.encode(), self.client_public_key)
        if not encrypted_command: self.__debug(f"command too large: {encrypted_command}"); return

        header = len(encrypted_command).to_bytes(self.header_size, byteorder="big")
        self.client_socket.sendall(header + encrypted_command)


    def close_user(self) -> None:
        self.client_socket.close()
        self.close_callback(self.address)


    def __debug(self, message: Union[str, SocketCommand]) -> None:
        logging.debug(f"[user {self.address}]: {message}")

