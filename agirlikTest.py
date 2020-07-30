import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    from tensorflow.keras.models import load_model
import nltk
from snowballstemmer import TurkishStemmer
import numpy as np
import random
import json
import requests
import bs4

nltk.download('punkt')

with open(r"covidDataset.json", encoding="utf8") as file:
    data = json.load(file)

stemmer = TurkishStemmer()
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

model = load_model('covidAgirlik.h5')


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stemWord(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return np.array(bag)


def covid19(country):
    res = requests.get("https://www.worldometers.info/coronavirus/#countries")
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    index = -1
    data = soup.select('tr td')
    for i in range(len(data)):
        if data[i].text.lower() == country.lower():
            index = i
            break
    gunlukTablo=""
    for i in range(7):
        if i == 0:
            gunlukTablo="\nÜlke adı: " + str(data[i + index].text)
        elif i == 1:
            gunlukTablo=gunlukTablo+'\n'+"Toplam vaka: " + str(data[i + index].text)
        elif i == 2:
            if data[i + index].text == '':
                gunlukTablo=gunlukTablo+'\n'+"Yeni vaka: 0"
            else:
                gunlukTablo=gunlukTablo+'\n'+"Yeni vaka: " + str(data[i + index].text)
        elif i == 3:
            gunlukTablo=gunlukTablo+'\n'+"Toplam ölüm: " + str(data[i + index].text)
        elif i == 4:
            if data[i + index].text == '':
                gunlukTablo=gunlukTablo+'\n'+"Yeni ölüm: 0"
            else:
                gunlukTablo=gunlukTablo+'\n'+"Yeni ölüm: " + str(data[i + index].text)
        elif i == 5:
            gunlukTablo=gunlukTablo+'\n'+"Toplam iyileşen: " + str(data[i + index].text)
        elif i == 6:
            gunlukTablo=gunlukTablo+'\n'+"Yeni iyileşen: " + str(data[i + index].text)
    return gunlukTablo


# Covid19 olma olasılığının hesaplanması
def covidOlasilik(cevapListesi):
    covidScore = 0
    toplamPuan = 100
    riskCarpani = 0
    if "hastane" in cevapListesi:
        covidScore += 3
    if "ishal" in cevapListesi:
        covidScore += 4
    if "gözBeyazCevresi" in cevapListesi:
        covidScore += 4
    if "ciltDokuntusu" in cevapListesi:
        covidScore += 4
    if "kokuTat" in cevapListesi:
        covidScore += 4
    if ("basAgrisi" in cevapListesi) or ("bogazAgrisi" in cevapListesi):
        covidScore += 4
    if ("umre" in cevapListesi) or ("yurtdisi" in cevapListesi):
        covidScore += 5
    if "ates" in cevapListesi:
        covidScore += 12
        riskCarpani += 1
    if "oksuruk" in cevapListesi:
        covidScore += 12
        riskCarpani += 1
    if "halsizlik" in cevapListesi:
        covidScore += 12
        riskCarpani += 1
    if "nefes" in cevapListesi:
        covidScore += 12
        riskCarpani += 1
    if ("konusmaZorlugu" in cevapListesi) or ("hareketKaybi" in cevapListesi):
        covidScore += 12
        riskCarpani += 1
    if "gogusAgrisi" in cevapListesi:
        covidScore += 12
        riskCarpani += 1

    sonucOlasilik = (covidScore / toplamPuan) * 100
    if riskCarpani >= 3:
        sonucOlasilik = sonucOlasilik * 2
    if sonucOlasilik >= 100:
        sonucOlasilik = 95
    return sonucOlasilik


# Kullanıcının çıkmak istediği ve sonuçları görmek istediği durumların kontrolü
def cikisDurumu(cevapListesi):
    cikisKontrol = False
    if "sonuc" in cevapListesi:
        cikisKontrol = True
    if "ayrilma" in cevapListesi:
        cikisKontrol = True
    if "sikayetYok" in cevapListesi:
        cikisKontrol = True
    return cikisKontrol


# Risk oranının hesaplanması
def covidRisk(covidOlasilik):
    if 30 >= covidOlasilik:
        riskDurumu = "Düşük risk grubunda bulunuyorsunuz."
    elif 60 > covidOlasilik > 30:
        riskDurumu = "Orta düzey risk grubunda bulunuyorsunuz. Şikayetlerinizin artması durumunda sağlık merkezlerine gitmelisiniz."
    elif covidOlasilik >= 60:
        riskDurumu = "Yüksek düzeyde risk grubunda bulunuyorsunuz, en yakın sağlık merkezine gitmelisiniz."
    return riskDurumu


def sonuc(olasilik, risk):
    return "Covid19 risk durumunuz: %{0}\n{1}".format(round(olasilik), risk)


cevapListesi = []


def reset():
    cevapListesi.clear()
    

def chat(message):
    covidOlasilikDurumu = covidOlasilik(cevapListesi)
    covidRiskDurumu = covidRisk(covidOlasilikDurumu)
    if message.lower() == "kapat":
        return sonuc(covidOlasilikDurumu, covidRiskDurumu)
    if message.lower() == "tablo":
        return covid19("Turkey")
    results = model.predict(np.asanyarray([bag_of_words(message, words)]))[0]
    # print(results)
    results_index = np.argmax(results)
    tag = labels[results_index]

    if results[results_index] > 0.85:
        for tg in data["intents"]:
            if tg['tag'] == tag:
                cevapListesi.append(tg['tag'])
                responses = tg['responses']
            if cikisDurumu(cevapListesi):
                return sonuc(covidOlasilikDurumu, covidRiskDurumu)
        return random.choice(responses)
    else:
        return "Tam olarak anlayamadım"
