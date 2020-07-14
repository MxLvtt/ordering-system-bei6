import socket
import time
import TimerHandler from timer_handler
from Crypto import Random
from Crypto.PublicKey import RSA
import hashlib


class NetworkHandler:
    CASHDESK_SERVER_IP   = "0.0.0.0"
    CASHDESK_SERVER_PORT = "0000"

    KITCHEN_SERVER_IP   = "0.0.0.0"
    KITCHEN_SERVER_PORT = "0000"
    HANDSHAKE_MSG       = "msg received thanks"                                          # this msg is just for debugging purposes
    HEADERSIZE   = 5

    def __init__(self,Server=True,station):                                              # station = "kitchen" oder "cashdesk"
        if Server is True AND station is "kitchen":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                # set server socket
            s.bind(( KITCHEN_SERVER_IP, KITCHEN_SERVER_PORT ))
            s.listen()
        elif Server is True AND station is "cashdesk":
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                # set server socket
            s.bind(( CASHDESK_SERVER_IP, CASHDESK_SERVER_PORT ))
            s.listen()



########################  SERVER METHODES (RECEIVING DATA) ######################################

    def receive(self,clientsocket):
        fullMsg = []                                                                     # Array to store msg
        bytes_recd = 0                                                                   # counter of received bytes
        
        while bytes_recd < MSGLEN:
            partMsg = clientsocket.recv(min(MSGLEN - bytes_recd, 2048))
            if partMsg == b'':
                raise RuntimeError("socket connection broken")
            partMsg = partMsg.decode("utf-8")
            fullMsg.append(partMsg)
            bytes_recd = bytes_recd + len(partMsg)
        string_fullmsg = b''.join(fullMsg)
        return do_decrypt(string_fullmsg)   



        
    def receive_messages_loop(self):
        #Todo : receive Messages
        clientsocket, address = self.sock.accept()                                  # waits for client to connect
        received_msg = self.receive(clientsocket)                                   # recieves data 
        #Todo Handshake 
        clientsocket.send(bytes(HANDSHAKE_MSG, "utf-8"))                            # telling client that msg arreived
        #Todo call event
    
        TimerHandler.start_timer(self.receive_messages_loop, 500)



    @staticmethod
    def do_decrypt(ciphertext):
        obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        message = obj2.decrypt(ciphertext)
        return message







############################## CLIENT METHODES (SENDING DATA)  ##############################################
    @staticmethod
    def send_with_handshake_to(station,msg):                                             # station -> "kitchen" / "cashdesk", msg -> msg to be sent
        if station is "kitchen":                                                         
            sock = connect_to_kitchen()                                                  # create socket --> connect
            if send(msg,sock) is True:                                                   # if full msg sent
                Handshake = sock.recv(1024)                                              # wait for server to send hanshake msg
                if Handshake.decode("utf-8") is HANDSHAKE_MSG:                           # check hanshake msg
                    print("msg received with hanshake")
                    sock.close()
                else:
                    # todo ---> raise error?    
        elif station is "cashdesk":                                                     
            sock = connect_to_cashdesk()                                                 # create socket --> connect
            if send(msg,sock) is True:                                                   # if full msg sent
                Handshake = sock.recv(1024)                                              # wait for server to send hanshake msg
                if Handshake.decode("utf-8") is HANDSHAKE_MSG:                           # check hanshake msg
                    print("msg received with hanshake")
                    sock.close()
                else:
                    # todo ---> raise error?      


    @staticmethod
    def send(imsg,sock):
        msg = self.do_encrypt(imsg)                                                   # encrypt msg
        # MSGLEN = len(msg)                                                             # get msg length
        # msg = f'{len(msg):<{HEADERSIZE}}' + msg                                       # integrate it in the beginning of the msg -> msg= Length + Headersize*space + msg
        totalsent = 0
        while totalsent < MSGLEN:                                                     # check if the total sent less than msg length
            sent = sock.send(bytes(msg[totalsent:], "utf-8"))                         # send the msg part
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
            if totalsent == MSGLEN:                                                   # full msg is sent
                print(f"full message length: {totalsent} was sent successfully")
                return True
      

    @staticmethod 
    def connect_to_kitchen():                                                            # connect to the kitchen server as client
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)                        # set client socket 
        sock.connect((KITCHEN_SERVER_IP, KITCHEN_SERVER_PORT)) 
        return sock

    @staticmethod
    def connect_to_cashdesk():                                                           # connect to the cashdesk server as client
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )                       # set client socket 
        sock.connect((CASHDESK_SERVER_IP, CASHDESK_SERVER_PORT)) 
        return sock                          


    @staticmethod
    def do_encrypt(message):
        obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        ciphertext = obj.encrypt(message)
        return ciphertext
   




    






############################ some other stuff maybe i'll need it maybe ned ######################################################

    # def send(self, imsg):
    #     # MSGLEN = len(msg)                                                     # get msg length
    #     # msg = f'{len(msg):<{HEADERSIZE}}' + msg                               # integrate it in the beginning of the msg -> msg= Length + Headersize*space + msg
    #     # totalsent = 0
    #     msg = self.do_encrypt(imsg)
    #     while totalsent < MSGLEN:                                             # check if the total sent less than msg length
    #         sent = self.sock.send(msg[totalsent:])                            # send the msg part
    #         if sent == 0:
    #             raise RuntimeError("socket connection broken")
    #         totalsent = totalsent + sent
    #         if totalsent == MSGLEN:
    #             print(f"full message length: {totalsent} was sent successfully")

    # def receive(self,clientsocket):
    #     fullMsg = []
    #     bytes_recd = 0

    #     while bytes_recd < MSGLEN:
    #         partMsg = clientsocket.recv(min(MSGLEN - bytes_recd, 2048))
    #         if partMsg == b'':
    #             raise RuntimeError("socket connection broken")
    #         fullMsg.append(partMsg)
    #         bytes_recd = bytes_recd + len(partMsg)

    #     string_fullmsg = b''.join(fullMsg)
    #     return do_decrypt(string_fullmsg)    


        



############################################################# other shit #################################################################




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