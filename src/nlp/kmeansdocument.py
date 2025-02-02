import matplotlib.pyplot as plt
import pandas as pd
import string
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

try:
  nltk.download('punkt_tab')
  nltk.download('stopwords')
except:
  pass

def sentence_processing(sentence):
  # Sentence processing
  lowercase_sentence = sentence.lower()
  lowercase_sentence = re.sub(r"\d+", "", lowercase_sentence)
  lowercase_sentence = lowercase_sentence.translate(str.maketrans("","",string.punctuation))
  lowercase_sentence = lowercase_sentence.strip()

  # Stemming process
  stemmer_factory = StemmerFactory()
  stemmer = stemmer_factory.create_stemmer()
  stemmer_sentence = stemmer.stem(lowercase_sentence)

  # Remove whitespace leading & trailing
  stopword_factory = StopWordRemoverFactory()
  stopword = stopword_factory.create_stop_word_remover()
  stopword_sentence = stopword.remove(stemmer_sentence)

  return stopword_sentence

df = pd.read_csv('your_own_file.csv')
vector = TfidfVectorizer()
x = vector.fit_transform(df['title'])

wcss = []
total_cluster = 10
for i in range(1,total_cluster):
  model = KMeans(n_clusters=i, init='k-means++', max_iter=100, n_init=1)
  model.fit(x)
  wcss.append(model.inertia_)

plt.plot(range(1,total_cluster), wcss)

df['cluster'] = model.labels_
df