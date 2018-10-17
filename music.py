import wave
from pydub import AudioSegment
import random
from textblob import TextBlob
import os
import math
import numpy as np

'''
pianoKeys = {16 : '16.wav', 17 : '17.wav', 18 : '18.wav', 19 : '19.wav', 
20 : '20.wav', 21 : '21.wav', 22 : '22.wav', 23 : '23.wav', 24 : '24.wav', 
25 : '25.wav', 26 : '26.wav', 27 : '27.wav', 28 : '28.wav', 29 : '29.wav', 
30 : '30.wav', 31 : '31.wav', 32 : '32.wav', 33 : '33.wav', 34 : '34.wav', 
35 : '35.wav', 36 : '36.wav', 37 : '37.wav', 38 : '38.wav', 39 : '39.wav', 
40 : '40.wav', 49 : '49.wav', 50 : '50.wav', 51: '51.wav', 52 : '52.wav', 53 : '53.wav', 
54 : '54.wav', 55 : '55.wav', 56 : '56.wav', 57 : '57.wav', 58 : '58.wav', 59 : '59.wav',
 60 : '60.wav', 61 : '61.wav'}
'''
pianoKeys = {}
for i in range(1, 89):
    if (i >= 65 and i <= 84):
        continue
    string = str(i) + ".wav"
    pianoKeys[i] = string
#print(pianoKeys) 

keys = {'A' : 1, 'Bb' : 2, 'B' : 3, 'C' : 4, 'Db' : 5, 'D' : 6, 
'Eb' : 7, 'E' : 8, 'F' : 9, 'Gb' : 10, 'G' : 11, 'Ab' : 12}

reverse_keys = {1 : 'A', 2 : 'Bb', 3 : 'B', 4 : 'C', 5 : 'Db', 6 : 'D', 
7 : 'Eb', 8 : 'E', 9 : 'F', 10 : 'Gb', 11 : 'G', 12 : 'Ab'}

pitch = [[], [1, 3, 5, 6, 8, 10, 12]]
for i in range(0, 12):
    pitch.append([])
    for j in pitch[i]:
        num = j + 1
        if (num >= 13):
            num -= 12
        pitch[i + 1].append(num)
#print (pitch)

chords = [[], [1, 5, 8]]
for i in range(1, 13):
    chords.append([])
    for j in chords[i]:
        num = j + 1
        if (num >= 13):
            num -= 12
        chords[i + 1].append(num)
#print (chords)

def random_generate():
    array = []
    sound = None
    filepath = "grandPiano"
    for i in range (0,100):
        num1 = random.randint(0,100)
        num = -1
        if(num1 < 33):
            num = random.randint(1,64)
        else:
            num = random.randint(85,88)
        array.append(num)
        sound2 = AudioSegment.from_file(filepath + '\\'+pianoKeys[array[i]])
        sound2 = sound2[:0.2 * 1000]
        if (sound == None):
            sound = sound2
        else:
            sound += sound2
    if (sound != None):
        sound.export("music.wav", format = "wav")

def get_Sentiment_Polarity(sentence):
    sentence = TextBlob(sentence)
    #print(sentence.sentiment)
    x = sentence.sentiment.polarity
    return x

def pitch_detection():
    f = wave.open('voice.wav', 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)#读取音频，字符串格式
    waveData = np.fromstring(strData,dtype=np.int16)#将字符串转化为int
    #waveData = waveData*1.0/(max(abs(waveData)))#wave幅值归一化
    framerate = f.getframerate()
    
    #每半秒一分析
    pitches = []
    amount = 0
    while (amount < len(waveData)):
        #傅里叶变换
        fly = np.fft.fft(waveData[amount : amount + 22050])
        #提取基频（分贝最大频率）
        freqs = np.fft.fftfreq(len(fly))
        idx = np.argmax(np.abs(fly))
        freq = freqs[idx]
        freq_in_hertz = abs(freq * 44110)
        x = freq_in_hertz
        x = ((math.log((x / 440)) / math.log(2)) * 12) + 49
        x = int(x + 0.5)
        while (x > 12):
            x -= 12
        while (x < 1):
            x += 12
        pitches.append(reverse_keys[x])
        amount += 22050
    print ('The pitch(es):')
    print (pitches)
    print()
    return pitches

