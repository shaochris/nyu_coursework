from myfunctions import *

class song(object):
	"""docstring for song"""
	def __init__(self):
		super(song, self).__init__()
		filename = './uploads/ThereForYou.wav'
		paused = False
		
	def play_music():
		global paused
		if paused:
			mixer.music.unpause()
			paused = False
		else:
			mixer.music.load(filename)
			mixer.music.play()

	def stop_music():
	    mixer.music.stop()

	def pause_music():
		global paused
		pause = True
		mixer.music.pause()

s1 = song()
song.play_music()