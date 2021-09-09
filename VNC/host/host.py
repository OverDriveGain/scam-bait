from threading import Thread
from input_manager import InputManager
from vnc import VNC
from port_forward import ssh_tunnel
from bogus import main_account_screen
import requests
import sys

PORTS_REQUEST = '136.244.115.143:4000'
status = 'None'
connection = 'None'
vnc = VNC()
input_manager = InputManager()


if len(sys.argv) < 2:
    main_account_screen()


# Start port 7000 remote port 4005
port_1 = 6969
port_2 = 7000
print('Hosting...')
try:
    requests.get(PORTS_REQUEST)
    print(requests.get(PORTS_REQUEST))
    port_remote_1 = int(requests.get(PORTS_REQUEST).headers['port'])
    port_remote_2 = port_remote_1 + 1
    ssh1_thread = Thread(target=ssh_tunnel, args=[port_1, port_remote_1])
    ssh1_thread.daemon = True
    ssh1_thread.start()
    print("SSH 1 thread started")
    ssh2_thread = Thread(target=ssh_tunnel, args=[port_2, port_remote_2])
    ssh2_thread.daemon = True
    ssh2_thread.start()
    print("SSH 2 thread started")
    transmit_thread = Thread(target=vnc.transmit)
    transmit_thread.daemon = True
    transmit_thread.start()
    print("Transmit thread started")
    input_thread = Thread(target=input_manager.receive_input, args=[])
    input_thread.daemon = True
    input_thread.start()
    print("Input thread started")
    transmit_thread.join()
    input_thread.join()
    print("Both threads joined")

except Exception as e:
    print(e)
    print("Nothing")