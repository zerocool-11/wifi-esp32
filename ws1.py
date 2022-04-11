import machine
from microWebSrv import MicroWebSrv
import json
from time import sleep
from servo import Servo_Motor

s=Servo_Motor(23,50)
s1=Servo_Motor(22,50)

# ow = Onewire(23)  # Initialize onewire & DS18B20 temperature sensor
# ds = Onewire.ds18x20(ow, 0)

# rtc = RTC()  # Real-time clock
# rtc.ntp_sync(server='us.pool.ntp.org', tz='PST8PDT')  # Pull time from Internet

# tm = Timer(0)  # Instatiate hardware timer
LED =machine.Pin(2,machine.Pin.OUT)

def cb_receive_text(webSocket, msg) :
    print(type(msg))
    print("WS RECV TEXT : %s" % msg)
    lst=msg.split(" ")
    if lst[0]=="s1":
        if int(lst[1]) in range(40,110):
            print("rotation recieved : ",lst[1])
            angle=int(lst[1])
            s.rotate(angle)
    if lst[0]=="s2":
        if int(lst[1]) in range(40,110):
            print("rotation recieved : ",lst[1])
            angle=int(lst[1])
            s1.rotate(angle)
    else:
            print("no rotation is being passed")
    #s.rotate(angle)
    
    webSocket.SendText("Reply for %s" % msg)

def cb_receive_binary(webSocket, data) :
    print("WS RECV DATA : %s" % data)

def cb_closed(webSocket) :
    # LED.value(0)  # Dispose of timer
    print("WS CLOSED")

def cb_timer(timer, websocket):
    LED.value(1)
    dict = {}  # Store data in dict
    dict['status'] = 1  # Poll temperature sensor
    print(dict)
    # dict['internal'] = machine.internal_temp()[1]  # Read ESP32 internal temp
    # dict['time'] = rtc.now()  # Record current time
    websocket.SendText(json.dumps(dict))  # Convert data to JSON and send
    
def cb_accept_ws(webSocket, httpClient) :
    print("WS ACCEPT")
    webSocket.RecvTextCallback   = cb_receive_text
    webSocket.RecvBinaryCallback = cb_receive_binary
    webSocket.ClosedCallback 	 = cb_closed
    cb = lambda timer: cb_timer(timer, webSocket)  # Use lambda to inject websocket
    # tm.init(period=3000, callback=cb)  # Init and start timer to poll temperature sensor

def start_websocket():
    mws = MicroWebSrv()                 # TCP port 80 and files in /flash/www
    mws.MaxWebSocketRecvLen     = 256   # Default is set to 1024
    mws.WebSocketThreaded       = True  # WebSockets with new threads
    mws.WebSocketStackSize      = 4096
    print("all the required variables has been initialized")
    mws.AcceptWebSocketCallback = cb_accept_ws # Function to receive WebSockets
    mws.Start(threaded=False)  # Blocking call (CTRL-C to exit)
    print("server started")
    print('Cleaning up and exiting.')
    mws.Stop()




