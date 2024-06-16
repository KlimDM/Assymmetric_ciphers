import socket
import pickle
from utils import FileCrypter, DiffieHellman


HOST = '127.0.0.1'
PORT = 8080
p = 11677
a = 6409
diffie_hellman = DiffieHellman(a, p)

with socket.socket() as s:
    s.connect((HOST, PORT))
    s.send(pickle.dumps(diffie_hellman.public_key()))
    data = s.recv(1024)
    print('Получено B =', pickle.loads(data))
    B = pickle.loads(data)
    K = B ** a % p
    print("K =", K)
    while True:
        message = input("Введите сообщение: ").encode("utf-8")
        if not message:
            break
        encrypted_msg = FileCrypter.encrypt(message, K)
        print(encrypted_msg)
        s.send(encrypted_msg)
    s.close()
