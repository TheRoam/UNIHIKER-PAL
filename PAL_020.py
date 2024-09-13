#READ COFIG FILE
print("--READING USER CONFIG")
import yaml
with open('/root/upload/PAL/PAL_config.yaml', 'r') as file:
    config=yaml.safe_load(file)

#CONFIGURATION VARIABLES
#--City ID for WMO weather forecast. Check IDs at:
#---https://worldweather.wmo.int/en/json/full_city_list.txt
CityID=config["PAL"]["wmo_city_id"]
#--Smart light brand: only Shelly25 allowed (Sonoff and Shelly1 TBC)
#---(otherwise, edit turnOn and turnOff functions according to local HTTP API)
lampBrand=config["DEVICES"]["light1"]["brand"]
lampChannel=config["DEVICES"]["light1"]["channel"]
#--Smart light local IP
#---add user and password if protected: "user:password@192.168.1.X"
lampIP=config["DEVICES"]["light1"]["ip"]
#--WIFI SSID and Password
#---Used to restore connection if lost (this has happened to occur several times
#---during testing, stopping the assistant service
wifiSSID=config["CREDENTIALS"]["ssid"]
wifiPWD=config["CREDENTIALS"]["pwd"]
#--Power save mode
#--- 1 -> Active: reduces brightness after 30 seconds
#--- 0 -> Inactive: brightness keeps constant
ps_mode=config["PAL"]["power_save_mode"]
#--Room temperature
#--- 1 -> Enabled: BMP-280 sensor is installed and will show room temperature.
#--- 0 -> Disabled: BMP-280 sensor is NOT installed and won't show room temperature.
room_temp==config["PAL"]["temperature_sensor"]

#--Eye theme:
#---chose from the files in the "eyes" folder: happy, angry, sad, surprised.
#---Voice recognition will trigger an animation that will change from default eyesA to eyesB
eyesA="surprised"
eyesB="happy"

#--Activation keywords
#---Recognized strings that will activate command recognition
activate=[
    "hey pal",
    "hey PAL",
    "pal",
    "pall",
    "Pall",
    "hey Pall",
    "Paul",
    "hey Paul",
    "pol",
    "Pol",
    "hey Pol",
    "poll",
    "pause",
    "paypal",
    "PayPal",
    "hey paypal",
    "hey PayPal"
]

import os
import subprocess
import time
from unihiker import Audio  # Import the package
audio = Audio()  # Instantiate the Audio class
#UNIHIKER gui
from unihiker import GUI
gui = GUI()
# color styles
green="#02fc9c"
red="#f71184"
blue="#00eeff" #PAL's blue
orange="#ffa200"

#START PROGRAM
ld=-1
os.system("brightness 100")
#Black background
gui.fill_rect(x=0,y=0,w=240,h=320,color=blue)
#Display loading text (doubled-up to show as bold text)
gui.draw_text(x = 200,y=180,text="PAL v0.1", font_size=32, color="white", angle=270, origin="center")
gui.draw_text(x = 199,y=181,text="PAL v0.1", font_size=32, color="white", angle=270, origin="center")
gui.draw_text(x = 201,y=179,text="PAL v0.1", font_size=32, color="white", angle=270, origin="center")
ld=ld+1
gui.fill_rect(x=150,y=80,w=25,h=200,color=blue)
gui.draw_text(x = 165,y=180,text="LOADING... ("+str(ld)+"/7", font_size=14, color="white", angle=270, origin="center")
gui.draw_text(x = 164,y=181,text="LOADING... ("+str(ld)+"/7", font_size=14, color="white", angle=270, origin="center")

