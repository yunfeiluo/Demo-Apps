import speech_recognition as sr
import pyaudio
import wave

## Recognize the sound
def getSpeak():
    # init
    r = sr.Recognizer()
    print("Say something:")
    
    with sr.Microphone() as source:
        audio = r.listen(source)

        #Save the audio file
        wf = wave.open("voice.wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(audio.sample_width)
        wf.setframerate(audio.sample_rate)
        wf.writeframes(audio.frame_data)
        wf.close()
    
    # recognize with CMU Sphinx
    # sentence = r.recognize_sphinx(audio)

    try:
        sentence = r.recognize_google(audio) #recognize with google
        print ("You said: " + sentence)
    except sr.UnknownValueError:
        #print ("Unknown")
        return ('blablabla...')
    except sr.RequestError as e:
        print ("Error; {0}".format(e))
        return ('Request Error!')
    return sentence