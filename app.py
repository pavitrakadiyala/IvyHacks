from flask import Flask,request, url_for, redirect, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/get_summary',methods=['POST','GET'])
def predict():
    input_txt = request.form['input_text']
    #print("Input text:"+input_txt)
    t = 0
    if request.method == 'POST':  
        if (input_txt == ""):
            f = request.files['file']  
            f_name = f.filename
            f.save(f_name)
            t = 1
        
        import spacy
        from spacy.lang.en.stop_words import STOP_WORDS
        from string import punctuation
        import speech_recognition as sr
        from heapq import nlargest 

        if (t == 1):
            if ("txt" in f_name):
                #Opening the text file
                f = open('trial.txt','r')
                text = f.read()
            elif("wav" in f_name):
                r = sr.Recognizer()
                with sr.AudioFile(f_name) as source:
                    audio_data = r.record(source)
                    t = r.recognize_google(audio_data)
                    nlp = spacy.load("en_core_web_sm") 
                    doc = nlp(t)
                    x = []
                    for sent in doc.sents:
                        x.append(str(sent))
                    text = ". ".join(x) + "."
        else:
            text = input_txt  

        stopwords = list(STOP_WORDS)

        nlp = spacy.load('en_core_web_sm')

        doc = nlp(text)

        tokens = [token.text for token in doc ]

        punctuation = punctuation + '\n' + ' ' + '  ' + '...' + '\n           '

        word_frequency = {}
        for word in doc:
            if word.text.lower() not in stopwords:
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequency.keys():
                        word_frequency[word.text] = 1
                    else:
                        word_frequency[word.text] += 1
                        
        max_frequency = max(word_frequency.values())

        for word in word_frequency.keys():
            word_frequency[word] = word_frequency[word]/max_frequency
                        
        sentence_tokens = [sent for sent in doc.sents]

        sentence_score = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequency.keys():
                    if sent not in sentence_score.keys():
                        sentence_score[sent] = word_frequency[word.text.lower()]
                    else:
                        sentence_score[sent] += word_frequency[word.text.lower()]
                        
        select_length = int(len(sentence_tokens)*0.3)

        summary = nlargest(select_length, sentence_score, key = sentence_score.get)                
                        
        final_summary = [word.text for word in summary]

        summary = ' '.join(final_summary)

        if(len(summary) == 0):
            final_sum = "Your input text was too small. This is your input text: " + text
        else:
            final_sum = summary


        return render_template('summary.html', output = final_sum)


if __name__ == '__main__':
    app.run(port=8000,host='0.0.0.0')