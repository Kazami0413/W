listen = False
command = False
upload = False
execute = ""
tarhget = ""
upload_destination = ""

port = 0

if not len(sys.argv[1:]):
    usage()
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)

    usage()

for o,a in opts:
    if o in ("-h","--help"):
                        usage()
    elif o in ("-l","--listen"):
                        listen = True
    elif o in ("-e", "--execute"):
                        execute = a
    elif o in ("-c", "--commandshell"):
                        command = True
    elif o in ("-u", "--upload"):
                        upload_destination = a
    elif o in ("-t", "--target"):
                        target = a
    elif o in ("-p", "--port"):
                        port = int(a)
    else:

        assert False,"Unhandled Option"

if not listen and len(target)and port > 0:
    buffer = sys.stdin.read()
    client_sender(buffer)
if listen:

    server_loop()

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    client.connect((target,port))
    if len(buffer):
        client.send(buffer)
    while True:
        recv_len = 1
        response = ""
        while recv_len:
            data = client.recv(4096)
            recv_len = len(data)
            response+= data
            if recv_len < 4096:
                break
        print response,
        buffer = raw_input("")
        buffer += "\n"

        client.send(buffer)
except:
    print"[*] Exception! Exiting."

    client.close()

    global target
    global port
    if not len(target):
        target = "0.0.0.0"#使用者設定目標

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))

        client_thread.start()

        global upload
        global execute
        global command

        if len(upload_destination):
            file_buffer = ""
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                else:
                    file_buffer += data
            try:
                file_descriptor = open(upload_destination,"wb")
                file_descriptor.write(file_buffer)
                file_descriptor.close()
                client_socket.send("Successfully saved file to %s\r\n" %upload_destination)
            except:
                    client_socket.send("Failed to save file to %s\r\n" % upload_destination)

        if len(execute):
               output = run_command(execute)
               client_socket.send(output)

        if command:
            while True:
                client_socket.send("server>")
                cmd_buffter =""
                while "\n" not in cmd_buffter:
                    cmd_buffter += client_socket.recv(1024)
                response = run_command(cmd_buffter)

                client_socket.send(response)