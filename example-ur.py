import socket
import time
import math
import struct
import codecs
class jointAngles:
    def __init__(self,base,shoulder,elbow,w1,w2,w3,a,v):
        self.base = base
        self.shoulder = shoulder
        self.elbow = elbow
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.a = a
        self.v = v

class robotInfo:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

def move(jointAngles,robotInfo):
    # This function is to move the UR
    HOST = robotInfo.ip # The remote host
    PORT = 30002
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    time.sleep(0.5)
    # position2 = str("movel([" + str(math.radians(jointAngles.base)) + "," + str(math.radians(jointAngles.shoulder)) + "," + str(math.radians(jointAngles.elbow)) + ","+ str(math.radians(jointAngles.w1)) + "," + str(math.radians(jointAngles.w2)) + "," + str(math.radians(jointAngles.w3)) + "], a=" + str(jointAngles.a)+", v="+ str(jointAngles.v)+")")
    position2 = str("movej([" + str(math.radians(jointAngles.base)) + "," + str(math.radians(jointAngles.shoulder)) + "," + str(math.radians(jointAngles.elbow)) + ","+ str(math.radians(jointAngles.w1)) + "," + str(math.radians(jointAngles.w2)) + "," + str(math.radians(jointAngles.w3)) + "], a=" + str(jointAngles.a)+", v="+ str(jointAngles.v)+")")
    final_position = position2 + '\n'
    s.sendall(final_position.encode('utf-8'))
    time.sleep(0.1)
    s.close()

def get_pos_get(robotInfo):  # noqa: E501
    #This function returns the joint position of the robot

    HOST = robotInfo.ip # The remote host
    PORT_30003 = 30003
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect((HOST, PORT_30003))
    time.sleep(1.00)
    packet_1 = s.recv(4)
    packet_2 = s.recv(8)
    packet_3 = s.recv(48)
    packet_4 = s.recv(48)
    packet_5 = s.recv(48)
    packet_6 = s.recv(48)
    packet_7 = s.recv(48) 

    packet_8 = s.recv(8)
    packet_8 = codecs.encode(packet_8, 'hex')
    packet_8 = codecs.decode(packet_8, 'hex')
    base = (struct.unpack('!d', packet_8)[0])
    base_fin = base*180/math.pi
    print ("Base = ", base_fin)

    packet_9 = s.recv(8)
    packet_9 = codecs.encode(packet_9, 'hex')
    packet_9 = codecs.decode(packet_9, 'hex')
    shoulder = (struct.unpack('!d', packet_9)[0])
    shoulder_fin = shoulder*180/math.pi
    print ("shoulder = ", shoulder_fin)

    packet_10 = s.recv(8)
    packet_10 = codecs.encode(packet_10, 'hex')
    packet_10 = codecs.decode(packet_10, 'hex')
    elbow = (struct.unpack('!d', packet_10)[0])
    elbow_fin = elbow*180/math.pi
    print ("Base = ", elbow_fin)

    packet_11 = s.recv(8)
    packet_11 = codecs.encode(packet_11, 'hex')
    packet_11 = codecs.decode(packet_11, 'hex')
    w1 = (struct.unpack('!d', packet_11)[0])
    w1_fin = w1*180/math.pi
    print ("Wrist 1 = ", w1_fin)

    packet_12 = s.recv(8)
    packet_12 = codecs.encode(packet_12, 'hex')
    packet_12 = codecs.decode(packet_12, 'hex')
    w2 = (struct.unpack('!d', packet_12)[0])
    w2_fin = w2*180/math.pi
    print ("Wrist 2 = ", w2_fin)

    packet_13 = s.recv(8)
    packet_13 = codecs.encode(packet_13, 'hex')
    packet_13 = codecs.decode(packet_13, 'hex')
    w3 = (struct.unpack('!d', packet_13)[0])
    w3_fin = w3*180/math.pi
    print ("Wrist 3 = ", w3_fin)

    current_pos = {
            "base": base_fin,
            "shoulder": shoulder_fin,
            "elbow": elbow_fin,
            "wrist1": w1_fin,
            "wrist2": w2_fin,
            "wrist3": w3_fin
    }
    s.close()
    return current_pos

if __name__ == "__main__":
    jA = jointAngles(0,90,0,0,0,0,0.1,0.1)
    robot = robotInfo('168.188.34.43','30002')
    move(jA,robot)