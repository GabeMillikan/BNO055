import serial
import serial.tools.list_ports
import threading
import struct
import time
from vector import *

class BNO055:
    def __init__(self, baud = 115200, port = None, timeout = 1):
        if port == None:
            ports = serial.tools.list_ports.comports()
            assert len(ports) > 0, "No ports found, please provide a port"
            port = str(ports[0]).split(" ")[0]
        
        self.port = port
        self.baud = baud
        self.timeout = timeout
        try:
            self.serialConnection = serial.Serial(self.port, self.baud, timeout = self.timeout)
        except:
            raise BaseException("Couldnt open serial port '%s'" % self.port)
        
        self.gravity = vector(0, 0, 0)
        self.orientation = vector(0, 0, 0)
        self.acceleration = vector(0, 0, 0)
        self.lastUpdate = 0
        self.updateCount = 0
        self.forwardVector = vector(0,0,1)
        
        self.die = False
        
        self.updateThread = threading.Thread(target = self.updateLoop)
        self.updateThread.start()
    
    def updateLoop(self):
        TATA = 0xffaaffbb
        TATA = TATA.to_bytes(4, 'little')
    
        while not self.die:
            try:
                v = self.serialConnection.read(4)
                
                if v != TATA or self.die:
                    continue
                
                # read 3 float vectors: gravity, orientation, acceleration
                # 3 vectors = 9 floats = 36 bytes
                data = self.serialConnection.read(36)
                data = struct.unpack('f' * 9, data)
                
                self.gravity = vector(*data[0:3])
                self.orientation = vector(*data[3:6])
                self.acceleration = vector(*data[6:9])
                
                self.lastUpdate = time.time()
                self.updateCount += 1
            except BaseException as e:
                print(e)
                self.serialConnection.close()
                self.serialConnection.open()
            
            # try to calculate rotation matrix :shrug:
            # orientation = (yaw, pitch, roll) = (alpha, beta, gamma)
            yaw   = rad(self.orientation.x)
            pitch = rad(self.orientation.y)
            roll  = rad(self.orientation.z)
    
            self.forwardVector = vector(
                cos(yaw) * cos(pitch),
                cos(yaw) * sin(pitch) * sin(roll) - cos(yaw)*cos(roll),
                cos(yaw) * sin(pitch) * cos(roll) + sin(yaw) * sin(roll))
    
    def close(self):
        self.die = True
        self.updateThread.join()
        self.serialConnection.close()
f = open("data.txt", 'w+')
if __name__ == "__main__":
    bno = BNO055()
    input("press enter to start")
    try:
        while True:
            #print()
            #print("Gravity     : %s" % str(bno.gravity))
            print("Orientation : %s" % str(bno.orientation))
            #print("forward     : %s" % str(bno.forwardVector))
            #print("Acceleration: %s" % str(bno.acceleration))
            f.write(str(tuple(bno.orientation.get())) + ", " + str(tuple(bno.gravity.get())) + ",\n")
            time.sleep(0.04)
    except BaseException as e:
        print(e)
    bno.close()
    f.close()
    
    
    
