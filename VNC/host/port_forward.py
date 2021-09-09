import socket
import select
import sys
from threading import Thread
import paramiko


def handler(chan, host, port):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except Exception as e:
        print("Forwarding request to %s:%d failed: %r" % (host, port, e))
        return

    print(
        "Connected!  Tunnel open %r -> %r -> %r"
        % (chan.origin_addr, chan.getpeername(), (host, port))
    )
    while True:
        r, w, x = select.select([sock, chan], [], [])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            chan.send(data)
        if chan in r:
            data = chan.recv(1024)
            if len(data) == 0:
                break
            sock.send(data)
    chan.close()
    sock.close()


def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward("", server_port)
    while True:
        chan = transport.accept(1000)
        if chan is None:
            continue
        thr = Thread(
            target=handler, args=(chan, remote_host, remote_port)
        )
        thr.setDaemon(True)
        thr.start()


def ssh_tunnel(port = 7000, port_remote = 4005):
    """
    ssh -R 4000:internal.example.com:80 public.example.com
    """
    ssh_host = 'kaxtus.com'
    ssh_port = 22
    ssh_user = 'portforward'
    ssh_pass = 'p0rt!@#'
    remote_bind_port = port_remote  # port on server to forward
    forward_host = '127.0.0.1'  # dest host to forward to
    forward_port = port  # dest port to forward to

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    try:
        client.connect(
            ssh_host,
            ssh_port,
            timeout=36,
            username=ssh_user,
            password=ssh_pass,
        )
    except Exception as e:
        print("*** Failed to connect to %s:%d: %r" % (ssh_host, ssh_port, e))
        sys.exit(1)

    print(
        "Now forwarding remote port %d to %s:%d ..."
        % (remote_bind_port, forward_host, forward_port)
    )

    try:
        reverse_forward_tunnel(
            remote_bind_port, forward_host, forward_port, client.get_transport()
        )
    except KeyboardInterrupt:
        print("C-c: Port forwarding stopped.")
        sys.exit(0)


if __name__ == "__main__":
    port = 7000
    port_remote = 4005
    if len(sys.argv) > 1:
        port = 6969
        port_remote = 4004
    ssh_tunnel(port, port_remote)
