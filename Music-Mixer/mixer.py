from myfunctions import *

####################################### initial #######################################
regular = False
vibrate = False
filter = False
echo = True

frames = []

def quit_program():
    global CONTINUE
    print('Good Bye')
    CONTINUE = False

def changeloop():
    if audio_loop.get() == True:
        audio_loop.set(False)
        loop_var.set("no loop")
    else:
        audio_loop.set(True)
        loop_var.set("loop")

s_partiality1 = tk.IntVar()
s_partiality2 = tk.IntVar()

loop_var = tk.StringVar()
loop_var.set("no loop")
audio_loop = tk.BooleanVar()

gain0 = tk.DoubleVar()
gain1 = tk.DoubleVar()
# initial
s_partiality1.set(50)
s_partiality2.set(50)
gain1.set(0.5)
gain0.set(0.5)
audio_loop.set(False)

# Main Window

window.geometry("800x600+0+100") # +350+100
window.configure(background = 'black')
window.winfo_toplevel().title("Music Mixer")
####################################### Bottom Panel #######################################
song_select_panel = tk.Frame(window)
song_select_panel.configure(background = 'black', width = width, height = height/2)
song_select_panel.pack(side = tk.BOTTOM, expand = True, fill = tk.BOTH, padx = 25)

# uploaded file path can be get by `left_path.get()` | `right_path.get()`
upload_panel = tk.Frame(song_select_panel)
upload_panel.configure(background = 'black')
upload_panel.pack(fill = tk.BOTH, pady = 5)

#
# # right song upload
# tk.Button(upload_panel, bg = 'black', fg = 'grey', text = 'Upload', command = right_selectPath).pack(side = tk.RIGHT)
# tk.Entry(upload_panel,  bg = 'black', fg = 'grey', textvariable = right_path).pack(side = tk.RIGHT)
# tk.Label(upload_panel,  bg = 'black', fg = 'grey', text = 'Choose your own:').pack(side = tk.RIGHT)

# click item on the list would get its name as
left_song_list = tk.Frame(song_select_panel)
left_song_list.configure(background = 'black')
left_song_list.pack(side = tk.LEFT, expand = True, fill = tk.BOTH, padx = 25, pady = 5)

left_flist = os.listdir('uploads')
left_lbox = tk.Listbox(left_song_list, background = 'black', fg = '#EF7E31', selectbackground = 'blue', exportselection=0)

right_song_list = tk.Frame(song_select_panel)
right_song_list.configure(background = 'black')
right_song_list.pack(side = tk.RIGHT, expand = True, fill = tk.BOTH, padx = 25, pady = 5)

right_flist = os.listdir('uploads')
right_lbox = tk.Listbox(right_song_list, background = 'black', fg = '#EF7E31', selectbackground = 'blue', exportselection=0)

def left_selectPath():
    global left_lbox
    path_ = filedialog.askopenfilename()
    left_path.set(path_)
    # wavefile1 = path_
    shutil.copy(path_, './uploads/')
    left_flist.append(path_)
    temp = path_.split('/')
    left_lbox.insert(tk.END,temp[-1])
    right_lbox.insert(tk.END, temp[-1])

tk.Label(upload_panel,  bg = 'black', fg = 'grey', text = 'Choose your own:').pack(side = tk.LEFT)
tk.Entry(upload_panel,  bg = 'black', fg = 'grey', textvariable = left_path).pack(side = tk.LEFT)
tk.Button(upload_panel, bg = 'black', fg = 'grey', text = 'Upload', command = left_selectPath).pack(side = tk.LEFT)

def left_select_song(event):
    global wavefile1
    # song_name = str(left_lbox.get(left_lbox.curselection()))
    wavefile1 = 'uploads/' + str(left_lbox.get(left_lbox.curselection()))
    print(wavefile1)

left_lbox.bind('<<ListboxSelect>>', left_select_song)
left_lbox.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
for item in left_flist:
    left_lbox.insert(tk.END, item)





def right_select_song(event):
    global wavefile2
    wavefile2 = 'uploads/' + str(right_lbox.get(right_lbox.curselection()))
    print(wavefile2)
right_lbox.bind('<<ListboxSelect>>', right_select_song)
right_lbox.pack(side = tk.RIGHT, fill = tk.BOTH, expand = True)
for item in right_flist:
    right_lbox.insert(tk.END, item)

