from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def connecting():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=receive_message, args=(client,)).start()


def receive_message(client):  # Takes client socket as argument.
    name = ""
    prefix = ""
    while True:
        try:
            message = client.recv(BUFSIZE)
            print(message)
        except:
            pass
        if message is not None:
            message = message.decode("utf-8")
        # special case: empty message
        if message == "":
            message = "{LOGOUT}"
        # message type: {LOGIN}
        if message.startswith("{LOGIN}"):
            name = message.split("}")[1]
            welcome = '{NEW}Welcome %s!' % name
            # send welcome to new comer
            send_message(welcome, destination=client)
            # send new comer information to all people
            message = "{NEW}%s has joined the chat!" % name
            send_message(message, broadcast=True)
            clients[client] = name
            prefix = name + " : "
            send_message("{CLIENTS}" + get_clients(), broadcast=True)
            continue
        # receive message {ALL} and  broadcast {MESSAGE}
        if message.startswith("{ALL}") and name:
            new_msg = message.replace("{ALL}", "{MESSAGE}"+prefix)
            send_message(new_msg, broadcast=True)
            continue
        # message type: {LOGOUT}
        if message == "{LOGOUT}":
            client.close()
            try:
                del clients[client]
            except KeyError:
                pass
            if name:
                send_message("{LEFT}%s has left the chat." %
                             name, broadcast=True)
                # update the chat room
                send_message("{CLIENTS}" + get_clients(), broadcast=True)
            break

        # private message
        try:
            msg_params = message.split("}")
            dest_name = msg_params[0][1:]
            dest_socket = find_client_socket(dest_name)
            msg = message.replace("{" + dest_name + "}", "{PRIVATE}"+ prefix)
            if dest_socket:
                send_message(
                    msg, destination = dest_socket)
            else:
                print("Invalid Destination. %s" % dest_name)
        except:
            print("Error parsing the message: %s" % message)


def send_message(message, prefix = "", destination = None, broadcast = False):
    send_msg=bytes(prefix + message, "utf-8")
    if broadcast:
        for socket in clients:
            socket.send(send_msg)
    else:
        if destination is not None:
            destination.send(send_msg)


def get_clients(separator = "|"):
    names=[]
    for _, name in clients.items():
        names.append(name)
    return separator.join(names)


def find_client_socket(des_name):
    for socket, name in clients.items():
        if name == des_name:
            return socket
    return None


HOST='127.0.0.1'
PORT=30153
BUFSIZE=1024
ADDR=(HOST, PORT)

# create TCP socket and bind the socket to the address (HOST, PORT)
SERVER=socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

clients={}
addresses={}

if __name__ == "__main__":
    try:
        SERVER.listen(5)
        print("Server Started at {}:{}".format(HOST, PORT))
        ACCEPT_THREAD=Thread(target = connecting)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()
    except KeyboardInterrupt:
        print("Closing...")
        ACCEPT_THREAD.interrupt()