def chord_detection():
    #Comparing
    point_cumulator = {'A' : 0, 'Bb' : 0, 'B' : 0, 'C' : 0, 'Db' : 0, 'D' : 0, 
    'Eb' : 0, 'E' : 0, 'F' : 0, 'Gb' : 0, 'G' : 0, 'Ab' : 0}

    pitches = pitch_detection()
    pitch_arr = []

    for pitch in pitches:
        for i in reverse_keys:
            if(pitch == reverse_keys[i]):
                pitch_arr.append(keys[pitch])

    for pitch in pitch_arr:
        for j in range(1, 13):
            for i in range(0,3):
                if(chords[j][i]==pitch):
                    point_cumulator[reverse_keys[j]]+=1
    
    rank = []
    maxi = 0
    for e in point_cumulator:
        if (point_cumulator[e] > maxi):
            maxi = point_cumulator[e]
    for e in point_cumulator:
        if(point_cumulator[e]==maxi):
            rank.append(e)

    #print (point_cumulator)

    if (len(rank) == 1):
        print('Rank Distribution:')
        print (point_cumulator)
        print()
        print('Final determined chord:')
        print(rank[0])
        return rank[0]
    else:
        num = random.randint(0, 12)
        print('Rank Distribution:')
        print (point_cumulator)
        print()
        print('Final determined chord:')
        print(rank[int(num % len(rank))])
        return rank[int(num % len(rank))]

    #if (mood == 0 or mood == -2):
        #就跟所有调比
    #elif (mood < 0):
        #就跟小调比
    #elif (mood > 0):
        #就跟大调比

def generate_Main(bpm):
    #TODO
    sound = None
    duration_main = 45*1000
    milisecond_per_beat = 60 / bpm *1000
    milisecond_duration = 0
    char_chord = chord_detection()
    #the chosen pitch
    real_chord=chords[keys[char_chord]]
    real_pitch=pitch[keys[char_chord]]
    total_beats = duration_main / milisecond_per_beat
    time_count = 0

    #determine beats per genYin
    beats_for_one = int(total_beats / 32)
    beats = 0
    low_sound = None
    
    for k in range(10000):
        key = -1
        if(time_count>=total_beats):
            break
        else:
            rand_num = random.randint(0,2)
            rand_beat = random.randint(1,2)
            milisecond_duration = rand_beat*milisecond_per_beat
            time_count+=rand_beat
            if (rand_num == 2):
                key = real_pitch[random.randint(0, 6)]
                key += (40 + 12 * random.randint(0, 1))
                sound2 = AudioSegment.from_file('grandPiano' + '\\'+pianoKeys[key])
                sound2 = sound2[:milisecond_duration]
                if (sound == None):
                    sound = sound2
                else:
                    sound += sound2
            else:
                layer = random.randint(0, 3)
                key = real_chord[random.randint(0, 2)]
                key += (40 + 12 * random.randint(0, 1))
                sound2 = AudioSegment.from_file('grandPiano' + '\\'+pianoKeys[key])
                sound2 = sound2[:milisecond_duration]
                for i in range(0, layer):
                    key = real_chord[random.randint(0, 2)]
                    key += (40 + 12 * random.randint(0, 1))
                    sound3 = AudioSegment.from_file('grandPiano' + '\\' + pianoKeys[key])
                    sound3 = sound3[:milisecond_duration]
                    sound2 = sound2.overlay(sound3)
                if (sound == None):
                    sound = sound2
                else:
                    sound += sound2
        
        #左手低音
        beats += rand_beat
        if (beats % beats_for_one == 0): #刚好在根音点上
            genYin = 0
            if (key > 51):  #如果音太高 降三个八度
                genYin = key - 36
            else:   #正常区间 减两个八度
                genYin = key - 24
            soundg = AudioSegment.from_file('grandPiano' + '\\' + pianoKeys[genYin])
            rand = random.randint(1,2)
            milisecond_duration = rand*milisecond_per_beat
            soundg = soundg[:milisecond_duration]
            if (low_sound == None):
                low_sound = soundg
            else:
                low_sound += soundg
        elif ((beats - 1) % beats_for_one == 0): #下次循环会多一个beat
            silence = AudioSegment.from_file('grandPiano' + '\\' + 'silence.wav')
            silence = silence[:milisecond_per_beat]  #空
            genYin = 0
            if (key > 51):  #如果音太高 降三个八度
                genYin = key - 36
            else:   #正常区间 减两个八度
                genYin = key - 24
            soundg = AudioSegment.from_file('grandPiano' + '\\' + pianoKeys[genYin])
            rand = random.randint(1,2)
            milisecond_duration = rand*milisecond_per_beat
            soundg = soundg[:milisecond_duration]
            if (low_sound == None):
                low_sound = soundg
            else:
                low_sound += soundg
        else:
            genYin = 0
            if (key > 51):  #如果音太高 降三个八度
                genYin = key - 24
            else:   #正常区间 减两个八度
                genYin = key - 12
            soundg = AudioSegment.from_file('grandPiano' + '\\' + pianoKeys[genYin])
            rand = random.randint(1,2)
            milisecond_duration = rand*milisecond_per_beat
            soundg = soundg[:milisecond_duration]
            if (low_sound == None):
                low_sound = soundg
            else:
                low_sound += soundg
    sound = sound.overlay(low_sound)
    sound.export("music.wav", format = "wav")

