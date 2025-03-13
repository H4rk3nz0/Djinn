import threading, signal
import os, argparse

from lib import DjinnServer, Util
from gspy import gspy

# Simple argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('-d','--debug', help='Enable Verbose Log Output', action='store_true', default=False)
parser.add_argument('-n','--name', help='Engagement/Client Name (Creating separate db file names)', default='default')
parser.add_argument("-p", "--port", type=int, help="The GraphSpy port (Default: 5000)", default=5000)
parser.add_argument("-i","--interface", type=str, help="GraphSpy interface (Default: 127.0.0.1)", default='127.0.0.1')
argsp = parser.parse_args()

# Initilize imports
djinnserver = DjinnServer.djinnserver(argsp)
util = Util.util()

code_tracker = {}

class djinn:
	def __init__(self):
		#self.check_uid()
		self.djinnserverThread = threading.Thread(target=djinnserver.run, args=(code_tracker,))
		self.djinnserverThread.start()
		self.gspyThread = threading.Thread(target=gspy.run, args=(argsp,))
		self.gspyThread.start()
		for sig in [signal.SIGTERM, signal.SIGABRT, signal.SIGINT]:
			signal.signal(sig, self.sig_handler)

	def check_uid(self):
		if os.getuid() != 0:
			util.print_f('Please run with sudo')
			exit()

	# Register interrup/shutdown handling and cleaning
	def sig_handler(self, sig, frame):
		util.print_w('Shutting Down Djinn Server & Cleaning, Please Wait ...')
		djinnserver.stop()
		self.djinnserverThread.join()
		gspy.stop()
		self.gspyThread.join()

djinn()
