import string 
import re
import nltk
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk import word_tokenize
from nltk.probability import FreqDist

try:
  pass
except:
  nltk.download('punkt_tab')

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
  tokens = nltk.tokenize.word_tokenize(stopword_sentence)

  # Frequent words
  frequent = nltk.FreqDist(tokens)
  most_common = frequent.most_common(5)

  return most_common