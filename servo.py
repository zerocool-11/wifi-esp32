import machine

class Servo_Motor:
    def __init__(self,pin,freq):     
        self.p1=machine.Pin(pin)
        self.servo = machine.PWM(self.p1,freq=freq)
        
    def rotate(self,angle):
        self.servo.duty(angle)
        
        


