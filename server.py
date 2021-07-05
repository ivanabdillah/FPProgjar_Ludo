import socket
import threading #memungkinkan aplikasi menjalankan beberapa hal sekaligus secara bersamaan

friends = {}

def read_msg(clients, sock_cli, addr_cli, username_cli):
    while True:
       #terima pesan
        data = sock_cli.recv(65535)
        if len(data)==0:
            break
        #parsing pesan
        dest,msg = data.decode("utf-8").split("|")
        unamefriend = msg
        msg = "<{}>:{}".format(username_cli,msg)

        #teruskan pesan ke semua clien
        if dest == "bcast" :
            send_broadcast (clients, msg, addr_cli)
        elif dest == "addFriend" :
            for x in clients.keys():
                if x == unamefriend :
                    friends[unamefriend] = clients[unamefriend]
                    print(msg, " Added as a friend")
        elif dest == "sendFriend" :
            send_friends (friends, msg, addr_cli)
        else:
            dest_sock_cli = clients[dest][0]
            send_msg(dest_sock_cli, msg)

        print(data)

    sock_cli.close()
    print("Connection Closed", addr_cli)

def send_friends (friends, data, sender_addr_cli):
    for sock_cli, addr_cli, _ in friends.values():
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            send_msg (sock_cli, data)

#kirim ke semua klien
def send_broadcast(clients, data, sender_addr_cli):
    for sock_cli, addr_cli, _ in clients.values():
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            print(sender_addr_cli[0], sender_addr_cli[1])
            send_msg (sock_cli, data)

def send_msg (sock_cli, data):
    sock_cli.send(bytes(data,"utf-8"))

#buat object socket server
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind object socket ke alamat ip dan port
sock_server.bind(("0.0.0.0",6666))

#listen for an incoming connection
sock_server.listen(5) #max antrian klien di memori

#buat dictionary ntuk menyimmpan informasi klein
clients = {}

while True:
    #accept connection from clien
    sock_cli, addr_cli = sock_server.accept()

    #baca username klien
    username_cli = sock_cli.recv(65535).decode("utf-8")
    print(username_cli, " joined")

    #LOGIC, kirim atau terima pesan
    #buat thread baru untuk membaca pesan dan jalankan threadnya
    thread_cli = threading.Thread(target=read_msg, args= (clients, sock_cli, addr_cli, username_cli))
    thread_cli.start()

    #simpan informasi ttg klien ke dictionary
    clients[username_cli] = (sock_cli, addr_cli, thread_cli)