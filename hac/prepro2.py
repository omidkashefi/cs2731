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
