#! /usr/bin/python

# Import and init an XBee device
import serial
from xbee import ZigBee
from binascii import b2a_hex
import sys

arq= open("log_porta_ttyAMA0.txt", 'w+')
 
def plaintext(texto):
	linha="\nSN: "+b2a_hex(texto['source_addr_long'])+"\nCampos do frame(lumi/temp/humi): "+str(texto['samples'][0]['adc-1'])+"/"+str(texto['samples'][0]['adc-2'])+"/"+str(texto['samples'][0]['adc-3'])
	arq.write(linha)

def con():
	ser = serial.Serial('/dev/ttyAMA0', 9600)

	# Use an XBee 802.15.4 device
	# To use with an XBee ZigBee device, replace with:
	xbee = ZigBee(ser)
	#xbee = XBee(ser)
	while(1):
		try:
			print "lendo frame"
			texto = xbee.wait_read_frame()
			print "frame: ",texto
			
			plaintext(texto)
		except KeyboardInterrupt:
			arq.close()
			ser.close()     
     
if __name__ == "__main__":
	con()
