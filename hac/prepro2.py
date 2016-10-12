__author__ = 'xzzhang'

import json
import string
import pickle
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

from nltk.tag.tnt import TnT
from nltk.corpus import brown
train_sents = brown.tagged_sents()
tagger = TnT()
tagger.train(train_sents)

punct = [c for c in string.punctuation]

def main():
    output = list() # list of sentence with token of form (tag, parent_index, level)
    wc = 0 # word count
    uc = 0 # unknown token count
    with open("tip.json", 'r') as f:
        lcnt = 0
        for line in f:
            data = json.loads(line)
            text = data['text']
            sents = sent_tokenize(text)
            for sent in sents:
                # removal of punctuation, ellipsis and currency
                raw_tokens = word_tokenize(sent)
                tokens = [t for t in raw_tokens if t not in punct]
                wc += len(tokens)
                tuples = tagger.tag(tokens)
                osent = list()
                for t in tuples:
                    if t[1] == 'Unk':
                        uc += 1
                    if t[1] == 'VB':
                        ot = t[1]+','+t[0].lower()
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

