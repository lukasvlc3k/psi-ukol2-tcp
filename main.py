import socket
import time
from _thread import *
from sys import argv


# thread function
def handle_connection(sock):
    while True:
        # read data from client
        data = read_data(sock)

        # no valid data received
        if not data:
            break

        handle_http_request(sock, data)

    # close the connection
    sock.close()


def handle_http_request(sock, request) -> bool:
    request_string = request.decode('utf-8')

    lines = request_string.split("\n")

    first_line = lines[0]
    first_line_parts = first_line.split()
    if len(first_line_parts) < 3:
        send_response(sock, "ERR: invalid http request", False)
        print("ERR: invalid http request")
        return False

    method = first_line_parts[0]
    path = first_line_parts[1]
    version = first_line_parts[2]

    if "HTTP" not in version.upper():
        send_response(sock, "ERR: invalid protocol, HTTP expected (" + version + " received)", False)
        print("ERR: invalid protocol, HTTP expected (" + version + " received)")
        return False

    if not method.upper() == "GET":
        send_response(sock, "ERR: invalid method, only GET supported (" + method + " received)", False)
        print("ERR: invalid method, only GET supported (" + method + " received)")
        return False

    message = "<html><body><b>IT WORKS!</b><p>Content of " + path + "</p><p>Time: " + str(
        time.time()) + "</p></body></html>"
    send_response(sock, message, True)


def send_response(connection, content, ok: bool):
    if ok:
        header = b'HTTP/1.1 200 OK\n' + b'Content-Type: text/html\n' + b'Content-Length: ' + str(len(content)).encode(
            'utf-8') + b'\n' + b'\n'
    else:
        header = b'HTTP/1.1 403 Forbidden'

    content_data = content.encode("utf-8")
    message = header + content_data

    connection.sendall(message)


def read_data(connection, timeout=1):
    connection.setblocking(False)

    # Data can be divided into several packets
    complete_data = b''
    data = b''

    read_begin = time.time()
    while True:
        # timeout
        if time.time() - read_begin > timeout:
            break

        try:
            # reading max 4kB of data
            data = connection.recv(4 * 1024)

            # some data found
            if data:
                complete_data += data  # adding new data fragment to complete data
                read_begin = time.time()
            else:
                time.sleep(0.1)

        except BlockingIOError:
            pass

    return complete_data


def main():
    host = ""
    if len(argv) != 2:
        port = 80
    else:
        port = int(argv[1])

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    print("server started on port", port)

    # start listening on port
    server.listen()
    print("socket is listening")

    while True:
        sock, addr = server.accept()
        # starting a new thread handling the connection
        start_new_thread(handle_connection, (sock,))

    server.close()


if __name__ == '__main__':
    main()
