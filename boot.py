import network
import time

timeout = 0

wifi = network.WLAN(network.STA_IF)

# Restarting WiFi
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

wifi.connect('Pluto','')

if not wifi.isconnected():
    print('connecting..')
    while (not wifi.isconnected() and timeout < 5):
        print(5 - timeout)
        timeout = timeout + 1
        time.sleep(2)
        
if(wifi.isconnected()):
    print('Connected',wifi.ifconfig())
else:
    print('Time Out')
#wifi.hostname("esp32.local")
import webrepl
webrepl.start()
#import ws1


