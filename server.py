from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
import time
import struct


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
            buf = message
            # if message is not None:
            message = message.decode("utf-8")
            print(buf)
        except:
            pass
        # special case: empty message
        try:
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
            # download
            if message.startswith("{DOWNLOAD}"):
                msg_params = message.split("|")
                dest_name = msg_params[0][10:]
                dest_socket = find_client_socket(dest_name)
                fileName = msg_params[1]
                filepath = "./server_files/"+fileName
                print(filepath)
                if os.path.isfile(filepath):
                    fhead = struct.pack(
                        '128sl',
                        os.path.basename(filepath).encode(
                            encoding="utf-8"),
                        os.stat(filepath).st_size)
                    print('server filepath: {0}'.format(filepath))
                    dest_socket.sendall(fhead)
                    fp = open(filepath, 'rb')
                    while True:
                        data = fp.read(1024)
                        if not data:
                            print('file send over...')
                            break
                        dest_socket.sendall(data)
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
        except:
            pass
        try:
            filename, filesize = struct.unpack('128sl', buf)
            isFile = True
        except:
            isFile = False
        if not isFile and "{DOWNLOAD}" not in message:
            # private message
            try:
                msg_params = message.split("}")
                dest_name = msg_params[0][1:]
                dest_socket = find_client_socket(dest_name)
                msg = message.replace(
                    "{" + dest_name + "}", "{PRIVATE}" + prefix)
                if dest_socket:
                    send_message(
                        msg, destination=dest_socket)
                else:
                    print("Invalid Destination. %s" % dest_name)
            except:
                print("Error parsing the message: %s" % message)
        # RECEIVE FILE
        elif isFile:
            try:
                now = int(round(time.time()*1000))
                fn = filename.strip(b"\x00").decode("utf-8")
                fn = fn.split(".")
                new_filename = os.path.join(
                    './server_files/', fn[0]+"-"+str(now)+"."+fn[1])
                print(new_filename, filesize)
                print('file new name is {0}, filesize if {1}'.format(
                    new_filename, filesize))

                recvd_size = 0  # 定义已接收文件的大小
                fp = open(new_filename, 'wb')
                print('start receiving...')

                while recvd_size < filesize:
                    if filesize - recvd_size > 1024:
                        data = client.recv(1024)
                        recvd_size += len(data)
                    else:
                        data = client.recv(filesize - recvd_size)
                        recvd_size = filesize
                    fp.write(data)
                print("should receive {}, actually receive {}".format(
                    filesize, recvd_size))
                fp.close()
                print('end receive...')
                users = client.recv(1024)
                users = users.decode("utf-8")
                sendList = users.split("|")[0]
                username = users.split("|")[1]
                print(sendList)
                new_msg = "{FILE}"+prefix+"<img src=\""+new_filename+"\">"
                if sendList == "ALL":
                    send_message(new_msg, broadcast=True)
                else:
                    dest_socket = find_client_socket(sendList)
                    self_socket = find_client_socket(username)
                    msg = "{PRIVATEFILE}" + prefix + \
                        "<img src=\""+new_filename+"\">"
                    if dest_socket:
                        send_message(
                            msg, destination=self_socket)
                        send_message(
                            msg, destination=dest_socket)
                    else:
                        print("Invalid Destination. %s" % dest_name)
            except:
                print("Error receive the FILE")


def send_message(message, prefix="", destination=None, broadcast=False):
    send_msg = bytes(prefix + message, "utf-8")
    if broadcast:
        for socket in clients:
            socket.send(send_msg)
    else:
        if destination is not None:
            destination.send(send_msg)


def get_clients(separator="|"):
    names = []
    for _, name in clients.items():
        names.append(name)
    return separator.join(names)


def find_client_socket(des_name):
    for socket, name in clients.items():
        if name == des_name:
            return socket
    return None


HOST = '127.0.0.1'
# HOST = "192.168.43.194"
PORT = 30153
BUFSIZE = 1024
ADDR = (HOST, PORT)

# create TCP socket and bind the socket to the address (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

clients = {}
addresses = {}

if __name__ == "__main__":
    try:
        SERVER.listen(5)
        print("Server Started at {}:{}".format(HOST, PORT))
        ACCEPT_THREAD = Thread(target=connecting)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        SERVER.close()
    except KeyboardInterrupt:
        print("Closing...")
        ACCEPT_THREAD.interrupt()
