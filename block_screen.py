import subprocess
import os


class ScreenBlocker:
	def get_username(self):
		return os.environ["USER"]

	def get_active_sessions(self):
		out = subprocess.Popen(['loginctl', 'list-sessions'], stdout=subprocess.PIPE)
		lines = out.stdout.readlines()
		return [sess.decode().split() for sess in lines[1:len(lines)-2]]

	def lock_session(self):
		name = self.get_username()
		for session in self.get_active_sessions():
			if session[2] == name:
				subprocess.Popen(["loginctl", "lock-session", session[0]])