####################################### Top Panel #######################################
Dashboard = tk.Frame(window)
Dashboard.configure(background = '#292931', width = width, height = height/2)
Dashboard.pack(side = tk.TOP, expand = True, fill = tk.BOTH)


####################################### Left Panel #######################################
left_panel = tk.Frame(Dashboard)
left_panel.configure(background = '#292931', width = 300, height = 200)
left_panel.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)

# image animation
# animation_left = tk.Canvas(left_panel, height = 150, width =300, bg = 'black')
# animation_left.pack(side = tk.RIGHT)
# imageObject = Image.open("./src/images/3.gif")
left_img = tk.PhotoImage(file = './src/images/5.gif')
left_canva = tk.Canvas(left_panel, width = 200, height = 200)
left_canva.configure(bg = '#292931',highlightthickness=0)
left_canva.pack(side = tk.RIGHT)
left_canva.create_image(1,1,image = left_img, anchor = tk.NW)

####################################### Control Panel #######################################

control_panel = tk.Frame(Dashboard)
control_panel.configure(background = '#292931', width = 200, height = 200)
control_panel.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)

# volumn adjust scales
volumn_panel = tk.Frame(control_panel)
volumn_panel.pack()
vol1 = tk.Scale(volumn_panel, highlightthickness = 0, highlightbackground = 'white', showvalue = 0, fg = 'orange', bg = '#292931', variable = gain0, from_ = 1, to = 0, resolution= 0.1, length = 200, width = 50).pack(side = tk.LEFT, ipadx = 10)
vol2 = tk.Scale(volumn_panel, highlightthickness = 0, highlightbackground = 'white', showvalue = 0, fg = 'orange', bg = '#292931', variable = gain1, from_ = 1, to = 0, resolution= 0.1, length = 200, width = 50).pack(side = tk.LEFT, ipadx = 10)

#
filter_mode = tk.StringVar()
filter_mode.set('standard')
om = tk.OptionMenu(control_panel, filter_mode, 'standard', 'vibrato', 'echo', 'filter')
om.configure(fg = 'white',bg = '#292931',highlightthickness=0)
om.pack(pady = 10)


file_control_panel = tk.Frame(control_panel)
file_control_panel.configure(background = 'black')
file_control_panel.pack(side = tk.BOTTOM)

loop_panel = tk.Frame(control_panel)
loop_panel.pack(side = tk.BOTTOM)


# play, pause, stop buttons
play_panel = tk.Frame(control_panel)
play_panel.configure(background = 'black')
play_panel.pack(side = tk.BOTTOM)



tk.Button(file_control_panel, bg = '#292931', fg = 'white', text = 'Save', command = save_file).pack(side = tk.LEFT)
tk.Button(file_control_panel, bg = '#292931', fg = 'white', text = 'Quit', command = quit_program).pack(side= tk.LEFT)

tk.Button(play_panel, bg = '#292931', fg = 'white', text = 'Play', command = play_audio_w_animation).pack(side = tk.LEFT)
tk.Button(play_panel, bg = '#292931', fg = 'white', text = 'Pause', command =  pause).pack(side = tk.LEFT)
tk.Button(play_panel, bg = '#292931', fg = 'white', text = 'Stop', command =  stop).pack(side = tk.LEFT)

tk.Button(file_control_panel, bg = '#292931', fg = 'white', text = 'loop', command = changeloop).pack(side = tk.LEFT)
tk.Label(loop_panel, textvariable = loop_var).pack(side = tk.LEFT)
# tk.Checkbutton(control_panel, bg = '#292931', fg = 'white', text = 'loop', variable = audio_loop, onvalue = True, offvalue = False).pack(side= tk.LEFT)
# tk.Checkbutton(song_select_panel, bg = '#292931', fg = 'white', text = 'loop', variable = audio_loop, onvalue = True, offvalue = False).pack(side= tk.LEFT)
####################################### Right Panel #######################################


right_panel = tk.Frame(Dashboard)
right_panel.configure(background = '#292931', width = 300, height = 200)
right_panel.pack(side = tk.LEFT, expand = True, fill = tk.BOTH)

# animation_right = tk.Canvas(right_panel, height = 150, width =300, bg = 'black')
# animation_right.pack(side = tk.LEFT)

