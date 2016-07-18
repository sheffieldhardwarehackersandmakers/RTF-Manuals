#!/usr/bin/python
#Read AM2320 digital temperature/humidity sensor using I2C mode
#Tested at I2C bus speed of 10kHz

import time
#download pigpio from abyz.co.uk/rpi/pigpio/index.html
#make sure pigpio daemon is started already using "sudo pigpiod"
import pigpio
#create instance on localhost
pi1=pigpio.pi()

#open i2c bus, specify bus and slave address
I2CBUS=1
I2CADDR=0x5C
handle=pi1.i2c_open(I2CBUS,I2CADDR)
#use handle for subsequent i2c commands and close handle when finished

#AM2320 goes to sleep after 3 seconds
#Wake up AM2320 by doing a quick write to slave address 0x5C.  The AM2320 will NOT acknowledge so this
#will generate an IO exception that will be silently ignored.
pigpio.exceptions = False
#Quick write to slave address, R/W# bit set to 0
pi1.i2c_write_quick(handle,0)
pigpio.exceptions = True

#Wait 800us
time.sleep(.001)

#AM2320 will now be awake and generate ACKs normally
#Write to slave address and send 0x03, 0x00, 0x04
#Modbus function code 0x03 is to read registers, 0x00 is the start register, 0x04 is the number of registers
#Could have used pi1.i2c_write_word_data(handle,0x03,0x0400)
pi1.i2c_write_device(handle,[0x03,0x00,0x04])

#Wait 1.5ms
time.sleep(.0015)

#Read out 8 bytes of data
#Byte 0: Should be Modbus function code 0x03
#Byte 1: Should be number of registers to read (0x04)
#Byte 2: Humidity high 8 bits
#Byte 3: Humidity low 8 bits
#Byte 4: Temperature high 8 bits
#Byte 5: Temperature low 8 bits
#Byte 6: CRC high byte
#Byte 7: CRC low byte
(count,data)=pi1.i2c_read_device(handle,8)

pi1.i2c_close(handle)

humidity = data[2]<<8|data[3]
print("Humidity (%) = "),
print(humidity/10.0)
#MSB of temperature high 8 bits is the sign bit
temperature = data[4]<<8 | data[5]
if((data[4] & 0x80) != 0):
    temperature = -(temperature & 0x7FFF)   
print("Temperature (C) = "),
print(temperature/10.0)
print("Temperature (F) = "),
print(temperature/10.0*1.8+32)
