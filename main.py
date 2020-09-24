import pyudev
import threading
import time
import sys

from block_screen import ScreenBlocker

class USBDetector():
	def __init__(self):
		thread = threading.Thread(target=self._work)
		thread.daemon = True
		thread.start()
	 
	def _work(self):
		self.context = pyudev.Context()
		self.monitor = pyudev.Monitor.from_netlink(self.context)
		self.monitor.filter_by(subsystem='usb')
		self.monitor.start()
		for device in iter(self.monitor.poll, None):
			if device.action == 'add':
				self.on_add()
			elif device.action == 'remove':
				self.on_remove()

	@staticmethod
	def on_add():
		print("Inserted")
		ScreenBlocker().lock_session()

	@staticmethod
	def on_remove():
		print("Removed")


usb = USBDetector()

while True:
	try:
		time.sleep(10)
	except KeyboardInterrupt:
		print("Good Bye")
		sys.exit(1)