# from transformers import *
import transformers
from summarizer import Summarizer as summarizer_bert
from aylienapiclient import textapi
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')

# Load model, model config and tokenizer via Transformers
custom_config = transformers.AutoConfig.from_pretrained('bert-base-cased')
custom_config.output_hidden_states = True
custom_tokenizer = transformers.AutoTokenizer.from_pretrained('bert-base-cased')
custom_model = transformers.AutoModel.from_pretrained('bert-base-cased', config=custom_config)
summarizer_bert_model = summarizer_bert(custom_model=custom_model, custom_tokenizer=custom_tokenizer, )

def summarizer_bert_get(text_url, text, num_sentences):
  if not num_sentences:
      num_sentences = int(len(sent_tokenize(text))**(1/2))
  try:

    # Filter unneccessary information
    citations = {"References:", "Reference:", "Citations:", "Citation:", "Resources:", "Bibliography:" "Resource:", "Author Bio:", "Author bio:", "author bio:"}

    current_l = len(text)
    for word in citations:
      try:
        idx = text.index(word)
        text = text[:idx]
      except:
        pass

      # check if accidentally cut all the text
      if len(text) < current_l/3:
        raise ValueError

    # 2nd round of filter
    sentences = sent_tokenize(text)
    filtered = set()
    for i, sentence in enumerate(sentences):
      if sentence[-1] in {"?", ":"} or sentence[-5:-1] in {'here', 'poor'} or sentence[:2] in {"By"} or len(sentence) < 10:
        filtered.add(sentence)
    
    new_sentences = [" " + sentence for sentence in sentences if sentence not in filtered]
    new_text = "".join(new_sentences)
    total_sentences = len(new_sentences)

    # # use for local testing only
    if not num_sentences:
      num_sentences = int(total_sentences**(1/2)) + 1
    
    # print(num_sentences, total_sentences)
    summary = summarizer_bert_model(new_text, ratio = (num_sentences + 1) / max(total_sentences, 1))

    # split into sub-sentences
    sentences = sent_tokenize(summary)
    
    # output
    output = {'sentences': summary, 'summary_num_sentences': len(sentences), "method": "bert"}
    print("Bert transformer works!")
  except:
    
  
    output = {}

    client = textapi.Client("79e389d3", "1bc2400da0cb4745c30fb68b67e5e5cf")

    if text_url:
        out = client.Summarize({'url': text_url,
                                'sentences_number': num_sentences})
    else:
        out = client.Summarize({'sentences_number': num_sentences,
                                'text': text,
                                'title': "Class reading"})

    output['summary_num_sentences'] = num_sentences
    output['sentences'] = "".join([" " + val for val in out['sentences']])[1:]
    output['method'] = "aylien"
    print("Bert transformer failed! Use aylien")
  return output


def summarizer_bert_get(text_url, text, num_sentences):
  if not num_sentences:
      num_sentences = int(len(sent_tokenize(text))**(1/2))
  else:
      num_sentences = int(num_sentences)

  # Filter unneccessary information
  citations = {"References:", "Reference:", "Citations:", "Citation:", "Resources:", "Bibliography:" "Resource:", "Author Bio:", "Author bio:", "author bio:"}

  current_l = len(text)
  for word in citations:
    try:
      idx = text.index(word)
      text = text[:idx]
    except:
      pass

    # check if accidentally cut all the text
    if len(text) < current_l/3:
      raise ValueError

  # 2nd round of filter
  sentences = sent_tokenize(text)
  filtered = set()
  for i, sentence in enumerate(sentences):
    if sentence[-1] in {"?", ":"} or sentence[-5:-1] in {'here', 'poor'} or sentence[:2] in {"By"} or len(sentence) < 10:
      filtered.add(sentence)
  
  new_sentences = [" " + sentence for sentence in sentences if sentence not in filtered]
  new_text = "".join(new_sentences)
  total_sentences = len(new_sentences)

  # # use for local testing only
  if not num_sentences:
    num_sentences = int(total_sentences**(1/2)) + 1
  
  print("haha", type(num_sentences), type(total_sentences), type(new_text))
  # print(num_sentences, total_sentences)
  summary = summarizer_bert_model(new_text, ratio = (num_sentences + 1) / max(total_sentences, 1))

  # split into sub-sentences
  sentences = sent_tokenize(summary)
  
  # output
  output = {'sentences': summary, 'summary_num_sentences': len(sentences), "method": "bert"}
  print("Bert transformer works!")
  return output