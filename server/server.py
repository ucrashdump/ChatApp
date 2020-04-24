from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from person import Person
import time

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def broadcast(msg, name):
    """
    send new messages to all clients
    :param msg:bytes["utf8"]
    :param name: str
    :return: """
    for person in persons:
        client = person.client
        client.send(bytes(name, "utf8") + msg)


def client_communication(person):
    """
    Thread to handle all messages from client
    :param: client: Person
    :return: None
    """
    client = person.client
    # get persons name
    # first message received is always the persons name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the chat!", "utf8")
    broadcast(msg, "")  # broadcast welcome message
    while True:  # wait for any messages from person.
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("{quit}", "utf8"):  # if message is quit disconnect clients
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:  # otherwise send message to all other clients
                broadcast(msg, name+": ")
                print(f"{name}: ", msg.decode("utf8"))

        except Exception as e:
            print("[EXCEPTION]", e)
            break


def wait_for_connection():
    """
    Wait for connection from new clients, start new thread once connected
    :param SERVER: SOCKET
    :return: None
    """
    run = True
    while run:
        try:
            client, addr = SERVER.accept()  # wait for any new connections
            person = Person(addr, client)  # create new person for connection
            persons.append(person)
            print(f"[CONNECTION]{addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            run = False
            break

    print("SERVER CRASHED")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # open server to listen for connections
    print("[STARTED] Waiting for connections...")
    ACCEPT_THREAD: Thread = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
