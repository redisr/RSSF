import os
import time

while 1:
	ini = time.time()
	os.system("python sendtoserver.py")
	fim = time.time()
	time.sleep(600-(fim-ini))
