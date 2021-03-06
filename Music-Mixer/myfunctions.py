import wave, pyaudio as pa, tkinter as tk, numpy as np, os, time
from struct import *
import math
from matplotlib import pyplot as plt
from scipy import signal
# from pygame import mixer
import threading
from tkinter import filedialog
from PIL import Image
from PIL import GifImagePlugin
from random import randint
import shutil

# init
height = 600
width  = 800
window = tk.Tk()

index1 = 0
index2 = 0
wavefile1 = 'uploads/ThereForYou.wav'
wavefile2 = 'uploads/Tired.wav'

pre_wavefile1 = wavefile1
pre_wavefile2 = wavefile2

on = False
off = False
save = False
q = False # quit

WAVE_OUTPUT_FILENAME = "results/mixer.wav"

audio_play = tk.BooleanVar()
audio_stop_play = tk.BooleanVar()
audio_play.set(False)
audio_stop_play.set(False)

music_playing = tk.BooleanVar()
music_playing.set(False)

animation_flag = tk.BooleanVar()
animation_flag.set(False)

def play_audio_w_animation():
    # animation_flag.set(True)
    music_playing.set(True)
    audio_play.set(True)
    audio_stop_play.set(False)

# get the status of on flag

def get_on():
    return on

# turn off the current music
def get_off():
    return off

def get_save():
    return save

def get_quit():
    return q

def set_on_false():
    global on
    on = False

def set_off_false():
    global off
    off = False

def set_save_false():
    global save
    save = False

# pause the playing music
def pause():
    global on
    music_playing.set(False)
    audio_play.set(False)
    # audio_stop_play.set(True)
    on = False
# resume the paused music
def resume():
    global on
    global off
    on = True
    off = False

# set the save flag to output music
def savefile():
    global save
    save = True

# stop the whole program
def stop():
    global off
    off = True
    animation_flag.set(False)
    audio_stop_play.set(True)




def clip16( x ):
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return x

# get file path  
left_path = tk.StringVar()
right_path = tk.StringVar()
def right_selectPath():
    path_ = filedialog.askopenfilename()
    right_path.set(path_)
    wavefile2 = path_

# speedup and slowdown function
times1 = tk.StringVar()
times1.set(1.0)
def speedup1():
	times1.set(float(times1.get())*2)
	if(float(times1.get()) > 8):
		times1.set(1.0)
def slowdown1():
	times1.set(float(times1.get())/2)
	if(float(times1.get()) < 0.5):
		times1.set(0.5)

times2 = tk.StringVar()
times2.set(1.0)
def speedup2():
	times2.set(float(times2.get())*2)
	if(float(times2.get()) > 8):
		times2.set(1.0)
def slowdown2():
	times2.set(float(times2.get())/2)
	if(float(times2.get()) < 0.5):
		times2.set(0.5)

# volumn adjust functions
song1_volumn = tk.IntVar()
song2_volumn = tk.IntVar()
song1_volumn.set(100)
song2_volumn.set(100)
def volumn1(event):
    print(song1_volumn.get() )

def volumn2(event):
    print(song2_volumn.get())


# save file
def save_file():
    # f = tk.filedialog.asksaveasfile(mode = 'w', defaultextension = '.wav')
    # if f is None:
    #     return
    # output_string = 1
    # f.write(output_string)
    # f.close()
    global WAVE_OUTPUT_FILENAME
    WAVE_OUTPUT_FILENAME = tk.filedialog.asksaveasfilename(defaultextension = '.wav')
    global save
    save = True


# index is a global var to index where is the current play index
# on is a global var to control the on/off the music
# W is a global var to control the vibration of the music (the bigger the more vibrating)
# gain is a global var to control the volume of music





