import RPi.GPIO as GPIO
import dht11
import time
import datetime

import tplink

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=4)

print('order: モニタリング開始')

#モニタリング開始時プラグがオフの場合の処理
info = tplink.TPLink_Plug('192.168.0.122').info_dict()
on_off_info = info['system']['get_sysinfo']['relay_state']

if on_off_info == 1:
    result = instance.read()
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))

        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
        
        if result.humidity > 60:
            tplink.TPLink_Plug('192.168.0.122').off()
            print('order: 電源OFF')

try:
    while True:
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))

            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            
            info = tplink.TPLink_Plug('192.168.0.122').info_dict()
            on_off_info = info['system']['get_sysinfo']['relay_state']
            
            if on_off_info == 0:            
                if result.humidity < 40:
                    tplink.TPLink_Plug('192.168.0.122').on()
                    print('order: 電源ON')
            
            if on_off_info == 1:            
                if result.humidity > 60:
                    tplink.TPLink_Plug('192.168.0.122').off()
                    print('order: 電源OFF')

        time.sleep(1)

except KeyboardInterrupt:
    
    info = tplink.TPLink_Plug('192.168.0.122').info_dict()
    on_off_info = info['system']['get_sysinfo']['relay_state']
    
    #モニタリング終了時プラグがオンの場合の処理
    if on_off_info == 1:
        tplink.TPLink_Plug('192.168.0.122').off()
        print('\norder: モニタリング終了 電源OFF')
        
    else:
        print('\norder: モニタリング終了')

    print("Cleanup")
    GPIO.cleanup()