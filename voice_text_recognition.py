from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import speech_recognition as sr

class VoiceTextRecognition:
    def recognise_voice(self, textbox):
        self.recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source,duration=1)
            recordedaudio = self.recognizer.listen(source)
        try:
            self.text = self.recognizer.recognize_google(recordedaudio,language='en-US')
            textbox.insert('3.2','Your message: {}'.format(self.text))
        except Exception as ex:
            textbox.insert('3.2', str(ex)) 
    
    def analyse_emotion(self):
        analyser  = SentimentIntensityAnalyzer()
        Sentence = [str(self.text)]
        score = {}
        for i in Sentence:
            score = analyser.polarity_scores(i)
        return score
    
    def analyse_text_emotion(self, text):
        analyser  = SentimentIntensityAnalyzer()
        Sentence = [str(text)]
        score = {}
        for i in Sentence:
            score = analyser.polarity_scores(i)
        return score
    