#Loader animation
def load_thread():
    #Create your own 2 color 9 step color ramp in:
    #https://rampgenerator.com/
    while True:
        gui.fill_rect(x=0,y=70,w=65,h=25,color="white")
        time.sleep(1)
        gui.fill_rect(x=0,y=95,w=65,h=25,color="#FFF3DF")
        time.sleep(1)
        gui.fill_rect(x=0,y=120,w=65,h=25,color="#FFE7BF")
        time.sleep(1)
        gui.fill_rect(x=0,y=145,w=65,h=25,color="#FFDC9F")
        time.sleep(1)
        gui.fill_rect(x=0,y=170,w=65,h=28,color="#FFD07F")
        time.sleep(1)
        gui.fill_rect(x=0,y=198,w=65,h=28,color="#FFC45F")
        time.sleep(1)
        gui.fill_rect(x=0,y=226,w=65,h=28,color="#FFB93F")
        time.sleep(1)
        gui.fill_rect(x=0,y=254,w=65,h=28,color="#FFAD1F")
        time.sleep(1)
        gui.fill_rect(x=0,y=282,w=65,h=28,color="#FFA200")
        time.sleep(1)
        gui.fill_rect(x=0,y=50,w=65,h=260,color=blue)
        time.sleep(1)

ld_thread=gui.start_thread(load_thread)


#Wifi restore
def confWifi():
    gui.fill_rect(x=130,y=0,w=15,h=320,color=blue)
    gui.draw_text(x = 140,y=180,text="RESTORING WIFI CONNECTION", font_size=12, color=red, angle=270, origin="center")
    #Create wifi credentials
    f = open("/root/upload/PAL/wifi.txt", "w")
    f.write("802-11-wireless-security.psk:"+wifiPWD)
    f.close()
    #Remove wifi connection and reconnect
    print("Removing WIFI connection")
    os.system('nmcli con delete "wifi"')
    wificreate='nmcli con add con-name "wifi" type wifi ifname wlan0 ssid "'+wifiSSID+'" wifi-sec.key-mgmt wpa-psk ipv4.dns 8.8.8.8,8.8.4.4'
    print("Restoring WIFI connection")
    os.system(wificreate)
    print("Reconnecting WIFI")
    os.system('nmcli con up "wifi" passwd-file /root/upload/PAL/wifi.txt')
    time.sleep(5)

