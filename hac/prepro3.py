__author__ = 'xzzhang'

import sys
import json
import string
import pickle
import nltk
import numpy
#from nltk.tokenize import sent_tokenize
#from nltk.tokenize import word_tokenize

#from nltk.tag.tnt import TnT
#from nltk.corpus import brown
#import nltk
#d = nltk.downloader.Downloader()
#d.url = 'https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml'
#d.download()

#train_sents = brown.tagged_sents()
#tagger = TnT()
#tagger.train(train_sents)

punct = [c for c in string.punctuation]

def main():
    output = list() # list of sentence with token of form (tag, parent_index, level)
    wc = 0 # word count
    uc = 0 # unknown token count
    if len(sys.argv) < 2:
        print("Usage:\t{0} <JSON file_name>".format(sys.argv[0]))
        return;

    with open(sys.argv[1], 'r') as f:
        lcnt = 0
        for line in f:
            data = json.loads(line)
            text = data['text']
            sents = nltk.sent_tokenize(text)
            for sent in sents:
                # removal of punctuation, ellipsis and currency
                raw_tokens = nltk.word_tokenize(sent)
                tokens = [t for t in raw_tokens if t not in punct]
                wc += len(tokens)
                tuples = nltk.pos_tag(tokens)
                osent = list()
                for t in tuples:
                    if t[1] == 'Unk':
                        uc += 1
                    #if t[1].startswith('VB'):
                    #    ot = t[1]+','+t[0].lower()
                    else:
                        ot = t[1]
                    osent.append((ot,-1,-1))
                output.append(osent)

            lcnt += 1
            if lcnt > 10:
                break
    print float(uc) / wc
    
    pickle.dump(output, open("a.p", "wb"))

if __name__ == "__main__":
    main()

