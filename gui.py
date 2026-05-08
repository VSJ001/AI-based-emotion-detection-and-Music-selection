from tkinter import END, Tk, Button
from tkinter import ttk
import tkinter
import face_recognition
import spotify
import voice_text_recognition
import random
import os


class Gui:
    def opening_page(self):
        self.heading = Tk()
        self.heading.geometry('800x800')
        frame = ttk.Frame(self.heading, padding=20)
        frame.pack()
        title = "How do you want your mood to be detected?.."
        ttk.Label(frame, text=title, font=(
            'Ink Free', 50, 'bold')).grid(column=0, row=0)
        buttonFace = Button(
            self.heading, text='Face recognition', cursor="hand2")
        buttonFace.config(command=self.face_cb)  # call back fun
        buttonFace.config(font=('Ink Free', 30, 'bold'), compound='left')
        buttonFace.config(borderwidth=10)
        buttonFace.pack(pady=20)
        buttonVoice = Button(self.heading, text='Voice',
                             command=self.voice_cb, cursor="hand2")
        buttonVoice.config(font=('Ink Free', 30, 'bold'), compound='center')
        buttonVoice.config(borderwidth=10, padx=100)
        buttonVoice.pack(pady=20)
        buttonText = Button(self.heading, text='Text',
                            command=self.text_cb, cursor="hand2")
        buttonText.config(font=('Ink Free', 30, 'bold'), compound='right')
        buttonText.config(borderwidth=10, padx=100)
        buttonText.pack(pady=20)
        buttonClose = Button(self.heading, text='Close', cursor="hand2")
        buttonClose.config(font=('Ink Free', 30, 'bold'),
                           compound='right', command=self.heading.destroy)
        buttonClose.config(borderwidth=10, padx=100)
        buttonClose.pack(pady=20)
        self.heading.mainloop()

    def face_cb(self):
        face_recog = face_recognition.Face()
        self.emotion = face_recog.opencam()
        self.heading.destroy()
        self.spotify_page()

    def spotify_page(self):
        self.page = Tk()
        self.page.geometry("800x800")
        frame = ttk.Frame(self.page, padding=20)
        frame.pack()
        title = "Navigate to spotify"
        label = ttk.Label(frame, text=title, font=('Ink Free', 50, 'bold'))
        label.pack()
        label = ttk.Label(
            frame, text=f"detected emotion:{self.emotion}", font=('Ink Free', 20, 'bold'))
        label.pack()
        playlist_button = Button(frame, text='Open playlist')
        playlist_button.config(command=self.open_playlist)  # call back fun
        playlist_button.config(font=('Ink Free', 30, 'bold'), compound='left')
        playlist_button.config(borderwidth=10)
        playlist_button.pack(pady=20)
        song_button = Button(frame, text='Open song')
        song_button.config(command=self.open_song)  # call back fun
        song_button.config(font=('Ink Free', 30, 'bold'), compound='left')
        song_button.config(borderwidth=10)
        song_button.pack(pady=20)
        play_offline_button = Button(frame, text="play offline songs")
        play_offline_button.config(command=self.open_offline_song)
        play_offline_button.config(
            font=('Ink Free', 30, 'bold'), compound='left')
        play_offline_button.config(borderwidth=10)
        play_offline_button.pack(pady=20)

    def open_playlist(self):
        sp = spotify.MySpotify()
        sp.open_spotify_playlist(self.emotion)
        self.page.destroy()

    def open_song(self):
        sp = spotify.MySpotify()
        sp.open_spotify_songs(self.emotion)
        self.page.destroy()

    def open_offline_song(self):
        if self.emotion == 'happy':
            directory = 'offline_songs\\happy\\'
            dir_list = os.listdir(directory)
            song = str(random.choice(dir_list))
            os.startfile(directory+song)

        elif self.emotion == 'surprise':
            directory = 'offline_songs\\surprise\\'
            dir_list = os.listdir(directory)
            song = str(random.choice(dir_list))
            os.startfile(directory+song)

        elif self.emotion == 'angry':
            directory = 'offline_songs\\angry\\'
            dir_list = os.listdir(directory)
            song = str(random.choice(dir_list))
            os.startfile(directory+song)

        elif self.emotion == 'sad':
            directory = 'offline_songs\\sad\\'
            dir_list = os.listdir(directory)
            song = str(random.choice(dir_list))
            os.startfile(directory+song)

        elif self.emotion == 'disgust':
            directory = 'offline_songs\\disgust\\'
            dir_list = os.listdir(directory)
            song = str(random.choice(dir_list))
            os.startfile(directory+song)

        else:
            directory = 'offline_songs\\neutral\\'
            dir_list = os.listdir(directory)
            song = str(random.choice(dir_list))
            os.startfile(directory+song)
        self.page.destroy()

    def voice_cb(self):
        self.open_voice_page()

    def open_voice_page(self):
        self.heading.destroy()
        self.voice_page = Tk()
        self.voice_page.geometry("800x800")
        frame = ttk.Frame(self.voice_page, padding=20)
        frame.pack()
        self.q1 = Questions()
        self.q2 = Questions()
        self.q3 = Questions()
        self.q4 = Questions()
        self.q1.voice_question_block(
            text="How are you feeling today", page=self.voice_page, question=self.q1)
        self.q2.voice_question_block(
            text="What's been on your mind lately? How does it make you feel?", page=self.voice_page, question=self.q2)
        self.q3.voice_question_block(
            text="Can you describe a recent situation that made you feel happy/sad/angry/anxious/etc.?", page=self.voice_page, question=self.q3)
        self.q4.voice_question_block(
            text="How do you cope with difficult emotions when you experience them?", page=self.voice_page, question=self.q4)
        analyse = ttk.Button(
            text="Analyse", command=self.analyse_voice_emotion, style='TButton')
        analyse.pack()

    def analyse_voice_emotion(self):
        a1, a2, a3, a4 = self.q1.analyse_voice_emotion(), self.q2.analyse_voice_emotion(
        ), self.q3.analyse_voice_emotion(), self.q4.analyse_voice_emotion()
        av_sentiment_score = (a1 + a2 + a3 + a4) / 4
        self.emotion = self.get_emotion(av_sentiment_score)
        self.voice_page.destroy()
        self.spotify_page()

    def get_emotion(self, sentiment_score):
        if sentiment_score >= 0.5:
            return 'happy'
        elif sentiment_score >= 0.05 and sentiment_score < 0.5:
            return 'surprise'
        elif sentiment_score >= -0.05 and sentiment_score < 0.05:
            return 'neutral'
        elif sentiment_score > -0.5 and sentiment_score < -0.05:
            return 'sad'
        elif sentiment_score >= -0.75 and sentiment_score <= -0.5:
            return 'disgust'
        else:
            return 'angry'

    def text_cb(self):
        self.open_text_page()

    def open_text_page(self):
        self.heading.destroy()
        self.text_page = Tk()
        self.text_page.geometry("800x800")
        frame = ttk.Frame(self.text_page, padding=20)
        frame.pack()
        self.q1 = Questions()
        self.q2 = Questions()
        self.q3 = Questions()
        self.q4 = Questions()
        self.q1.text_question_block(
            text="How are you feeling today", page=self.text_page, question=self.q1)
        self.q2.text_question_block(
            text="What's been on your mind lately? How does it make you feel?", page=self.text_page, question=self.q2)
        self.q3.text_question_block(
            text="Can you describe a recent situation that made you feel happy/sad/angry/anxious/etc.?", page=self.text_page, question=self.q3)
        self.q4.text_question_block(
            text="How do you cope with difficult emotions when you experience them?", page=self.text_page, question=self.q4)
        analyse = ttk.Button(
            text="Analyse", command=self.analyse_text_emotion, style='TButton')
        analyse.pack()

    def analyse_text_emotion(self):
        a1, a2, a3, a4 = self.q1.analyse_text_emotion(), self.q2.analyse_text_emotion(
        ), self.q3.analyse_text_emotion(), self.q4.analyse_text_emotion()
        av_sentiment_score = (a1 + a2 + a3 + a4) / 4
        self.emotion = self.get_emotion(av_sentiment_score)
        self.text_page.destroy()
        self.spotify_page()


class Questions:
    def recognise_voice(self):
        self.voice = voice_text_recognition.VoiceTextRecognition()
        self.voice.recognise_voice(self.textbox)

    def analyse_voice_emotion(self):
        return (self.voice.analyse_emotion()['compound'])

    def voice_question_block(self, text, page, question):
        q = ttk.Label(text=text, font=('Ink Free', 20, 'bold'))
        q.pack()
        self.textbox = tkinter.Text(page, height=3, width=80)
        self.textbox.pack()
        button = ttk.Button(text="record voice", cursor="hand2",
                            command=question.recognise_voice)
        button.pack(padx=20, pady=20)

    def text_question_block(self, text, page, question):
        q = ttk.Label(text=text, font=('Ink Free', 20, 'bold'))
        q.pack()
        self.textbox = tkinter.Text(page, height=3, width=80)
        self.textbox.pack()

    def analyse_text_emotion(self):
        text = self.textbox.get('1.0', END)
        text_score = voice_text_recognition.VoiceTextRecognition()
        return text_score.analyse_text_emotion(text)['compound']
