import nltk
from snowballstemmer import TurkishStemmer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import numpy
import json
import matplotlib.pyplot as plt

# Json dosyası olarak oluşturulan Covid-19 metin veri setini yükleme.
nltk.download('punkt')
with open(r"covidDataset.json") as file:
    data = json.load(file)

# Türkçe kelimeler için stemmer
stemmer = TurkishStemmer()

# Değişken tanımlamaları
words = []
labels = []
docs_x = []
docs_y = []

# Cümlelerin kelimelere ve etiketlere ayrılması
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

# Cümlelerin küçük harfe alınması ve ayrılması
words = [stemmer.stemWord(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

# Etiketlerin alfabetik sıralanması
labels = sorted(labels)

# Eğitime ait giriş ve çıkış değişkenleri tanımlanması
training = []
output = []
out_empty = [0 for _ in range(len(labels))]

# Kelimelerin 0-1 mantığına göre ayrılması.
for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stemWord(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

# Eğitim giriş ve çıkış değerlerini dizi olarak ayarlama
training = numpy.array(training)
output = numpy.array(output)

# Keras ile yapay sinir ağı modelinin inşa edilmesi.

model = Sequential()
model.add(Dense(32, input_shape=(len(training[0]),), activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(8, activation="relu"))
model.add(Dense(16, activation="relu"))
model.add(Dense(32, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(len(labels), activation="softmax"))
model.summary()
model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=.001), metrics=['acc'])
history = model.fit(training, output, epochs=300, verbose=2, batch_size=4)

# Eğitime ait ağırlık dosyasının kaydedilmesi.
model.save('covid.h5')

# Eğitime ait başarım ve kayıp grafiklerinin çizilmesi.
acc = history.history['acc']
loss = history.history['loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'b', label='Eğitim Başarımı')
plt.title('Eğitim Başarımı')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'b', label='Eğitim Kaybı')
plt.title('Eğitim Kaybı')
plt.legend()
