<<<<<<< HEAD
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

=======
import pickle
import re
import string

punct1 = [s for s in string.punctuation]
punct2 = ['``', "''", '...', '--']
punct = set(punct1 + punct2)

tagged_sents = "/afs/cs.pitt.edu/usr0/xiaozhong/public/cs2731/pos_tagged_sentences.txt"
sent_cnt_limit = 1000
default_head_idx = -1
default_reduc_lv = -1

def main():
    corpus = list()
    with open(tagged_sents) as f:
        sent_cnt = 0;
        for sent in f:
            res = list()
            tuples = re.findall('\(.*?\)(?=\s)', sent)
            for t in tuples:
                #print t
                word, tag = re.findall('(?<=["\'])\S+(?=["\'])', t)
                if word in punct:
                    continue
                if tag.startswith('VB'):
                    tt = "{},{}".format(tag,word.lower())
                    res.append((tt, default_head_idx, default_reduc_lv))
                else:
                    res.append((tag, default_head_idx, default_reduc_lv))
            corpus.append(res)
            sent_cnt += 1
            if (sent_cnt >= sent_cnt_limit):
                break
#    for s in corpus:
#        print s
    pickle.dump(corpus, open('a.p', 'wb'))

if __name__ == "__main__":
    main()
>>>>>>> 3c1802c198ef2aecec9dc64ca6e4fafd3a8d81d7
