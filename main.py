import pandas as pd
from pydub import AudioSegment
from gtts import gTTS
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
from pygame import mixer

announcements = []

def textToSpeech(text, filename, language):
    text = str(text)
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save(filename)

def mergeAudios(audios):
    combined = AudioSegment.empty()
    for audio in audios:
        combined += AudioSegment.from_mp3(audio)
    return combined

def generateSkeleton():
    audio = AudioSegment.from_mp3('railway.mp3')
    start = 18500
    finish = 19900
    audioProcessed = audio[start:finish]
    audioProcessed.export("tune1.mp3", format="mp3")

    # 1 - Kripya dhyan digiye
    # start = 88000
    # finish = 90200
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("1.mp3", format="mp3")
    textToSpeech("कृपया ध्यान दीजीए ", "1.mp3", 'hi')

    # 3 - Se chalkar
    # start = 91000
    # finish = 92200
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("3.mp3", format="mp3")
    textToSpeech(" से चलकर ", "3.mp3", 'hi')

    # 5 - Ke raste
    # start = 94000
    # finish = 95000
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("5.mp3", format="mp3")
    textToSpeech(" के रास्ते ", "5.mp3", 'hi')

    # 7 - Ko jaane wali gadi sankhya
    # start = 96000
    # finish = 98900
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("7.mp3", format="mp3")
    textToSpeech(" को जाने वाली गाड़ी संख्या  ", "7.mp3", 'hi')

    # 9 - Kuch hi samay me platform number
    # start = 105500
    # finish = 108200
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("9.mp3", format="mp3")
    textToSpeech(" कुछ ही समय मे platform नंबर ", "9.mp3", 'hi')

    # 11 - par aa rhi hai
    # start = 109000
    # finish = 112250
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("11.mp3", format="mp3")
    textToSpeech(" पर आ रही है।", "11.mp3", 'hi')

    # 12 - may I have your attention please. train no
    # start = 18900
    # finish = 23900
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("12.mp3", format="mp3")
    textToSpeech("May I have your attention please. Train number ", '12.mp3', 'en')

    # 14 - from
    # start = 30155
    # finish = 31000
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("14.mp3", format="mp3")
    textToSpeech(" from ", "14.mp3", 'en')

    # 16 - to
    # start = 31557
    # finish = 32500
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("16.mp3", format="mp3")
    textToSpeech(" to ", "16.mp3", 'en')

    # 18 - via
    # start = 33900
    # finish = 34500
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("18.mp3", format="mp3")
    textToSpeech(" via ", "18.mp3", 'en')

    # 20 - is arriving shortly on platform no
    # start = 36500
    # finish = 40500
    # audioProcessed = audio[start:finish]
    # audioProcessed.export("20.mp3", format="mp3")
    textToSpeech(" is arriving shortly on platform number ", "20.mp3", 'en')

def generateAnnouncement(filename):
    df = pd.read_excel(filename)
    for index, item in df.iterrows():
        textToSpeech(item['from'], f"2.mp3", "hi")
        textToSpeech(item['via'], f"4.mp3", "hi")
        textToSpeech(item['to'], f"6.mp3", "hi")
        textToSpeech(item['train_no'] + " "+ item['train_name'], f"8.mp3", "hi")
        textToSpeech(item['platform'], f"10.mp3", "hi")

        # 13 - Generate train no and name
        textToSpeech(item['train_no'] + " "+ item['train_name'], f"13.mp3", "en")
        # 15 - Generate from-city
        textToSpeech(item['from'], f"15.mp3", "en")
        # 17 - to-city
        textToSpeech(item['to'], f"17.mp3", "en")
        # 19 - via-city
        textToSpeech(item['via'], f"19.mp3", "en")
        # 21 - platform number
        textToSpeech(item['platform'], f"21.mp3", "en")

        audios = [f"{i}.mp3" for i in range(1, 22)]
        audios.insert(0, 'tune1.mp3')
        audios.insert(12, 'tune1.mp3')
        audios.append('tune1.mp3')

        announcement = mergeAudios(audios)
        announcement.export(f"announcement_{index+1}.mp3", format='mp3')
        announcements.append(f"announcement_{index+1}.mp3")
    return df

def announce(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()

if __name__ == '__main__':
    print("Generating Skeleton...")
    generateSkeleton()
    print("Generating Announcement...")
    exel = generateAnnouncement("announce_hindi.xlsx")
    print("All generated")
    window = tkinter.Tk()
    window.title("Railway announcement system")
    cv_img = cv2.cvtColor(cv2.imread("railway.png"), cv2.COLOR_BGR2RGB)
    canvas = tkinter.Canvas(window, width=555, height=354)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
    image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
    canvas.pack()
    for index, item in exel.iterrows():
        btn = tkinter.Button(window, text=f"{item['from'].capitalize()} to {item['to'].capitalize()} ({item['train_name'].capitalize()})", background='blue', foreground='white', border=5, font='Times 12 italic bold', width=60, height=2, command=partial(announce, f"announcement_{index+1}.mp3"))
        btn.pack()

    window.mainloop()
