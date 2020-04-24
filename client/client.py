from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:
    """
    for communication with server
    """
    HOST = "localhost"
    PORT = 5500
    ADDR = (HOST, PORT)
    BUFSIZ = 512

    def __init__(self, name):
        """
        Init object and send name to server
        :param name: str
        여기서는 메시지를 받고 쓰레드처리
        클라이언트에서 메시지 수신을 여기서 함.
        """
        self.lock = Lock()  # 쓰레드 블락을 이용하여 메모리 안정성을 높이기 위해서 레드 락을 설정.
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)

    def receive_messages(self):
        """
        receive messages from server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode()

                # make sure memory is safe to access
                self.lock.acquire()  # 메모리 안정성을 위해서 쓰레드 락 설정
                self.messages.append(msg)
                self.lock.release()  # 쓰레드 락 해제
                print(msg)
            except Exception as e:
                print("[EXCEPTION]", e)
                break

    def send_message(self, msg):
        """
        send messages to server
        :param msg: str
        :return:None
        """
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def get_messages(self):
        """
        :returns
        :param: list[str]
        """
        messages_copy = self.messages[:]
        # make sure memory is safe to access
        self.lock.acquire()  # 메모리 안정성을 위해서 쓰레드 락 설정
        self.messages =[]
        self.lock.release()  # 쓰레드 락 해제
        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")
