import RPi.GPIO as GPIO

# Manipulate 4 pin shared anode LED with Raspberry Pi

# Lauri rig pins
ledB = 27
ledG = 22
ledR = 10
# Test rig pins
# ledB = 6
# ledG = 5
# ledR = 4

# Enabling pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledG, GPIO.OUT)
GPIO.setup(ledR, GPIO.OUT)
GPIO.setup(ledB, GPIO.OUT)

# Sends current to all pins disabling all lights
def cleanLed():
    GPIO.output(ledG, True)
    GPIO.output(ledR, True)
    GPIO.output(ledB, True)

cleanLed()

# Setting up all leds with 1000Hz
ledGreenDim = GPIO.PWM(ledG, 1000)
ledBlueDim = GPIO.PWM(ledB,1000)
ledRedDim = GPIO.PWM(ledR,1000)

# Setting up all leds, duty cycle to max
ledGreenDim.start(100.0)
ledBlueDim.start(100.0)
ledRedDim.start(100.0)

def redLed():
    cleanLed()
    ledRedDim.ChangeDutyCycle(0.0)

def blueLed():
    cleanLed()
    ledBlueDim.ChangeDutyCycle(0.0)

def greenLed():
    cleanLed()
    ledGreenDim.ChangeDutyCycle(0.0)

# Will set LED values in duty cycle according to provided RGB value in decimal
def pickLed(r,g,b):
    cleanLed()
    ledRedDim.ChangeDutyCycle(100.0)
    ledBlueDim.ChangeDutyCycle(100.0)
    ledGreenDim.ChangeDutyCycle(100.0)
    r_led = 100 - ((100.0/255.0)*r)
    g_led = 100 - ((100.0/255.0)*g)
    b_led = 100 - ((100.0/255.0)*b)
    ledRedDim.ChangeDutyCycle(r_led)
    ledGreenDim.ChangeDutyCycle(g_led)
    ledBlueDim.ChangeDutyCycle(b_led)
    print r_led
    print g_led
    print b_led

# make_server is used to create this simple python webserver
from wsgiref.simple_server import make_server
from cgi import parse_qs
import os

# Check current path
current_dir = os.path.dirname(os.path.realpath(__file__))
# Template file
index_html = os.path.join(current_dir, 'index.html')

# Server template as a string
def serveHtml(file):
    with open(file, 'r') as myfile:
      data=myfile.read()
    return data

# Function that is ran when a http request comes in
def simple_app(env, start_response):

    # set some http headers that are sent to the browser
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)

    # What did the user ask for?
    if env["PATH_INFO"] == "/r":
        print("user asked for /on")
        cleanLed()
        redLed()
        return serveHtml(index_html)

    elif env["PATH_INFO"] == "/g":
        print("user asked for /off")
        cleanLed()
        greenLed()
        return serveHtml(index_html)

    elif env["PATH_INFO"] == "/b":
        print("user asked for /off")
        cleanLed()
        blueLed()
        return serveHtml(index_html)

    # Process a POST request with hex RGB value            
    elif env["PATH_INFO"] == "/working":
        print("user asked for /working")
        request_body_size = int(env.get('CONTENT_LENGTH', 0))
        request_body = env['wsgi.input'].read(request_body_size)
        # Request to dictionary
        d = parse_qs(request_body)
        # Parse only values we expected
        hex_color = d['led_color']
        hex_color_sting = ''.join(hex_color)
        # Split hex string
        red_int = int(hex_color_sting[1:3], 16)
        green_int = int(hex_color_sting[3:5], 16)
        blue_int = int(hex_color_sting[5:7], 16)
        print "red - %s green - %s blue - %s" % (red_int, green_int, blue_int)
        pickLed(red_int, green_int, blue_int)
        # for testing
        # return hex_color_sting
        return serveHtml(index_html)
    else:
        print("user asked for something else")
        return serveHtml(index_html)

# Create a small python server
httpd = make_server("", 8411, simple_app)
print "Serving on port 8411..."
print "You can open this in the browser http://192.168.1.xxx:8411 where xxx is your rpi ip aadress"
print "Or if you run this server on your own computer then http://localhost:8411"
httpd.serve_forever()
