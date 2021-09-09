import eel
from threading import Thread
from input_manager import InputManager
from vnc import VNC

status = 'None'
connection = 'None'
vnc = VNC()
input_manager = InputManager()

eel.init('web')

@eel.expose
def stop_host():
    global status
    status = 'None'
    print("Stopping server...")

@eel.expose
def connect(ip, port_1):
    global status
    global vnc
    global connection
    print('Connecting...: ' + ip)
    input_manager.ip = ip
    input_manager.port = int(port_1)
    vnc.ip = ip
    vnc.port = int(port_1) + 1
    try:
        vnc.start_receive()
        input_manager.connect_input()
        connection = 'active'
    except Exception as e:
        print(e)
        print('Connection failed...')

@eel.expose
def test_opened_ports(ip, port_start, port_end):
    global status
    global vnc
    global connection
    input_manager.ip = ip
    vnc.ip = ip
    opened_ports = []
    for i in range(int(port_start), int(port_end), 2):
        port_1 = i
        opened_ports.append(port_1)
        input_manager.port = int(port_1)
        vnc.port = int(port_1) + 1
        try:
            print('Testing port: ' + str(port_1))
            vnc.start_receive()
            input_manager.connect_input()
        except Exception as e:
            print(e)
            print('Connection failed to port: ' + str(port_1))
            opened_ports.pop()
    print('Opened ports: ')
    print(opened_ports)

@eel.expose
def transmit_input(data, event_type):
    if event_type == 'keydown':
        input_manager.transmit_input(keydown=data)
        pass
    elif event_type == 'keyup':
        input_manager.transmit_input(keyup=data)
        pass
    elif event_type == 'mousemove':
        input_manager.transmit_input(mouse_pos=data)
        pass
    elif event_type == 'mousedown':
        input_manager.transmit_input(mouse_pos=data['pos'], mouse_down=data['button'])
    elif event_type == 'mouseup':
        input_manager.transmit_input(mouse_pos=data['pos'], mouse_up=data['button'])

eel.start('index.html', block=False, port=8081)

while True:
    if connection == 'active':
        eel.updateScreen(vnc.receive())
    eel.sleep(.01)
