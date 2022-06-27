import madgwickahrs as fusion
import serial
import time
import OpenGL.GL as gl
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import math
import pygame

arduinoData=serial.Serial("/dev/ttyACM0",2000000)
# time.sleep(6)
count = 0
prevT = 0
 
def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1) * 180/3.14
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2) *180/3.14
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)*180/3.14
     
        return roll_x, pitch_y, yaw_z # in radians

def resizewin(width, height):
    """
    For resizing window
    """
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def quat_to_ypr(q):
    yaw   = math.atan2(2.0 * (q[1] * q[2] + q[0] * q[3]), q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3])
    pitch = -math.asin(2.0 * (q[1] * q[3] - q[0] * q[2]))
    roll  = math.atan2(2.0 * (q[0] * q[1] + q[2] * q[3]), q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3])
    pitch *= 180.0 / math.pi
    yaw   *= 180.0 / math.pi
    yaw   -= -0.13  # Declination at Chandrapur, Maharashtra is - 0 degress 13 min
    roll  *= 180.0 / math.pi
    return [yaw, pitch, roll]

def drawText(position, textString, size):
    font = pygame.font.SysFont("Courier", size, True)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def draw(w, nx, ny, nz):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)

    drawText((-2.6, 1.8, 2), "PyTeapot", 18)
    drawText((-2.6, 1.6, 2), "Module to visualize quaternion or Euler angles data", 16)
    drawText((-2.6, -2, 2), "Press Escape to exit.", 16)

    # if(useQuat):
    [yaw, pitch , roll] = quat_to_ypr([w, nx, ny, nz])
    drawText((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" %(yaw, pitch, roll), 16)
    glRotatef(2 * math.acos(w) * 180.00/math.pi, -1 * nx, nz, ny)
    # else:
    #     yaw = nx
    #     pitch = ny
    #     roll = nz
    #     drawText((-2.6, -1.8, 2), "Yaw: %f, Pitch: %f, Roll: %f" %(yaw, pitch, roll), 16)
    #     glRotatef(-roll, 0.00, 0.00, 1.00)
    #     glRotatef(pitch, 1.00, 0.00, 0.00)
    #     glRotatef(yaw, 0.00, 1.00, 0.00)

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(1.0, 0.2, 1.0)

    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)
    glEnd()

tracking = fusion.MadgwickAHRS()
video_flags = OPENGL | DOUBLEBUF
pygame.init()
screen = pygame.display.set_mode((640, 480), video_flags)
pygame.display.set_caption("PyTeapot IMU orientation visualization")
resizewin(640, 480)
init()
frames = 0
ticks = pygame.time.get_ticks()
freq = 0
while (True):
    while (arduinoData.inWaiting()==0):
        continue
    count+=1
    if  time.time() * 1000 - prevT > 1000:
        freq = count
        prevT = time.time() * 1000
        print(freq)
    event = pygame.event.poll()
    dataPacket = arduinoData.readline() #reply
    dataPacket=str(dataPacket,'utf-8')
    # print(dataPacket)
    splitPacket=dataPacket.split("\t")
    # print (splitPacket)
    if(len(splitPacket) < 6 ):
        print("not enough elementss")
        continue
    if splitPacket[0] == '':
        print("empty packet")
        continue
    try:
        ax = float(splitPacket[0])
        ay = float(splitPacket[1])
        az = float(splitPacket[2])
        gx = float(splitPacket[3])
        gy = float(splitPacket[4])
        gz = float(splitPacket[5])
        tracking.update_imu([gx,gy,gz],[ax,ay,az])
        # print(tracking.quaternion.q)
        quat = tracking.quaternion.q
        euler = euler_from_quaternion(quat[1], quat[2], quat[3], quat[0])
        print(euler)
        draw(quat[0], quat[1], quat[2], quat[3])
        pygame.display.flip()
        # print ("t=", time.time() * 1000, "ax=",ax," ay=",ay," az=",az, "gx=",gx," gy=",gy," gz=",gz  )
    except:
        pass