ld=ld+1
gui.fill_rect(x=150,y=80,w=25,h=200,color=blue)
gui.draw_text(x = 165,y=180,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
gui.draw_text(x = 164,y=181,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
#Internet Connection
gui.fill_rect(x=110,y=0,w=35,h=320,color=blue)
gui.draw_text(x = 140,y=180,text="checking WIFI", font_size=12, color="black", angle=270, origin="center")
#Check wifi
wifi=subprocess.getoutput("ifconfig | grep wlan0 | cut -d ',' -f 1")
if(wifi[-2:]=="UP"):
    gui.draw_text(x = 120,y=180,text="OK", font_size=12, color=orange, angle=270, origin="center")
    gui.draw_text(x = 119,y=181,text="OK", font_size=12, color=orange, angle=270, origin="center")
    print("---WIFI OK")
    time.sleep(0.5)
else:
    gui.fill_rect(x=130,y=0,w=15,h=320,color=blue)
    gui.draw_text(x = 140,y=180,text="ERROR IN WIFI CONNECTION", font_size=12, color=red, angle=270, origin="center")
    print("---WIFI ERROR!! Try configuring it again.")
    time.sleep(1)
    gui.fill_rect(x=130,y=0,w=15,h=320,color=blue)
    gui.draw_text(x = 140,y=180,text="RETRYING...", font_size=12, color=orange, angle=270, origin="center")
    gui.draw_text(x = 139,y=181,text="RETRYING...", font_size=12, color=orange, angle=270, origin="center")
    try:
        #Remove wifi connection and reconnect
        confWifi()
        gui.draw_text(x = 120,y=180,text="OK", font_size=12, color=orange, angle=270, origin="center")
        gui.draw_text(x = 119,y=181,text="OK", font_size=12, color=orange, angle=270, origin="center")
        print("---WIFI OK")
        time.sleep(0.5)
    except:
        gui.fill_rect(x=130,y=0,w=15,h=320,color=blue)
        gui.draw_text(x = 140,y=180,text="CONNECTION ERROR", font_size=12, color=red, angle=270, origin="center")
        time.sleep(1)
        gui.draw_text(x = 120,y=180,text="CLOSING PROGRAM", font_size=12, color=orange, angle=270, origin="center")
        time.sleep(2)
        os._exit(0)


ld=ld+1
gui.fill_rect(x=150,y=80,w=25,h=200,color=blue)
gui.draw_text(x = 165,y=180,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
gui.draw_text(x = 164,y=181,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
#Ping dfrobot.com to check connection
gui.fill_rect(x=110,y=0,w=35,h=320,color=blue)
gui.draw_text(x = 140,y=180,text="checking internet connection", font_size=12, color="black", angle=270, origin="center")

def intCon():
    while True:
        ping=subprocess.getoutput("ping dfrobot.com -c 1 | head -n 2 | tail -n 1")
        if ping[-28:]=="Destination Host Unreachable" or ping[-36:]=="Temporary failure in name resolution":
            confWifi()
        else:
            print("---INTERNET OK")
            return False

intCon()

gui.draw_text(x = 120,y=180,text="OK", font_size=12, color=orange, angle=270, origin="center")
gui.draw_text(x = 119,y=181,text="OK", font_size=12, color=orange, angle=270, origin="center")
time.sleep(0.5)


ld=ld+1
gui.fill_rect(x=150,y=80,w=25,h=200,color=blue)
gui.draw_text(x = 165,y=180,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
gui.draw_text(x = 164,y=181,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
#WMO Weather forecast
gui.fill_rect(x=110,y=0,w=35,h=320,color=blue)
gui.draw_text(x = 140,y=180,text="loading climate service", font_size=12, color="black", angle=270, origin="center")
import requests
import json
try:
    climate=requests.get("https://worldweather.wmo.int/en/json/"+CityID+"_en.json").json()
except:
    gui.fill_rect(x=130,y=0,w=15,h=320,color=blue)
    gui.draw_text(x = 140,y=180,text="ERROR IN WMO CONNECTION", font_size=12, color=red, angle=270, origin="center")
    time.sleep(2)
    gui.fill_rect(x=130,y=0,w=15,h=320,color=blue)
    gui.draw_text(x = 140,y=180,text="RETRYING...", font_size=12, color=red, angle=270, origin="center")
    try:
        climate=requests.get("https://worldweather.wmo.int/en/json/"+CityID+"_en.json").json()
    except:
        gui.fill_rect(x=130,y=0,w=15,h=320,color=blue)
        gui.draw_text(x = 140,y=180,text="ERROR IN WMO CONNECTION", font_size=12, color=red, angle=270, origin="center")
        time.sleep(1)
with open('/root/upload/PAL/wmo/icons.json') as ic:
    wmo_ico = json.load(ic)
month=["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
#Climate thread updates weather data every hour
def climate_thread():
    global climate
    #sleep 1 hour
    time.sleep(3600)
    #Program thread loop (loops every 1 second like temp thread, but only recalculates every 1h)
    try:
        climate=requests.get("https://worldweather.wmo.int/en/json/"+CityID+"_en.json").json()
    except:
        print("ERROR IN WMO CONNECTION")

clm_thread=gui.start_thread(climate_thread)
gui.draw_text(x = 120,y=180,text="OK", font_size=12, color=orange, angle=270, origin="center")
gui.draw_text(x = 119,y=181,text="OK", font_size=12, color=orange, angle=270, origin="center")
print("---weather OK")
time.sleep(0.5)


ld=ld+1
gui.fill_rect(x=150,y=80,w=25,h=200,color=blue)
gui.draw_text(x = 165,y=180,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
gui.draw_text(x = 164,y=181,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
#SpeechRecognition
gui.fill_rect(x=110,y=0,w=35,h=320,color=blue)
gui.draw_text(x = 140,y=180,text="loading Speech Recognition", font_size=12, color="black", angle=270, origin="center")
import speech_recognition as sr

#-results array
results=[]
result=[]
temps=[]

#-face animation when message recognized
reconThread=""
def face_thread():
    #Clear screen
    gui.fill_rect(x=0,y=0,w=240,h=320,color=blue)
    #Show background image
    gui.draw_image(x=0, y=0, image='/root/upload/PAL/eyes/PAL_'+eyesB+'.jpg')
    #Show mouth
    gui.fill_rect(x=0,y=50,w=65,h=260,color="white")
    #wait 3 seconds
    time.sleep(3)
    #Restore default face
    #Clear screen
    gui.fill_rect(x=0,y=0,w=240,h=320,color=blue)
    #Show background image
    gui.draw_image(x=0, y=0, image='/root/upload/PAL/eyes/PAL_'+eyesA+'.jpg')
    #Show mouth
    gui.fill_rect(x=0,y=50,w=65,h=260,color="white")
    #stop thread
    gui.stop_thread(reconThread)
def reconFace():
    global reconThread
    reconThread=gui.start_thread(face_thread)

#-voice commands
def comandos(msg):
    # LAMP ON
    if any(keyword in msg for keyword in ["turn on the lamp", "turn the lights on","turn the light on", "turn on the light", "turn on the lights"]):
        turnLAMP("on")
        reconFace()
        os.system("aplay '/root/upload/PAL/mp3/Turn_ON_lights.wav'")

    # LAMP OFF
    elif any(keyword in msg for keyword in ["turn off the lamp","turn the lights off","turn the light off", "turn off the light", "turn off the lights"]):
        turnLAMP("off")
        reconFace()
        os.system("aplay '/root/upload/PAL/mp3/Turn_OFF_lights.wav'")

    # SHOW WEATHER
    elif any(keyword in msg for keyword in ["weather", "the weather", "show me the weather", "tell me the weather", "what is the weather", "what's the weather","what's the weather liked", "weather like", "wether like"]):
        reconFace()
        os.system("aplay '/root/upload/PAL/mp3/Showing_weather.wav'")
        time.sleep(2)
        temp_program()

def turnLAMP(s):
    if(lampBrand=="Shelly25"):
        requests.get("http://"+lampIP+"/relay/"+lampChannel+"?turn="+s)

gui.draw_text(x = 120,y=180,text="OK", font_size=12, color=orange, angle=270, origin="center")
gui.draw_text(x = 119,y=181,text="OK", font_size=12, color=orange, angle=270, origin="center")
print("---SpeechRecognition OK")
time.sleep(0.5)

ld=ld+1
gui.fill_rect(x=150,y=80,w=25,h=200,color=blue)
gui.draw_text(x = 165,y=180,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
gui.draw_text(x = 164,y=181,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
#UNIHIKER pinpong
gui.fill_rect(x=110,y=0,w=35,h=320,color=blue)
gui.draw_text(x = 140,y=180,text="loading pinpong library", font_size=12, color="black", angle=270, origin="center")
from pinpong.libs.dfrobot_bmp280 import BMP280
from pinpong.extension.unihiker import *
from pinpong.board import Board,Pin
gui.draw_text(x = 120,y=180,text="OK", font_size=12, color=orange, angle=270, origin="center")
gui.draw_text(x = 119,y=181,text="OK", font_size=12, color=orange, angle=270, origin="center")
print("---pinpong OK")
time.sleep(0.5)


ld=ld+1
gui.fill_rect(x=150,y=80,w=25,h=200,color=blue)
gui.draw_text(x = 165,y=180,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
gui.draw_text(x = 164,y=181,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
# Initialize UNIHIKER board. It freezes the display while loading.
gui.fill_rect(x=110,y=0,w=35,h=320,color=blue)
gui.draw_text(x = 140,y=180,text="starting board", font_size=12, color="black", angle=270, origin="center")

Board().begin()
# Set Pin P25 as an output pin for the LED "L"
led = Pin(Pin.P25, Pin.OUT)
gui.draw_text(x = 120,y=180,text="OK", font_size=12, color=orange, angle=270, origin="center")
gui.draw_text(x = 119,y=181,text="OK", font_size=12, color=orange, angle=270, origin="center")
time.sleep(0.5)


ld=ld+1
gui.fill_rect(x=150,y=80,w=25,h=200,color=blue)
gui.draw_text(x = 165,y=180,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
gui.draw_text(x = 164,y=181,text="LOADING... ("+str(ld)+"/7)", font_size=14, color="white", angle=270, origin="center")
# Start BMP280 temperature sensor
gui.fill_rect(x=110,y=0,w=35,h=320,color=blue)
gui.draw_text(x = 140,y=180,text="activating temperature sensor", font_size=12, color="black", angle=270, origin="center")
try:
    if(room_temp==0):
        gui.draw_text(x = 119,y=181,text="NO SENSOR FOUND", font_size=12, color=orange, angle=270, origin="center")
        print("---BMP280 IS NOT INSTALLED")
        time.sleep(0.5)
    else:
        bmp2801 = BMP280(mode = 1)
        bmp2801.begin()
        gui.draw_text(x = 119,y=181,text="OK", font_size=12, color=orange, angle=270, origin="center")
        print("---BMP280 OK")
        time.sleep(0.5)
except:
    bmp2801 = 0
    gui.fill_rect(x=110,y=0,w=35,h=320,color=blue)
    gui.draw_text(x = 120,y=180,text="ERROR IN I2C CONNECTION", font_size=12, color=red, angle=270, origin="center")
    time.sleep(2)
gui.fill_rect(x=110,y=0,w=35,h=320,color=blue)
gui.draw_text(x = 140,y=180,text="COMPLETED CONFIGURATION", font_size=12, color=orange, angle=270, origin="center")
gui.draw_text(x = 139,y=181,text="COMPLETED CONFIGURATION", font_size=12, color=orange, angle=270, origin="center")
print("-CONFIGURATION DONE")
time.sleep(1)

#Stop loader animation
gui.stop_thread(ld_thread)

#Power saving after 30seconds of call. Called in a thread, so its killed every time.
def power_save():
    time.sleep(30)
    os.system("brightness 1")
    gui.stop_thread(pwr_thread)

#Run power saving thread if activated
if ps_mode==1:
    pwr_thread=gui.start_thread(power_save)

btnA=0

def shutdown_menu():
    global btnA
    #activate menu if deactivated
    if btnA==0:
        btnA=1
        gui.fill_rect(x=120,y=94,w=95,h=180,color="black")
        gui.draw_rect(x=120,y=94,w=95,h=180,width=1, color="white")
        gui.draw_text(x=200, y=185, text="EXIT?", font_size=16, color=red, angle=270, origin="center")
        gui.draw_text(x=201, y=184, text="EXIT?", font_size=16, color=red, angle=270, origin="center")
        gui.fill_rect(x=140,y=115,w=30,h=60,color="white")
        gui.draw_text(x=155, y=146, text="YES", font_size=14, angle=270, origin="center", color="black",onclick=lambda: os._exit(0))
        gui.fill_rect(x=140,y=195,w=30,h=60,color="white")
        gui.draw_text(x=155, y=225, text="NO", font_size=14, angle=270, origin="center", color="black",onclick=menu_btns)
    #deactivate menu if activated
    elif btnA==1:
        btnA=0
        menu_btns()

#shtdwn_thread=gui.start_thread(shutdown_menu)
gui.on_a_click(shutdown_menu)

def rst_bright():
    global pwr_thread
    #restore brightness
    if(pwr_thread):
        gui.stop_thread(pwr_thread)
    os.system("brightness 100")
    #restore thread callback
    pwr_thread=gui.start_thread(power_save)

#Voice recognition setup at start
listen=""
def record_and_convert():
    global result
    global listen
    #Speech to text
    r = sr.Recognizer()
    m = sr.Microphone()
    
    r.energy_threshold = 125
    r.dynamic_energy_threshold = False
    '''
    try:
        with m as source:
            r.adjust_for_ambient_noise(source, duration=1)
    except:
        print("FAILED to adjust ambient noise")
    '''
    listen=r.listen_in_background(m,rec_callback,phrase_time_limit=4)

#Background voice recognition called at start
def rec_callback(recognizer,audio):
    global activate
    try:
        #start recognizing
        result=recognizer.recognize_google(audio, language="en-GB", show_all=True)
        if result == []:
            print("Empty result")
        else:
            print(result)
            print(result["alternative"])
            result=result["alternative"]
            print(result)
            #now check for the activation word
            indicate_mic()
            #check in every recognised phrase
            for i,r in enumerate(result):
                ok=0
                print(r["transcript"])
                result2=r["transcript"]
                if any(a in result2 for a in activate):
                    turnLED("on")
                    buzzer.pitch(3000, 1)
                    os.system("aplay '/root/upload/ultron/mp3/ding.wav'")
                    results_array(result2)
                    #on first match, run command and exit loop
                    comandos(result2)
                    ok=1
                if ok == 1:
                    break
    
        #restore empty result
        result=[]
        turnLED("off")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def results_array(r):
    if len(results) < 10:
        #add to the first place in the array
        results.insert(0,r)
    else:
        #if more than ten, add to the first place, then remove the last
        results.insert(0,r)
        results.pop(10)

def draw_results():
    #Clean previous results
    gui.fill_rect(x = 0,y=70,w=205,h=250, color="black")
    for n,r in enumerate(results):
        gui.draw_text(x = (225-15*(n+1)),y=70,text=r, font_size=12, color="white", origin='top_left', angle=270)

def indicate_mic():
    gui.fill_rect(x=0,y=50,w=65,h=260,color=orange)
    time.sleep(1)
    gui.fill_rect(x=0,y=50,w=65,h=260,color="white")

def voice_program():
    #Black background
    gui.fill_rect(x=0,y=0,w=240,h=320,color="black")
    #Title draw
    gui.draw_text(x = 233,y=70,text="RECONOCIMIENTO DE VOZ", font_size=12, color=green, angle=270, origin="top_left")
    draw_results()

def cls_temp():
    global tmp_thread
    print("Closing climate program")
    os.system("brightness 100")
    gui.stop_thread(tmp_thread)
    menu_btns()
    
#climate program shows weather data
def clm_program():
    global climate
    #Program thread loop (loops every 1 second like temp thread, but only recalculates every 1h)
    #Blue background
    gui.fill_rect(x=95,y=0,w=113,h=320,color=blue)
    #Show mouth
    gui.fill_rect(x=0,y=50,w=65,h=260,color="white")
    #Show initial weather
    #Todays icon in the middle
    ico_file=int(climate["city"]["forecast"]["forecastDay"][0]["weatherIcon"]/100)
    #play weather audio
    wmo_audio(ico_file)
    #find image file
    ico_file=wmo_ico(ico_file,0)
    gui.draw_image(x=150, y=150, w=60, h=80, image="/root/upload/PAL/wmo/"+ico_file+".png")
    #Todays maximum in red
    gui.draw_text(x=190,y=230,text=climate["city"]["forecast"]["forecastDay"][0]["maxTemp"], font_size=12, color=red, angle=270, origin="left")
    #Todays minimum in blue
    gui.draw_text(x=170,y=230,text=climate["city"]["forecast"]["forecastDay"][0]["minTemp"], font_size=12, color="white", angle=270, origin="left")
        #Date on right, duplicated for bold
    gui.draw_text(x=215,y=90,text=climate["city"]["forecast"]["forecastDay"][0]["forecastDate"][-2:], font_size=14, color="black", angle=270, origin="top_left")
    gui.draw_text(x=214,y=91,text=climate["city"]["forecast"]["forecastDay"][0]["forecastDate"][-2:], font_size=14, color="black", angle=270, origin="top_left")
    gui.draw_text(x=197,y=90,text=month[int(climate["city"]["forecast"]["forecastDay"][0]["forecastDate"][-5:-3])-1], font_size=14, color="black", angle=270, origin="top_left")
    gui.draw_text(x=196,y=91,text=month[int(climate["city"]["forecast"]["forecastDay"][0]["forecastDate"][-5:-3])-1], font_size=14, color="black", angle=270, origin="top_left")
    gui.draw_text(x=180,y=90,text=climate["city"]["forecast"]["forecastDay"][0]["forecastDate"][0:4], font_size=14, color="black", angle=270, origin="top_left")
    gui.draw_text(x=179,y=91,text=climate["city"]["forecast"]["forecastDay"][0]["forecastDate"][0:4], font_size=14, color="black", angle=270, origin="top_left")
    
    #Tomorrow icon in the middle
    day=1
    ico_file=int(climate["city"]["forecast"]["forecastDay"][day]["weatherIcon"]/100)
    ico_file=wmo_ico(ico_file,day)
    gui.draw_image(x=120, y=110, w=30, h=40, image="/root/upload/PAL/wmo/"+ico_file+".png")
        #Date below
    gui.draw_text(x=119,y=122,text=climate["city"]["forecast"]["forecastDay"][day]["forecastDate"][-2:], font_size=8, color="black", angle=270, origin="top_left")
        #min temp
    gui.draw_text(x=135,y=100,text=climate["city"]["forecast"]["forecastDay"][day]["minTemp"], font_size=8, color="white", angle=270, origin="top_left")
        #max temp
    gui.draw_text(x=150,y=145,text=climate["city"]["forecast"]["forecastDay"][day]["maxTemp"], font_size=8, color=red, angle=270, origin="top_left")

    #2-after tomorrow icon in the middle
    day=2
    ico_file=int(climate["city"]["forecast"]["forecastDay"][day]["weatherIcon"]/100)
    ico_file=wmo_ico(ico_file,day)
    gui.draw_image(x=120, y=170, w=30, h=40, image="/root/upload/PAL/wmo/"+ico_file+".png")
        #Date below
    gui.draw_text(x=119,y=182,text=climate["city"]["forecast"]["forecastDay"][day]["forecastDate"][-2:], font_size=8, color="black", angle=270, origin="top_left")
        #min temp
    gui.draw_text(x=135,y=160,text=climate["city"]["forecast"]["forecastDay"][day]["minTemp"], font_size=8, color="white", angle=270, origin="top_left")
        #max temp
    gui.draw_text(x=150,y=205,text=climate["city"]["forecast"]["forecastDay"][day]["maxTemp"], font_size=8, color=red, angle=270, origin="top_left")

    #3-after tomorrow icon in the middle
    day=3
    ico_file=int(climate["city"]["forecast"]["forecastDay"][day]["weatherIcon"]/100)
    ico_file=wmo_ico(ico_file,day)
    gui.draw_image(x=120, y=230, w=30, h=40, image="/root/upload/ultron/wmo/"+ico_file+".png")
        #Date below
    gui.draw_text(x=119,y=242,text=climate["city"]["forecast"]["forecastDay"][day]["forecastDate"][-2:], font_size=8, color="black", angle=270, origin="top_left")
        #min temp
    gui.draw_text(x=135,y=220,text=climate["city"]["forecast"]["forecastDay"][day]["minTemp"], font_size=8, color="white", angle=270, origin="top_left")
        #max temp
    gui.draw_text(x=150,y=265,text=climate["city"]["forecast"]["forecastDay"][day]["maxTemp"], font_size=8, color=red, angle=270, origin="top_left")
    #Close button placed on right
    cls_btn=gui.draw_image(x=135, y=230, w=75, h=75, image="/root/upload/PAL/eyes/alpha-btn_S.png", onclick=cls_temp)

def wmo_audio(i):
    if i==2 or i==9 :
        #Tormenta
        os.system("aplay '/root/upload/PAL/mp3/T_storm.wav'")
    elif 10 <= i <= 15 :
        #Llueve
        os.system("aplay '/root/upload/PAL/mp3/T_rainning.wav'")
    elif 20 <= i <= 23 :
        #Nublado
        os.system("aplay '/root/upload/PAL/mp3/T_cloudy.wav'")
    elif i==24 :
        #Despejado
        os.system("aplay '/root/upload/PAL/mp3/T_sky-clear.wav'")
    elif i==29 or i==32 or i==34 :
        #Frio
        os.system("aplay '/root/upload/PAL/mp3/T_freezing.wav'")
    elif i==31 or i==33 :
        #Calor
        os.system("aplay '/root/upload/PAL/mp3/T_hot.wav'")

def temp_program():
    #Program launch
    #Black background
    gui.fill_rect(x=0,y=0,w=240,h=320,color=blue)
    #Add room temperature on bottom
    gui.fill_rect(x=60,y=70,w=35,h=200,color="white")
    #gui.draw_text(x=143,y=48,text="Room(ºC)", font_size=9, color=green, angle=345, origin="top_left")
    #Add weather in middle
    #City name on top (triplicated for bold effect)
    gui.draw_text(x=234,y=180,text=climate["city"]["cityName"], font_size=16, color="black", angle=270, origin="top")
    gui.draw_text(x=235,y=180,text=climate["city"]["cityName"], font_size=16, color="black", angle=270, origin="top")
    gui.draw_text(x=234,y=181,text=climate["city"]["cityName"], font_size=16, color="black", angle=270, origin="top")

    #Start temperature thread
    global tmp_thread
    tmp_thread=gui.start_thread(temp_thread)
    #Display weather
    clm_program()

def wmo_ico(i,d):
    #check if icon has day/night variation
    if(21 <= i <= 24):
        #suffix=climate["city"]["forecast"]["forecastDay"][d]["weatherIcon"]-i*100
        daytime=time.gmtime().tm_hour
        if 7 <= daytime <= 19:
            daytime="a"
        else:
            daytime="b"
        i=str(i)+daytime
    return str(i)

def temp_thread():
    #Program thread loop
    while True:
        #Only in BMP280 is installed
        if(room_temp==0):
            temp="E"
        else:
            try:
                temp=str(int(bmp2801.temp_c()))
            except:
                temp="E"
        temp_array(temp)

        gui.fill_rect(x=60,y=70,w=35,h=200,color="white")
            #room temperature duplicated for bold effect
        if temp=="E":
            gui.draw_text(x=85,y=183,text=temp, font_size=12, color=red, angle=270, origin="center")
            gui.draw_text(x=86,y=184,text=temp, font_size=12, color=red, angle=270, origin="center")
        else:
            gui.draw_text(x=85,y=183,text=temp, font_size=12, color="black", angle=270, origin="center")
            gui.draw_text(x=86,y=184,text=temp, font_size=12, color="black", angle=270, origin="center")
            #brightness transparent button
        gui.draw_image(x=70, y=150, w=180, h=80, image="/root/upload/PAL/eyes/alpha-btn_L.png", onclick=rst_bright)
        time.sleep(5)

def temp_array(t):
    if len(temps) < 2:
        #add to the first place in the array
        temps.insert(0,t)
    else:
        #if more than two, add to the first place, then remove the last
        temps.insert(0,t)
        temps.pop(2)

def turnLED(s):
    if s == "on":
        led.write_digital(1)
    elif s == "off":
        led.write_digital(0)

#LOAD MENUS
#Load transparent menu buttons
def menu_btns():
    #Black background - Clear screen
    gui.fill_rect(x=0,y=0,w=240,h=320,color=blue)
    #Show background image
    gui.draw_image(x=0, y=0, image='/root/upload/PAL/eyes/PAL_'+eyesA+'.jpg')
    #Show mouth
    gui.fill_rect(x=0,y=50,w=65,h=260,color="white")
    #Draw transparent buttons
    menu_left=gui.draw_image(x=135, y=75, w=75, h=75, image="/root/upload/PAL/eyes/alpha-btn_S.png", onclick=temp_program)
    menu_cntr=gui.draw_image(x=70, y=150, w=180, h=80, image="/root/upload/PAL/eyes/alpha-btn_L.png", onclick=rst_bright)
    menu_right=gui.draw_image(x=135, y=230, w=75, h=75, image="/root/upload/PAL/eyes/alpha-btn_S.png", onclick=lambda: print("click en cuadrado DER"))

def main_menu():
    #Restart brightness thread
    rst_bright()
    #Pop menu window
    #partially clear screen
    gui.fill_rect(x=80,y=90,w=140,h=190,color="black")
    #Draw frame
    gui.draw_rect(x=80,y=90,w=140,h=190,width=4,color="white")
    #Draw title background
    gui.fill_rect(x=220,y=91,w=19,h=188,color="green")

    #Close menu
    cls_btn=gui.draw_image(x=135, y=230, w=75, h=75, image="/root/upload/PAL/eyes/alpha-btn_S.png", onclick=menu_btns)

menu_btns()

if __name__ == "__main__":
    #Play initial message
    reconFace()
    os.system("aplay '/root/upload/PAL/mp3/Program_started.wav'")
    #Launch voice recognition
    record_and_convert()
    
    #Refresh listener and check internet every hour
    def webThread():
        global listen
        while True:
            print("Started web refresh thread")
            time.sleep(3600)
            #play indicative sound
            buzzer.pitch(3000, 1)
            #internet connection
            intCon()
            #listener stop
            print("Stopping listener")
            listen(wait_for_stop=False)
            #listener start
            print("Restarting listener")
            record_and_convert()
            print("Internet and listener refreshed. Restarting thread loop")

    web_thread=gui.start_thread(webThread)
    while True:
        time.sleep(1)
