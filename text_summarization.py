import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

f = open('trial.txt','r')
text = f.read()

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
                
from heapq import nlargest 

select_length = int(len(sentence_tokens)*0.3)

summary = nlargest(select_length, sentence_score, key = sentence_score.get)                
                
final_summary = [word.text for word in summary]

summary = ' '.join(final_summary)

print(len(text))
print(len(summary))

print(summary)