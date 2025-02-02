import pandas as pd
import string
import re
import nltk
from bertopic import BERTopic
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

def frequent_words(df):
  df['title'] = df['title'].apply(sentence_processing)
  sentence = df['title'].to_list()
  sentence = ' '.join(sentence)
  tokens = nltk.tokenize.word_tokenize(sentence)
  frequent = nltk.FreqDist(tokens)
  return frequent

df = pd.read_csv('your_own_file.csv')
model = BERTopic(verbose=True, embedding_model='all-MiniLM-L6-v2')
fitting_model = model.fit_transform(df['title'])
df_topic_modelling = model.get_topic_info()
df_topic_modelling