import nltk
from snowballstemmer import TurkishStemmer
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import numpy
import random
import json

nltk.download('punkt')
with open(r"covidDataset.json",encoding="utf8") as file:
    data = json.load(file)


stemmer=TurkishStemmer()
words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stemWord(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

model = load_model('covid.h5')

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stemWord(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return numpy.array(bag)


def covidOlasilik(cevapListesi):
    covidScore = 0
    belirtiSayisi = 8
    if ("umre" in cevapListesi):
        covidScore += 1
    if ("hastane" in cevapListesi):
        covidScore += 1
    if ("yurtdisi" in cevapListesi):
        covidScore += 1
    if ("ates" in cevapListesi):
        covidScore += 1
    if ("koku" in cevapListesi):
        covidScore += 1
    if ("oksuruk" in cevapListesi):
        covidScore += 1
    if ("nefes" in cevapListesi):
        covidScore += 1
    if ("halsizlik" in cevapListesi):
        covidScore += 1
    return (covidScore / belirtiSayisi) * 100


def covidRiskDurumu(covidOlasilik):
    if 50 > covidOlasilik:
        riskDurumu = "Düşük risk grubunda bulunuyorsunuz."
    elif 75 > covidOlasilik > 50:
        riskDurumu = "Orta düzey risk grubunda bulunuyorsunuz. Şikayetlerinizin artması durumunda sağlık merkezlerine gitmelisiniz."
    elif covidOlasilik > 75:
        riskDurumu = "Yüsek düzeyde risk grubunda bulunuyorsunuz, en yakın sağlık merkezine gitmelisiniz."
    return riskDurumu


def chat(message):
    cevapListesi = []

    if message.lower() == "quit":
        covidOlasilikDurumu = covidOlasilik(cevapListesi)
        return "Covid19 risk durumunuz: %{0}".format(covidOlasilikDurumu)+"\n"+covidRiskDurumu(covidOlasilikDurumu)
        
    results = model.predict(np.asanyarray([bag_of_words(message, words)]))[0]
    # print(results)
    results_index = numpy.argmax(results)
    tag = labels[results_index]

    if results[results_index] > 0.85:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                cevapListesi.append(tg['tag'])
                responses = tg['responses']
                
        return random.choice(responses)
    
    else:
        return "Tam olarak anlayamadım"