right_img = tk.PhotoImage(file = './src/images/5.gif')
right_canva = tk.Canvas(right_panel, width = 200, height = 200)
right_canva.configure(background = '#292931',highlightthickness=0)
right_canva.pack(side = tk.LEFT)
right_canva.create_image(1,1,image = right_img, anchor = tk.NW)

####################################### main function #######################################



wf1 = wave.open(wavefile1, 'rb')
wf2 = wave.open(wavefile2, 'rb')
# print('left file is ' + wavefile1)
# print('right file is ' + wavefile2)
p = pa.PyAudio()
# Open audio stream
stream = p.open(
    format=pa.paInt16,
    channels=2,
    rate=44100,
    input=False,
    output=True)

index = 0
# music_array1, music_array2 = get_music()
pre_out = [0,0,0,0]

# for echo
b0 = 1.0
delay_sec = 0.05 # 50 milliseconds
N = int( 44100 * delay_sec )
BUFFER_LEN_echo = N              # length of buffer

buffere01 = BUFFER_LEN_echo * [0]
buffere02 = BUFFER_LEN_echo * [0]
buffere03 = BUFFER_LEN_echo * [0]
buffere04 = BUFFER_LEN_echo * [0]
buffere11 = BUFFER_LEN_echo * [0]
buffere12 = BUFFER_LEN_echo * [0]
buffere13 = BUFFER_LEN_echo * [0]
buffere14 = BUFFER_LEN_echo * [0]
buffere21 = BUFFER_LEN_echo * [0]
buffere22 = BUFFER_LEN_echo * [0]
buffere23 = BUFFER_LEN_echo * [0]
buffere24 = BUFFER_LEN_echo * [0]
buffere31 = BUFFER_LEN_echo * [0]
buffere32 = BUFFER_LEN_echo * [0]
buffere33 = BUFFER_LEN_echo * [0]
buffere34 = BUFFER_LEN_echo * [0]

BLOCKLEN = 4

input_bytes1 = wf1.readframes(BLOCKLEN)
input_bytes2 = wf2.readframes(BLOCKLEN)
output_block0 = BLOCKLEN * [0]
output_block1 = BLOCKLEN * [0]
output_block2 = BLOCKLEN * [0]
output_block3 = BLOCKLEN * [0]

# Vibrato parameters
f0 = 2
W = 0.1  # use W = 0 for no effect.

# Difference equation coefficients
a1 = -1.9
a2 = 0.998

# Initialization
y01 = [0.0, 0.0, 0.0, 0.0]
y11 = [0.0, 0.0, 0.0, 0.0]
y21 = [0.0, 0.0, 0.0, 0.0]
y02 = [0.0, 0.0, 0.0, 0.0]
y12 = [0.0, 0.0, 0.0, 0.0]
y22 = [0.0, 0.0, 0.0, 0.0]
y03 = [0.0, 0.0, 0.0, 0.0]
y13 = [0.0, 0.0, 0.0, 0.0]
y23 = [0.0, 0.0, 0.0, 0.0]
y04 = [0.0, 0.0, 0.0, 0.0]
y14 = [0.0, 0.0, 0.0, 0.0]
y24 = [0.0, 0.0, 0.0, 0.0]

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN = 1024  # Set buffer length.
buffer11 = BUFFER_LEN * [0]  # list of zeros
buffer21 = BUFFER_LEN * [0]
buffer31 = BUFFER_LEN * [0]
buffer41 = BUFFER_LEN * [0]
buffer12 = BUFFER_LEN * [0]  # list of zeros
buffer22 = BUFFER_LEN * [0]
buffer32 = BUFFER_LEN * [0]
buffer42 = BUFFER_LEN * [0]
buffer13 = BUFFER_LEN * [0]  # list of zeros
buffer23 = BUFFER_LEN * [0]
buffer33 = BUFFER_LEN * [0]
buffer43 = BUFFER_LEN * [0]
buffer14 = BUFFER_LEN * [0]  # list of zeros
buffer24 = BUFFER_LEN * [0]
buffer34 = BUFFER_LEN * [0]
buffer44 = BUFFER_LEN * [0]

# Initialize buffer indices
kr = int(0.5 * BUFFER_LEN)  # read index
kw = 0  # write index

CONTINUE = True

