from aylienapiclient import textapi
from nltk import sent_tokenize

def summarize_aylien2_text(text, num_sentences = None):
    try:
        # # use for local testing only
        if not num_sentences:
            sentences = sent_tokenize(text)
            total_sentences = len(sentences)
            num_sentences = int(total_sentences**(1/2)) + 1

        output = {}

        client = textapi.Client("79e389d3", "1bc2400da0cb4745c30fb68b67e5e5cf")

        out = client.Summarize({'sentences_number': num_sentences,
                                'text': text,
                                'title': None})

        output['summary_num_sentences'] = num_sentences
        output['sentences'] = "".join([" " + val for val in out['sentences']])[1:]
        output['method'] = "aylien"
        return output
    except: 
        print('Error:', text)
        output = {'sentences': "", 'summary_num_sentences': 0, "method": "tfidf"}
        return output