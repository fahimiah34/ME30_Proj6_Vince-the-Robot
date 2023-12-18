import time
import RPi.GPIO as GPIO
import requests

GPIO.setmode(GPIO.BOARD)

#ip address of other pi
PI_IP = '10.243.83.75'

# GPIO pins for button input
l_button = 13
r_button = 29
GPIO.setup(l_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(r_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# assign motor driver terminals to GPIO pins
# in1 = 38
# in2 = 40
# in3 = 35
# in4 = 37
# ena = 3
# enb = 5
# GPIO.setup(in1, GPIO.OUT)
# GPIO.setup(in2, GPIO.OUT)
# GPIO.setup(in3, GPIO.OUT)
# GPIO.setup(in4, GPIO.OUT)
# GPIO.setup(ena, GPIO.OUT)
# GPIO.setup(enb, GPIO.OUT)

# p1 = GPIO.PWM(ena, 500)
# p2 = GPIO.PWM(enb, 500)
# p1.ChangeDutyCycle(100)
# p2.ChangeDutyCycle(100)

# GPIO.output(in1, GPIO.HIGH)
# GPIO.output(in2, GPIO.LOW)
# GPIO.output(in3, GPIO.HIGH)
# GPIO.output(in4, GPIO.LOW)

# defining which ramp side the robot is on
on_left = False
slowed = False

def adjust_motor_speed(partner_ahead=False):
    global slowed
    speed = requests.get('http://10.243.89.129:5000/get_speed')
    speed = int(speed.content.decode('utf-8'))
    print('CURRENT SPEED FROM SERVER!!!!: '+str(speed))

    #if both buttons are pressed, do nothing
    if not GPIO.input(l_button) and not GPIO.input(r_button):
        # if we are at minimum speed for partner to catch up, then speed up again
        if slowed:
            response = requests.get('http://10.243.89.129:5000/target/325') #return to standard speed
            print('returned to normal speed')
            slowed = False
        return
    
    # If we're behind, speed up
    elif on_left and not GPIO.input(l_button) or not on_left and not GPIO.input(r_button):
        print('We are behind')
        speed = speed + 50
        response = requests.get('http://10.243.89.129:5000/target/' + str(speed))
        response = response.content.decode('utf-8')
        print('Increasing speed by 50 mm/s')
        
        #if we can't go up by 50, go to maximum and ask other robot to slow down
        if response == 'no':
            speed = speed - 150
            requests.get('http://10.243.89.129:5000/target/530') #telling ourselves to go to maximum speed
            requests.get('http://' + PI_IP + ':5000/target/' + str(speed))
            print('Going to maximum speed')
        slowed = False
    
    # If we're ahead, slow down
    elif on_left and not GPIO.input(r_button) or not on_left and not GPIO.input(l_button):
        speed = speed - 50
        response = requests.get('http://10.243.89.129:5000/target/'+str(speed))
        response = response.content.decode('utf-8')
        print('Reducing speed by 50 mm/s')

        #if we can't down up by 50, go to minimum and ask other robot to speed up
        if response == 'no':
            speed = speed + 150
            requests.get('http://10.243.89.129:5000/target/125') #telling ourselves to go to maximum speed
            requests.get('http://' + PI_IP + ':5000/target/' + str(speed))
            print('going to minimum speed')
        slowed = True

def monitor_buttons():
    while True:
        if requests.get('http://10.243.89.129:5000/stop').content.decode('utf-8') == 'yay':
            return
        if GPIO.input(l_button) != GPIO.input(r_button):
            adjust_motor_speed()
        time.sleep(0.1)

if __name__ == '__main__':
    time.sleep(0.5)
    monitor_buttons()

#code for asking the partner to change speed
     # api = 'http://10.243.93.234:5000/target/' + str(speed + 50)
    # print(api)
    # response = requests.get(api)
    # partner_status = response.content.decode('utf-8')

    # if (partner_status == 'no'):
    #     # slow down because they can't go faster or
    #     # speed up if they can't go slower
    #     pass
