# -*- coding: utf-8 -*-
"""análise de MTF corpus

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kqI8pVnMeU80Or6lzX6h6JiU7ZgvBouE
"""

#instalando o nltk
import nltk
nltk.download('all')

# pacotes para a word cloud
# import os

# from os import path

# pacote para exportar df
import pandas as pd

# pegando arquivos do drive
from google.colab import drive
drive.mount('/content/drive')

# tirando as marcas de pontuação
import re
def process_text(raw_txt):
  raw_txt = re.sub('\.', ' ', raw_txt)
  raw_txt = re.sub('``', '', raw_txt)
  raw_txt = re.sub("''", '', raw_txt)
  raw_txt = re.sub('"', '', raw_txt)
  raw_txt = re.sub('!', ' ', raw_txt)
  raw_txt = re.sub(':', ' ', raw_txt)
  raw_txt = re.sub('\,', ' ', raw_txt)
  raw_txt = re.sub('-', ' ', raw_txt)
  raw_txt = re.sub(';', ' ', raw_txt)
  raw_txt = re.sub('- -', ' ', raw_txt)
  raw_txt = re.sub('\+', ' ', raw_txt)
  raw_txt = re.sub('\?', ' ', raw_txt)
  raw_txt = re.sub("\.", " ", raw_txt)
  raw_txt = re.sub('\n', " ", raw_txt)
  raw_txt = re.sub('#', " ", raw_txt)
  raw_txt = re.sub('[()]', '', raw_txt)
  raw_txt = re.sub(' +', ' ', raw_txt)
  raw_txt = raw_txt.lower()
  return raw_txt

# pasta dos textos
path = "/content/drive/MyDrive/Corpora|Datasets/MFT_corpus/"

#ABRE O CORPUS ORIGINAL
import glob
texts_path = glob.glob(path + "*txt", recursive=True)
print(len(texts_path))

texts = ""
for path in range(len(texts_path)):
  with open(texts_path[path], "rU", encoding='windows-1252') as fd:
    texts = texts + fd.read()

# print(texts)

#limpando os textos
texts_clean = process_text(texts)

# import nltk
# nltk.download('punkt')

# tokenizar as palavras
words_texts = nltk.word_tokenize(texts_clean)
texts_list = nltk.Text(words_texts)
# print(texts_list)
# conhecendo o corpus
print('O número de tokens é ' + str(len(words_texts)))
print('O número de types é ' + str(len(set(words_texts))))
ratio1 = len(set(words_texts)) / len(words_texts)
ratio = round(ratio1 * 100, 2)
print('A razão type-token é ' + str(ratio))

stopwords.append("n't", "'s", '2')

# apagando as stopwords com nltk
from nltk.corpus import stopwords
stopwords = list(stopwords.words('english'))
new_stopwords = ["n't", "'s", '2']
updated_stopwords = stopwords + new_stopwords


# filtered_sentence = [w for w in words_texts if not w.lower() in updated_stopwords]

filtered_sentence = []

for w in words_texts:
    if w not in updated_stopwords:
        filtered_sentence.append(w)

# print(words_texts)
# print(filtered_sentence)

# distribuição da frequência
from nltk import FreqDist
freq = FreqDist(filtered_sentence)
freq.most_common(50)

import matplotlib.pyplot as plt
top_10_tokens = freq.most_common(10)  # Get the top 10 most common tokens

# Extract tokens and their frequencies for plotting
tokens, frequencies = zip(*top_10_tokens)

# Plotting the top 10 most frequent tokens
plt.figure(figsize=(10, 6))
plt.bar(tokens, frequencies, color='skyblue')
plt.xlabel('Tokens')
plt.ylabel('Frequencies')
plt.title('Top 10 Most Frequent Tokens')
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
plt.tight_layout()
plt.show()

people_concordance = texts_list.concordance('people', lines = 135) #linhas de concordância

# colocando para string
texts_str = str(texts_clean)

# fazendo o POS tagging com spacy
#print(texts_str)
import spacy
nlp = spacy.load("en_core_web_sm")

# aplicando o modelo da spacy
doc = nlp(texts_str)

#transformando as tags + palavras em um dataframe
spacy_tag = [(word, word.lemma_, word.tag_, word.pos_, word.dep_, ) for word in doc]
text_df = pd.DataFrame(spacy_tag)
text_df.columns = ['word', 'lemma', 'tags', 'pos', 'dep']

print(text_df['pos'].value_counts())

print(text_df['lemma'].value_counts()[:10])

#vendo os nomes
nouns_df = text_df.loc[text_df['pos'] == 'NOUN']
nouns_df2 = nouns_df[["word", "lemma"]]
nouns_df2

#vendo os verbos
verbs_df = text_df.loc[text_df['pos'] == 'VERB']
verbs_df2 = verbs_df[["word", "lemma"]]

#verbs_df.groupby('lemma').count()
# verbs_df['lemma'].value_counts(normalize=True)
lemma_verb = pd.DataFrame(verbs_df['lemma'])
# lemma_verb.columns = ['word', 'lemma']
lemma_verb = lemma_verb.drop_duplicates()
lemma_verb

# tirando a polaridade (https://www.analyticsvidhya.com/blog/2021/06/rule-based-sentiment-analysis-in-python/0)
!pip install vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# function to calculate vader sentiment
def vadersentimentanalysis(word):
    vs = analyzer.polarity_scores(word)
    return vs['compound']
lemma_verb['vader sentiment'] = lemma_verb['lemma'].apply(vadersentimentanalysis)

# function to analyse
def vader_analysis(compound):
    if compound >= 0.5:
        return 'Positive'
    elif compound <= -0.5 :
        return 'Negative'
    else:
        return 'Neutral'
lemma_verb['vader analysis'] = lemma_verb['vader sentiment'].apply(vader_analysis)

#analise de sentimento dos verbos pelo lema
lemma_verb['vader analysis'].value_counts()

#analise de sentimentos dos nomes
nouns_df['vader sentiment'] = nouns_df['lemma'].apply(vadersentimentanalysis)
nouns_df['vader analysis'] = nouns_df['vader sentiment'].apply(vader_analysis)
nouns_df['vader analysis'].value_counts()

#analise de sentimento nos lemas de todo o corpus
text_df['vader sentiment'] = text_df['lemma'].apply(vadersentimentanalysis)
text_df['vader analysis'] = text_df['vader sentiment'].apply(vader_analysis)
text_df['vader analysis'].value_counts()

# salvando as palavras e os lemas de todo o corpus em uma planilha
lemma_verb.to_csv(r'/content/drive/MyDrive/Outros/Corpora/MTF_VERBS.csv', index = False)

"""# Questões:


1.   agora temos os significados de cada verbo, como compará-los para saber quais são de ação, estado, natureza, etc? Fazer manualmente?
2. quais corpora seriam interessantes de fazer a comparação?

# **próximos passos**
*   verbos mais frequentes OK
*   contextos gramaticais em que esses verbos aparecem A FAZER
*   análise de polaridade (positivo ou negativo) OK
*   sentido deles (ação, sentimento?) - acredito que é ação já que é uma ameaça A FAZER
*   fazer testes de similaridade com corpora de outros gêneros
"""