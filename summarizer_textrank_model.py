import numpy as np
import pandas as pd
import nltk
from aylienapiclient import textapi
# nltk.download('punkt') # one time execution
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
stop_words = stopwords.words('english')
import re
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

# function to remove stopwords
def remove_stopwords(sen):
    sen_new = " ".join([i for i in sen if i not in stop_words])
    return sen_new

# Extract word vectors
word_embeddings = {}
print("start loading vectorization")
f = open('./vectorization/glove.6B.100d.txt', encoding='utf-8')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    word_embeddings[word] = coefs
f.close()

def summarizer_textrank_get(text_url, txt, num_sentences = None):
  try:
    sentences = []
    for s in [txt]:
      sentences.append(sent_tokenize(s))

    sentences = [y for x in sentences for y in x] # flatten list

    # remove punctuations, numbers and special characters
    clean_sentences = pd.Series(sentences).str.replace("[^a-zA-Z]", " ")

    # make alphabets lowercase
    clean_sentences = [s.lower() for s in clean_sentences]

    # remove stopwords from the sentences
    clean_sentences = [remove_stopwords(r.split()) for r in clean_sentences] 

    sentence_vectors = []
    for i in clean_sentences:
      if len(i) != 0:
        v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
      else:
        v = np.zeros((100,))
      sentence_vectors.append(v)


    # similarity matrix
    sim_mat = np.zeros([len(sentences), len(sentences)])

    for i in range(len(sentences)):
      for j in range(len(sentences)):
        if i != j:
          sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]

    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)

    summary = ""

    if not num_sentences:
      num_sentences = int(np.sqrt(len(ranked_sentences))) + 1
    else:
      num_sentences = int(num_sentences)
    # Extract top 10 sentences as the summary
    for i in range(num_sentences):
      summary += ranked_sentences[i][1] + " "
    sentences = sent_tokenize(summary)
    
    # output
    output = {'sentences': summary[:-1], 'summary_num_sentences': len(sentences), "method": "textrank"}

    return output
  except:
    try:
      if not num_sentences:
        num_sentences = int(np.sqrt(len(sent_tokenize(txt)))) + 1
      else:
        num_sentences = int(num_sentences)
      output = {}

      client = textapi.Client("79e389d3", "1bc2400da0cb4745c30fb68b67e5e5cf")

      if text_url:
          out = client.Summarize({'url': text_url,
                                  'sentences_number': num_sentences})
      else:
          out = client.Summarize({'sentences_number': num_sentences,
                                  'text': txt,
                                  'title': "Class reading"})

      output['summary_num_sentences'] = num_sentences
      output['sentences'] = "".join([" " + val for val in out['sentences']])[1:]
      output['method'] = "aylien"
      print("TextRank failed! Use aylien")
    except:
      print('Error:', txt[:10])
      output = {'sentences': "", 'summary_num_sentences': 0, "method": "textrank"}
      return output
