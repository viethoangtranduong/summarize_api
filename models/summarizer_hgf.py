from transformers import pipeline
from nltk import sent_tokenize

summarizer = pipeline("summarization")


def hgf(text, max_length = 130, min_length = 30):
  try:
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    sentences = sent_tokenize(summary)
  
    # output
    output = {'sentences': summary, 'summary_num_sentences': len(sentences), "method": "hgf"}

    return output    
  except:
    print('Error:', text)
    output = {'sentences': "", 'summary_num_sentences': 0, "method": "hgf"}
    return output