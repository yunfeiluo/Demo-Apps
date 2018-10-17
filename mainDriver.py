import record
import os
import music
import wave
import numpy as np
import bpm_detector as bd 

def main(): 
    while (True):
        command = input('Type the command: ')
        if (command == 'exit'):  #ending condition
            break
        elif (command == 'record'):
            possibleString = record.getSpeak() #get audio input
            print(possibleString)  #check
            sentiment = -2
            if (possibleString != 'blablabla...'):
                sentiment = music.get_Sentiment_Polarity(possibleString)

            f = wave.open('voice.wav','rb')
            params = f.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            strData = f.readframes(nframes)#读取音频，字符串格式
            waveData = np.fromstring(strData,dtype=np.int16)#将字符串转化为int
            
            #bpm detect
            #data, fs = bd.read_wav('voice.wav')
            #bpms = bd.bpm_detector(data, fs)
            #bpm = bpm = np.median(bpms)
            #print (bpms)
            #print (len(bpms)) 
            
            #Pre_setting of bpm
            music.generate_Main(230)
        elif (command == 'check music'):
            os.system('music.wav')
        elif (command == 'new music'):
            bpm = input('Type the bpm')
            bpm = int(bpm)
            music.generate_Main(bpm)
        
        elif (command == 'test'):
            #bpm = bd.get_file_bpm('voice.wav')
            #print(bpm)
            filename = input('Which file would you like to test?')
            f = wave.open(filename,'rb')
            bpm = bd.get_file_bpm(filename)
            print(bpm)
            params = f.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            strData = f.readframes(nframes)#读取音频，字符串格式
            waveData = np.fromstring(strData,dtype=np.int16)#将字符串转化为int

        elif (command == 'random generate'):
            music.random_generate()
            os.system("music.wav")
        elif (command == 'check record'):
            os.system('voice.wav')  #play the wav file
        else:
            continue  #Keep running

if __name__ == '__main__':
    main()