def generate_refrain(bpm, major):
    #TODO
    print(" ")

def generate_Interval(bpm, major):
    #TODO
    print(" ")

def generate_Ending(bpm, major):
    #TODO
    print(" ")

def combine(sound1, sound2):
    sound1 = AudioSegment.from_file(sound1, format = 'wav')
    sound2 = AudioSegment.from_file(sound2, format = 'wav')
    combine = sound1 + sound2
    return combine

def overlay(wave1, wave2):
    sound1 = AudioSegment.from_file(wave1, format = 'wav')
    sound2 = AudioSegment.from_file(wave2, format = 'wav')
    combine = sound1.overlay(sound2)
    return combine

def add_drums(bpm):
    #TODO
    filepath = 'drums'
    drums_file = {1 : 'base_drum.wav', 2 : 'cai_cha_0.wav', 
    3 : 'jun_gu.wav', 4 : 'cai_cha_1.wav', 
    5 : 'diao_cha1.wav', 6 : 'diao_cha_2.wav', 
    7 : 'tom_drum1.wav', 8 : 'tom_drum2.wav', 9 : 'tom_drum3.wav'}

    sound = None
    duration_main = 45*1000
    milisecond_per_beat = 60 / bpm *1000
    milisecond_duration = 0
    char_chord = chord_detection()
    #the chosen pitch
    real_chord=chords[keys[char_chord]]
    real_pitch=pitch[keys[char_chord]]
    total_beats = duration_main / milisecond_per_beat
    time_count = 0

    #determine beats per genYin
    beats_for_one = int(total_beats / 32)
    beats = 0
    rand = random.randint(1,2)
    milisecond_duration = rand*milisecond_per_beat
    drums_sound = AudioSegment.from_file(filepath + '\\' + drums_file[1])
    drums_sound = drums_sound[:milisecond_duration]
    num_between_base = random.randint(2, 4)

    


if __name__ == '__main__':
    major = chord_detection()
    generate_Main(230)
    os.system('music.wav')