while CONTINUE:
    window.update()
    # if music_playing.get():
    #     try:
    #         update1 = 'gif -index ' + str(randint(1, imageObject.n_frames-1))
    #         frame1 = tk.PhotoImage(file='./src/images/3.gif', format = update1)
    #         animation_left.create_image(-60, -50, image = frame1, anchor = tk.NW)
    #         update2 = 'gif -index ' + str(randint(1, imageObject.n_frames-1))
    #         frame2 = tk.PhotoImage(file='./src/images/3.gif', format = update2)
    #         animation_right.create_image(-60, -50, image = frame2, anchor = tk.NW)
    #     except RuntimeError:
    #         print('Animation Error')
    if pre_wavefile1 != wavefile1 or pre_wavefile2 != wavefile2:
        wf1 = wave.open(wavefile1, 'rb')
        wf2 = wave.open(wavefile2, 'rb')
        pre_wavefile1 = wavefile1
        pre_wavefile2 = wavefile2
    if audio_play.get() == True and audio_stop_play.get() == False:
        stream.start_stream()
        input_tuple1 = unpack('hh' * BLOCKLEN, input_bytes1)
        input_tuple2 = unpack('hh' * BLOCKLEN, input_bytes2)
        if index < min(int(wf1.getnframes()/4), int(wf2.getnframes()/4)):
            output_value00 = int(clip16(gain0.get() * input_tuple1[0]))
            output_value10 = int(clip16(gain0.get() * input_tuple1[1]))
            output_value20 = int(clip16(gain1.get() * input_tuple2[0]))
            output_value30 = int(clip16(gain1.get() * input_tuple2[1]))
            output_block0 = [output_value00, output_value10, output_value20, output_value30]
            output_value01 = int(clip16(gain0.get() * input_tuple1[2]))
            output_value11 = int(clip16(gain0.get() * input_tuple1[3]))
            output_value21 = int(clip16(gain1.get() * input_tuple2[2]))
            output_value31 = int(clip16(gain1.get() * input_tuple2[3]))
            output_block1 = [output_value01, output_value11, output_value21, output_value31]
            output_value02 = int(clip16(gain0.get() * input_tuple1[4]))
            output_value12 = int(clip16(gain0.get() * input_tuple1[5]))
            output_value22 = int(clip16(gain1.get() * input_tuple2[4]))
            output_value32 = int(clip16(gain1.get() * input_tuple2[5]))
            output_block2 = [output_value02, output_value12, output_value22, output_value32]
            output_value03 = int(clip16(gain0.get() * input_tuple1[6]))
            output_value13 = int(clip16(gain0.get() * input_tuple1[7]))
            output_value23 = int(clip16(gain1.get() * input_tuple2[6]))
            output_value33 = int(clip16(gain1.get() * input_tuple2[7]))
            output_block3 = [output_value03, output_value13, output_value23, output_value33]

            if filter_mode.get() == 'vibrato':

                y01 = buffer11[int(kr)]
                y11 = buffer21[int(kr)]
                y21 = buffer31[int(kr)]
                y31 = buffer41[int(kr)]
                y02 = buffer12[int(kr)]
                y12 = buffer22[int(kr)]
                y22 = buffer32[int(kr)]
                y32 = buffer42[int(kr)]
                y03 = buffer13[int(kr)]
                y13 = buffer23[int(kr)]
                y23 = buffer33[int(kr)]
                y33 = buffer43[int(kr)]
                y04 = buffer14[int(kr)]
                y14 = buffer24[int(kr)]
                y24 = buffer34[int(kr)]
                y34 = buffer44[int(kr)]
                buffer11[kw] = output_block0[0]
                buffer21[kw] = output_block0[1]
                buffer31[kw] = output_block0[2]
                buffer41[kw] = output_block0[3]
                buffer11[kw] = output_block1[0]
                buffer22[kw] = output_block1[1]
                buffer32[kw] = output_block1[2]
                buffer42[kw] = output_block1[3]
                buffer13[kw] = output_block2[0]
                buffer23[kw] = output_block2[1]
                buffer33[kw] = output_block2[2]
                buffer43[kw] = output_block2[3]
                buffer14[kw] = output_block3[0]
                buffer24[kw] = output_block3[1]
                buffer34[kw] = output_block3[2]
                buffer44[kw] = output_block3[3]
                kr = kr + 1 + W * math.sin(2 * math.pi * f0 * index / 44100)
                if kr >= BUFFER_LEN:
                    kr = kr - BUFFER_LEN

                kw = kw + 1
                if kw == BUFFER_LEN:
                    kw = 0
                output_bytes = pack('hh' * BLOCKLEN,
                                    clip16(y01 + y21), clip16(y11 + y31),
                                    clip16(y02 + y22), clip16(y12 + y32),
                                    clip16(y03 + y23), clip16(y13 + y33),
                                    clip16(y04 + y24), clip16(y14 + y34))
                stream.write(output_bytes)
                frames.append(output_bytes)

            if filter_mode.get() == 'standard':
                output_bytes = pack('hh' * BLOCKLEN,
                                    clip16(output_block0[0] + output_block0[2]),
                                    clip16(output_block0[1] + output_block0[3]),
                                    clip16(output_block1[0] + output_block1[2]),
                                    clip16(output_block1[1] + output_block1[3]),
                                    clip16(output_block2[0] + output_block2[2]),
                                    clip16(output_block2[1] + output_block2[3]),
                                    clip16(output_block3[0] + output_block3[2]),
                                    clip16(output_block3[1] + output_block3[3]))
                stream.write(output_bytes)
                frames.append(output_bytes)

            if filter_mode.get() == 'echo':
                y01 = b0 * output_block0[0] + buffere01[0]
                y02 = b0 * output_block0[1] + buffere02[0]
                y03 = b0 * output_block0[2] + buffere03[0]
                y04 = b0 * output_block0[3] + buffere04[0]
                y11 = b0 * output_block1[0] + buffere11[0]
                y12 = b0 * output_block1[1] + buffere12[0]
                y13 = b0 * output_block1[2] + buffere13[0]
                y14 = b0 * output_block1[3] + buffere14[0]
                y21 = b0 * output_block2[0] + buffere21[0]
                y22 = b0 * output_block2[1] + buffere22[0]
                y23 = b0 * output_block2[2] + buffere23[0]
                y24 = b0 * output_block2[3] + buffere24[0]
                y31 = b0 * output_block3[0] + buffere31[0]
                y32 = b0 * output_block3[1] + buffere32[0]
                y33 = b0 * output_block3[2] + buffere33[0]
                y34 = b0 * output_block3[3] + buffere34[0]

                buffere01.append(output_block0[0])
                buffere02.append(output_block0[1])
                buffere03.append(output_block0[2])
                buffere04.append(output_block0[3])
                buffere11.append(output_block1[0])
                buffere12.append(output_block1[1])
                buffere13.append(output_block1[2])
                buffere14.append(output_block1[3])
                buffere21.append(output_block2[0])
                buffere22.append(output_block2[1])
                buffere23.append(output_block2[2])
                buffere24.append(output_block2[3])
                buffere31.append(output_block3[0])
                buffere32.append(output_block3[1])
                buffere33.append(output_block3[2])
                buffere34.append(output_block3[3])

                del buffere01[0]
                del buffere02[0]
                del buffere03[0]
                del buffere04[0]
                del buffere11[0]
                del buffere12[0]
                del buffere13[0]
                del buffere14[0]
                del buffere21[0]
                del buffere22[0]
                del buffere23[0]
                del buffere24[0]
                del buffere31[0]
                del buffere32[0]
                del buffere33[0]
                del buffere34[0]

                output_bytes = pack('hh' * BLOCKLEN,
                                    int(clip16(y01 + y03)), int(clip16(y02 + y04)),
                                    int(clip16(y11 + y13)), int(clip16(y12 + y14)),
                                    int(clip16(y21 + y23)), int(clip16(y22 + y24)),
                                    int(clip16(y31 + y33)), int(clip16(y32 + y34)))
                stream.write(output_bytes)
                frames.append(output_bytes)


            if filter_mode.get() == 'filter':
                y01[0] = output_block0[0] - a1 * y11[0] - a2 * y21[0]
                y01[1] = output_block0[1] - a1 * y11[1] - a2 * y21[1]
                y01[2] = output_block0[2] - a1 * y11[2] - a2 * y21[2]
                y01[3] = output_block0[3] - a1 * y11[3] - a2 * y21[3]
                y02[0] = output_block1[0] - a1 * y12[0] - a2 * y22[0]
                y02[1] = output_block1[1] - a1 * y12[1] - a2 * y22[1]
                y02[2] = output_block1[2] - a1 * y12[2] - a2 * y22[2]
                y02[3] = output_block1[3] - a1 * y12[3] - a2 * y22[3]
                y03[0] = output_block2[0] - a1 * y13[0] - a2 * y23[0]
                y03[1] = output_block2[1] - a1 * y13[1] - a2 * y23[1]
                y03[2] = output_block2[2] - a1 * y13[2] - a2 * y23[2]
                y03[3] = output_block2[3] - a1 * y13[3] - a2 * y23[3]
                y04[0] = output_block3[0] - a1 * y14[0] - a2 * y24[0]
                y04[1] = output_block3[1] - a1 * y14[1] - a2 * y24[1]
                y04[2] = output_block3[2] - a1 * y14[2] - a2 * y24[2]
                y04[3] = output_block3[3] - a1 * y14[3] - a2 * y24[3]

                y21[0] = y11[0]
                y11[0] = y01[0]
                y21[1] = y11[1]
                y11[1] = y01[1]
                y21[2] = y11[2]
                y11[2] = y01[2]
                y21[3] = y11[3]
                y11[3] = y01[3]
                y22[0] = y12[0]
                y12[0] = y02[0]
                y22[1] = y12[1]
                y12[1] = y02[1]
                y22[2] = y12[2]
                y12[2] = y02[2]
                y22[3] = y12[3]
                y12[3] = y02[3]
                y23[0] = y13[0]
                y13[0] = y03[0]
                y23[1] = y13[1]
                y13[1] = y03[1]
                y23[2] = y13[2]
                y13[2] = y03[2]
                y23[3] = y13[3]
                y13[3] = y03[3]
                y24[1] = y14[1]
                y14[1] = y04[1]
                y24[0] = y14[0]
                y14[0] = y04[0]
                y24[2] = y14[2]
                y14[2] = y04[2]
                y24[3] = y14[3]
                y14[3] = y04[3]
                output1 = y01
                output2 = y02
                output3 = y03
                output4 = y04
                output_bytes = pack('hh' * BLOCKLEN,
                                    int(clip16(y01[0] + y01[2])), int(clip16(y01[1] + y01[3])),
                                    int(clip16(y02[0] + y02[2])), int(clip16(y02[1] + y02[3])),
                                    int(clip16(y03[0] + y03[2])), int(clip16(y03[1] + y03[3])),
                                    int(clip16(y04[0] + y04[2])), int(clip16(y04[1] + y04[3])))
                stream.write(output_bytes)
                frames.append(output_bytes)
        else:
            if audio_loop.get() == False:
                print("no loop")
                if get_save() == True:
                    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                    waveFile.setnchannels(2)
                    waveFile.setsampwidth(p.get_sample_size(pa.paInt16))
                    waveFile.setframerate(44100)
                    waveFile.writeframes(b''.join(frames))
                    waveFile.close()
                    print("* Saved File")
                frames.clear()
                set_on_false()
                audio_play.set(False)
                audio_stop_play.set(False)
                set_save_false()
            else:
                print("loop")
            wf1 = wave.open(wavefile1, 'rb')
            wf2 = wave.open(wavefile2, 'rb')
            index = 0
        # output_bytes = pack('hh', output_value0 + output_value2, output_value1 + output_value3)

        input_bytes1 = wf1.readframes(BLOCKLEN)
        input_bytes2 = wf2.readframes(BLOCKLEN)
        index = index + 1
    elif audio_stop_play.get() == True :
        # print('* Stop')
        stream.stop_stream()
        if get_save() == True:
            # animation_flag.set(False)
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(2)
            waveFile.setsampwidth(p.get_sample_size(pa.paInt16))
            waveFile.setframerate(44100)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            print("* Saved File")
        frames.clear()
        wf1 = wave.open(wavefile1, 'rb')
        wf2 = wave.open(wavefile2, 'rb')
        # set_on_false()
        audio_play.set(False)
        audio_stop_play.set(False)
        set_save_false()
        # set_off_false()
    # elif get_quit() == True:
    #     print("* Finish")
    #     window.quit()
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()
    else:
        continue



