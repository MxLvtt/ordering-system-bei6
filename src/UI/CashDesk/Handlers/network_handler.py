import select
import socket
import time
import sys
import random
import math

# References file contains all the global information
import Templates.references as REFS

from Handlers.timer_handler import TimerHandler
from Handlers.encryption_handler import EncryptionHandler


class NetworkHandler:
    DEBUG = True
    initialized = False

    HEADERSIZE = 5

    IP_CONFIG = ("127.0.0.1", 80)
    IP_CONFIG_PARTNER = ("127.0.0.1", 80)

    KITCHEN_IP_CONFIG = (REFS.KITCHEN_SERVER_IP, REFS.KITCHEN_SERVER_PORT)
    CASHDESK_IP_CONFIG = (REFS.CASHDESK_SERVER_IP, REFS.CASHDESK_SERVER_PORT)

    SERVER_SOCKET = None

    def __init__(self, main_station: bool):
        """ Initializes the network handler.

        main_station: True, if the ordering system runs on the cashdesk station. False, for the kitchen station.
        """
        if main_station:
            NetworkHandler.IP_CONFIG = NetworkHandler.CASHDESK_IP_CONFIG
            NetworkHandler.IP_CONFIG_PARTNER = NetworkHandler.KITCHEN_IP_CONFIG
        else:
            NetworkHandler.IP_CONFIG = NetworkHandler.KITCHEN_IP_CONFIG
            NetworkHandler.IP_CONFIG_PARTNER = NetworkHandler.CASHDESK_IP_CONFIG

        NetworkHandler.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        NetworkHandler.SERVER_SOCKET.bind(NetworkHandler.IP_CONFIG)
        NetworkHandler.SERVER_SOCKET.listen()

        NetworkHandler.initialized = True


######################################  SERVER METHODES (RECEIVING DATA) ######################################


    @staticmethod
    def string_to_byte(text):
        return bytes(text, "utf-8")

    @staticmethod
    def receive(socket):
        if not EncryptionHandler.initialized:
            print("EncryptionHandler not initialized yet. Aborting the receive method.")
            return

        # Array to store all received message junks
        msg_chunks = []
        # Counter of received bytes
        bytes_received = 0

        while bytes_received < REFS.MESSAGE_LENGTH:
            try:
                chunk = socket.recv(min(REFS.MESSAGE_LENGTH - bytes_received, 2048))
            except OSError as err:
                print("NetworkHandler send error: {0}".format(err))
                raise err

            if chunk == b'':
                raise RuntimeError("Socket connection broken while receiving")

            # Decode the chunk to UTF-8
            chunk = chunk.decode("utf-8")

            # Add the chunk to the list of all received chunks
            msg_chunks.append(chunk)

            # Update the amount of bytes received
            bytes_received = bytes_received + len(chunk)
        
        string_fullmsg = ''.join(msg_chunks)

        return EncryptionHandler.decrypt(string_fullmsg)

    def start_receive_loop(self):
        """ Continuos loop that will constantly wait for messages to arrive
        and if so, send a response to the client and also call events so that
        services can react to the message.

        This can not be a static method and has to be called by the object created 
        in the cashdesk-gui-model class.
        """
        try:
            if not NetworkHandler.initialized:
                raise RuntimeError("NetworkHandler has not been initialized yet.")

            read_list = [NetworkHandler.SERVER_SOCKET]
            write_list = [NetworkHandler.SERVER_SOCKET]

            readable, writable, inerror = select.select(read_list, write_list, [], 0)

            for s in readable:
                if s is NetworkHandler.SERVER_SOCKET:
                    # Waits for client to connect
                    (clientsocket, address) = NetworkHandler.SERVER_SOCKET.accept()

                    # Receiving data from client
                    received_msg = NetworkHandler.receive(clientsocket)

                    print(f"Received: '{received_msg}'")

                    service_response = ""

                    # TODO: call event and give along the received message
                    # TODO: if event returns anything, attach it to the handshake

                    service_response = "M12OK"

                    try:
                        recved_id = received_msg[0:REFS.IDENTIFIER_LENGTH]
                        # Responding to client to indicate a successfull message transmission
                        # clientsocket.send(NetworkHandler.string_to_byte(REFS.HANDSHAKE_MSG))
                        NetworkHandler.send(
                            recved_id + REFS.HANDSHAKE_MSG + service_response,
                            clientsocket
                        )
                    except OSError as err:
                        print("NetworkHandler send error: {0}".format(err))
                        raise err
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        finally:
            # Run this function again after <delay_ms> milliseconds
            TimerHandler.start_timer(
                callback=self.start_receive_loop,
                delay_ms=REFS.RECEIVE_REFRESH_DELAY,
                store_id=False
            )

    # @staticmethod
    # def do_decrypt(ciphertext):
    #     iv = Random.new().read(AES.block_size)
    #     cipher = AES.new(REFS.PUBLIC_KEY_16BIT, AES.MODE_CBC, iv)
    #     message = iv + cipher.decrypt(ciphertext)

    #     return message


