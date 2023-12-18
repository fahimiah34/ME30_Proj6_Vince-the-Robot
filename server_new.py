# import Flask
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# import GPIO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# import time
import time 


ip_address = 0
delay_start = 0
speed = 0


# maximum and minumum speed up the ramp while pushing the tube in mm/s
max_speed = 535.71
min_speed = 124.74

# button GPIO setup
l_button = 13
r_button = 29
GPIO.setup(l_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(r_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# assign motor driver terminals to GPIO pins
in1 = 38
in2 = 40
in3 = 35
in4 = 37
ena = 3
enb = 5
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT) 
GPIO.setup(enb, GPIO.OUT)

# control speed of motors
p1 = GPIO.PWM(ena, 500)
p2 = GPIO.PWM(enb, 500)
p1.ChangeDutyCycle(100)
p2.ChangeDutyCycle(100)
p1.start(0)
p2.start(0)


# Taking input speed and converting to pwm duty cycle value
def speed_to_pwm(speed):
   min_pwm = 60
   max_pwm = 100
   return int(min_pwm + (max_pwm - min_pwm)/(max_speed - min_speed) * (speed - min_speed))

@app.route("/")
def index():
    # Render the HTML page
    return render_template("index.html")

# startup process from user input on website
@app.route("/start", methods=['POST'])
def start_process():
    global speed

    # assigning values from user
    ip_address = request.form.get('ip_address', '')
    delay_start = request.form.get('delay_start', '')
    delay_start = int(delay_start)
    speed = request.form.get('speed', '')
    speed = int(speed)

    print("Starting process with IP: {}, Delay: {}, Speed: {}".format(ip_address, delay_start, speed))
    # Include your logic to start the process with these parameters
    time.sleep(delay_start)
    p1.ChangeDutyCycle(speed_to_pwm(speed))
    p2.ChangeDutyCycle(speed_to_pwm(speed))
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    return jsonify(status="Process started")

@app.route('/target/<int:curr_speed>', methods=['GET'])
def handle_speed_request(curr_speed):
    global speed
    if curr_speed > min_speed and curr_speed < max_speed:
        speed = curr_speed
        p1.ChangeDutyCycle(speed_to_pwm(speed))
        p2.ChangeDutyCycle(speed_to_pwm(speed))
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
        return jsonify('ok'), 200
    else:
        return jsonify('no'), 200
        
@app.route('/stop', methods=['POST'])
def stop():
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    return jsonify('yay'), 200

@app.route('/get_speed', methods=['GET'])
def get_speed():
    return jsonify(speed), 200

def handle_partner_speed(speed):
    pass

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000)