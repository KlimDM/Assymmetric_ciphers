import socket
import pickle
import threading
from utils import FileCrypter

HOST = '127.0.0.1'
PORT = 8080
b = 5408


def handle_client(conn, addr):
    print(f'Подключено от: {addr}')
    with conn:
        data = conn.recv(1024)
        if not data:
            return None
        message = pickle.loads(data)
        g, p, A = message
        print(f"Получено от {addr}: {message}")
        B = g ** b % p
        K = A ** b % p
        conn.send(pickle.dumps(B))
        print("K =", K)
        while True:
            message = conn.recv(1024)
            if not message:
                break
            print(message)
            decrypted_msg = FileCrypter.decrypt(message, K).decode("utf-8")
            print(f"Получено от {addr}: '{decrypted_msg}'")
        s.close()


with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        break