###################################### CLIENT METHODES (SENDING DATA)  ######################################


    @staticmethod
    def send_with_handshake(raw_message):
        identifier = REFS.FORMAT_STRING.format(random.randint(0, REFS.MAX_IDENTIFIER))

        raw_message = identifier + raw_message

        # Create client connection to the server of the other station
        _socket = NetworkHandler.connect()

        # If message has been sent successfully
        if NetworkHandler.send(raw_message, _socket) is True:
            response = ""

            try:
                if NetworkHandler.DEBUG:
                    print("Waiting for ACK response...", end=' ')
                # Receive any response
                response = _socket.recv(1024)
            except OSError as err:
                print("NetworkHandler receive error: {0}".format(err))
                raise err
            finally:
                _socket.close()

            decrypted_response = EncryptionHandler.decrypt(response.decode("utf-8"))

            # Check response for handshake identifier
            if f"{identifier}{REFS.HANDSHAKE_MSG}" in decrypted_response:
                if NetworkHandler.DEBUG:
                    print("Success!")

                additional_text = decrypted_response.replace(f"{identifier}{REFS.HANDSHAKE_MSG}", "")
                if additional_text != "":
                    print(f"Additional handshake content: '{additional_text}'")
            else:
                if NetworkHandler.DEBUG:
                    print("Failed!")
                # TODO ---> raise error? Resend?
                pass
            
        _socket.close()

    @staticmethod
    def send(raw_message, _socket) -> bool:
        if not EncryptionHandler.initialized:
            print("EncryptionHandler not initialized yet. Aborting the receive method.")
            return

        if NetworkHandler.DEBUG:
            print(f"Sending: '{raw_message}'")

        # Encrypt the raw message
        msg = EncryptionHandler.encrypt(raw_message)

        if len(msg) < REFS.MESSAGE_LENGTH:
            null_bytes = [b'\0' for x in range(REFS.MESSAGE_LENGTH - len(msg))]
            msg = msg + b''.join(null_bytes)
        
        totalsent = 0

        # Repeat as long as we haven't sent every message chunk
        while totalsent < REFS.MESSAGE_LENGTH:
            sent = 0

            try:
                # Send as much of the message as possible
                sent = _socket.send(msg[totalsent:])
            except OSError as err:
                print("NetworkHandler send error: {0}".format(err))
                raise err

            # "sent" contains the actual number of bytes sent
            # If 0, then something went wong
            if sent == 0:
                raise RuntimeError("Socket connection broken while sending message")

            # Increment the amount of bytes sent in total
            totalsent = totalsent + sent

            # Did we send all enough bytes?
            if totalsent == REFS.MESSAGE_LENGTH:
                if NetworkHandler.DEBUG:
                    print(f"Full message (length = {totalsent} Bytes) was sent successfully.")

                return True

        return False

    @staticmethod
    def connect():
        _socket = None

        try:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.connect(NetworkHandler.IP_CONFIG_PARTNER)
        except OSError as err:
            print("NetworkHandler connect error: {0}".format(err))
            raise err

        return _socket

    # @staticmethod
    # def do_encrypt(message) -> bytes:
    #     cipher = AES.new(REFS.PUBLIC_KEY_16BIT, AES.MODE_CBC, 'This is an IV456')
    #     ciphertext = cipher.encrypt(message)
    #     return ciphertext


###################################### some other stuff maybe i'll need it maybe ned ######################################

    # def send(self, imsg):
    #     # MSGLEN = len(msg)                                                     # get msg length
    #     # msg = f'{len(msg):<{HEADERSIZE}}' + msg                               # integrate it in the beginning of the msg -> msg= Length + Headersize*space + msg
    #     # totalsent = 0
    #     msg = self.do_encrypt(imsg)
    #     while totalsent < MSGLEN:                                             # check if the total sent less than msg length
    #         sent = NetworkHandler.SERVER_SOCKET.send(msg[totalsent:])                            # send the msg part
    #         if sent == 0:
    #             raise RuntimeError("socket connection broken")
    #         totalsent = totalsent + sent
    #         if totalsent == MSGLEN:
    #             print(f"full message length: {totalsent} was sent successfully")

    # def receive(self,clientsocket):
    #     msg_chunks = []
    #     bytes_received = 0

    #     while bytes_received < MSGLEN:
    #         chunk = clientsocket.recv(min(MSGLEN - bytes_received, 2048))
    #         if chunk == b'':
    #             raise RuntimeError("socket connection broken")
    #         msg_chunks.append(chunk)
    #         bytes_received = bytes_received + len(chunk)

    #     string_fullmsg = b''.join(msg_chunks)
    #     return do_decrypt(string_fullmsg)


###################################### other shit ######################################

    # def create_keys(self):                                                 # Client
    #     random_generator = Random.new().read
    #     self.key = RSA.generate(1024,random_generator)                      # private key size of 1024 of random characters
    #     public = key.publickey().exportKey()                                # public key exported public key from previously generated private key
    #     hash_object = hashlib.sha1(public)                                  # hash public key to send over to server
    #     hex_digest  = hash_object.hexdigest()                               # hex_digest and public will be sent to server, which will verify them by comparing the hash got from client and new hash of the public key.

    # def encrypt(self):                                                        # server
    #     """ encrypt CTR MODE session key """
    #     key_128 = os.urandom(16)                                              # create 16bit long key
    #     en = AES.new(key_128,AES.MODE_CTR,counter = lambda:key_128)
    #     encrypto = en.encrypt(key_128)                                        # encrypt created key
    #     #hashing sha1
    #     en_object = hashlib.sha1(encrypto)
    #     en_digest = en_object.hexdigest()                                     # en_digest is session key
    #     #encrypting session key and public key
    #     E = server_public_key.encrypt(encrypto,16)                            # after encrypting

    # def decrypt(string msg):                                                   #decrypt msg coming from server
    #     en = eval(msg)
    #     decrypt = key.decrypt(en)
    #     return decrypt
    #    # hashing sha1
    #     en_object = hashlib.sha1(decrypt) en_digest = en_object.hexdigest()
