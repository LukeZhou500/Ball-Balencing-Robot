#!/usr/bin/python3
import time
import math
import cv2
import numpy as np
from picamera2 import Picamera2
from collections import deque
import pigpio
import RPi.GPIO as GPIO

# --- OpenCV global speed knobs ---
cv2.setUseOptimized(True)
cv2.setNumThreads(4)

# === PID & robot imports ===
from Pid import PIDController   # <-- use the stripped version here
from robotKinematics import RobotKinematics

# === Tuning / constants ===
centerX = 90
centerY = 65
chill_range = 0
chillnumb = 30
last_time=0
TARGET_DT = 0.015

lastErrorX = 0
lastLastErrorX = 0
lastLastLastErrorX = 0
errorX = 0

lastErrorY = 0
lastLastErrorY = 0
lastLastLastErrorY = 0
errorY = 0

pid_x = PIDController(kp=0.06, ki=0.1, kd=0.01,kv=0.025) #p = 0.16 v = 0.06
pid_y = PIDController(kp=0.06, ki=0.1, kd=0.01,kv=0.025)#0.08, 0.05

# === Servo GPIO pins ===
servo1 = 18
servo2 = 13
servo3 = 12

# Start pigpio PWM control
pwm = pigpio.pi()
pwm.set_mode(servo1, pigpio.OUTPUT)
pwm.set_mode(servo2, pigpio.OUTPUT)
pwm.set_mode(servo3, pigpio.OUTPUT)

# Set PWM frequency to 50 Hz (standard for servos)
pwm.set_PWM_frequency(servo1, 50)
pwm.set_PWM_frequency(servo2, 50)
pwm.set_PWM_frequency(servo3, 50)

# Kinematics
robot = RobotKinematics()

class Camera:
    def __init__(self, resolution=(200, 150), format="RGB888"):
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(
            main={"size": resolution, "format": format},
            controls={"FrameDurationLimits": (8333, 8333)}
        )
        self.picam2.configure(config)

        self.lower_ball = np.array([5, 210, 60], dtype=np.uint8)
        self.upper_ball = np.array([15, 255, 255], dtype=np.uint8)

        self.kernel3 = np.ones((3, 3), np.uint8)
        self.queue = deque(maxlen=16)
        self.queue.append((resolution[0] // 2, resolution[1] // 2))

        self.picam2.start()

    def take_picture(self):
        return self.picam2.capture_array()

    def terminate(self):
        self.picam2.stop()
        self.picam2.close()
        cv2.destroyAllWindows()

    def preprocess(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    def find_stuff(self, hsv_frame):
        mask_ball = cv2.inRange(hsv_frame, self.lower_ball, self.upper_ball)
        mask_dilated = cv2.dilate(mask_ball, self.kernel3, iterations=1)
        mask_eroded = cv2.erode(mask_dilated, self.kernel3, iterations=6)
        mask_dilated2 = cv2.dilate(mask_eroded, self.kernel3, iterations=4)

        contours, _ = cv2.findContours(mask_dilated2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ball_center = self.queue[-1] if self.queue else (0, 0)

        if contours:
            c = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)
            if area > 30:
                x, y, w, h = cv2.boundingRect(c)
                ball_center = (x + w // 2, y + h // 2)

        self.queue.append(ball_center)
        return ball_center

def moveServo(thetaX,thetaY,H):
    #print(thetaX,"thetay",thetaY)
    if thetaX < 2 and thetaY < 2 and thetaX> -2 and thetaY >-2:      
        nx = math.sin(thetaX)*-1
        ny = math.sin(thetaY)
        nz = math.cos(math.sqrt(thetaX**2 + thetaY**2))
        #print(nx,"ny",ny,"nz",nz)
        # normalize to unit vector
        norm = math.sqrt(nx*nx + ny*ny + nz*nz)
        #print(norm)
        if norm == 0:
            norm = 1
        nx, ny, nz = nx/norm, ny/norm, nz/norm
        #print(nx,"ny",ny,"nz",nz)
        
        
        # use your current platform height
        h = H
        if nz > 0.7:
            robot.solve_inverse_kinematics_vector(nx, ny, nz, h)
            #print("Theta1:", robot.theta1, "Theta2:", robot.theta2, "Theta3:", robot.theta3)
            pwm1 = (-robot.theta1 / (math.pi/2)) * 1000 + 1530
            pwm2 = (-robot.theta2 / (math.pi/2)) * 1000 + 1495
            pwm3 = (-robot.theta3 / (math.pi/2)) * 1000 + 1450
            
            #print("PWM1:", pwm1, "PWM2:", pwm2, "PWM3:", pwm3)
            
            pwm.set_servo_pulsewidth(servo1, pwm1)
            pwm.set_servo_pulsewidth(servo2, pwm2)
            pwm.set_servo_pulsewidth(servo3, pwm3)

if __name__ == "__main__":
    cam = Camera()

    try:
        while True:
            img = cam.take_picture()
            hsv = cam.preprocess(img)
            ball_center = cam.find_stuff(hsv)
            
            current_time = time.time()
            # --- Control logic ---
            lastLastLastErrorX = lastLastErrorX
            lastLastErrorX = lastErrorX
            lastErrorX = errorX
            lastLastLastErrorY = lastLastErrorY
            lastLastErrorY = lastErrorY
            lastErrorY = errorY
            errorX = (centerX - ball_center[0])*0.4+lastErrorX*0.2+lastLastErrorX*0.2+lastLastLastErrorX*0.2
            errorY = (centerY - ball_center[1])*0.4+lastErrorY*0.2+lastLastErrorY*0.2+lastLastLastErrorY*0.2
            #print(errorX,"errorY",errorY)
            if(errorX < 50 and errorY<50): 
                outputX = pid_x.update(errorX,current_time)  # tilt in X
                outputY = pid_y.update(errorY,current_time)  # tilt in Y
                #print(outputX,"ouputY",outputY)
                thetaX = math.radians(outputX)  # tilt in X
                thetaY = math.radians(outputY)  # tilt in Y
                moveServo(thetaX, thetaY, 130.0)
            
            elapsed = current_time - last_time
            sleep_time = TARGET_DT - elapsed
            last_time = current_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    finally:
        cam.terminate()
