from myfunctions import *

regular = False
vibrate = True
filter = False
save = True

WAVE_OUTPUT_FILENAME = "results/mixer.wav"

frames = []

s_partiality1 = tk.IntVar()
s_partiality2 = tk.IntVar()

gain0 = tk.DoubleVar()
gain1 = tk.DoubleVar()
# initial
s_partiality1.set(50)
s_partiality2.set(50)
gain1.set(0.5)
gain0.set(0.5)
# S_partiality1 = tk.Scale(window, variable = s_partiality1)
# S_partiality2 = tk.Scale(window, variable = s_partiality2)

# S_partiality1.pack()
# S_partiality2.pack()

Gain = tk.Scale(window, from_ = 0, to = 1.0, resolution= 0.1, variable = gain0)

Gain.pack()

Gain1 = tk.Scale(window, from_ = 0, to = 1.0, resolution= 0.1, variable = gain1)

Gain1.pack()

B_pause = tk.Button(window, text = "pause", command = pause)
B_resume = tk.Button(window, text = "resume", command = resume)

B_pause.pack()
B_resume.pack()

B_start = tk.Button(window, text = "start", command = resume)

B_start.pack()

B_off = tk.Button(window, text = "off", command = stop)

B_off.pack()


wf1 = wave.open(wavefile1, 'rb')
wf2 = wave.open(wavefile2, 'rb')



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

while True:
    window.update()
    if get_on() == True and get_off() == False:
        input_tuple1 = unpack('hh' * BLOCKLEN, input_bytes1)
        input_tuple2 = unpack('hh' * BLOCKLEN, input_bytes2)

            # if len(music_array1) > 0 and index < 1000000:
            #     output_value0 = int(clip16(gain.get() * music_array1[index][0]))
            #     output_value1 = int(clip16(gain.get() * music_array1[index][1]))
            #     output_value2 = int(clip16(gain.get() * music_array2[index][0]))
            #     output_value3 = int(clip16(gain.get() * music_array2[index][1]))
        if index < 90000000:
            # output_value0 = int(clip16(gain.get() * input_tuple1[0]))
            # output_value1 = int(clip16(gain.get() * input_tuple1[1]))
            # output_value2 = int(clip16(gain.get() * input_tuple2[0]))
            # output_value3 = int(clip16(gain.get() * input_tuple2[1]))
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
            # output_block1 = [output_value0, output_value1, output_value2, output_value3]
            if vibrate == True:
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

            if regular == True:
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

            if filter == True:
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
        # output_bytes = pack('hh', output_value0 + output_value2, output_value1 + output_value3)

        input_bytes1 = wf1.readframes(BLOCKLEN)
        input_bytes2 = wf2.readframes(BLOCKLEN)
        index = index + 1
    elif get_off() == True:
        print('* Finished')
        stream.stop_stream()
        stream.close()
        p.terminate()
        if save == True:
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(2)
            waveFile.setsampwidth(p.get_sample_size(pa.paInt16))
            waveFile.setframerate(44100)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
        break
    else:
        continue

# print('* Finished')
#
# stream.stop_stream()
# stream.close()
# p.terminate()