import pickle
import copy
from nltk.util import ngrams
import operator
from math import log


#===========================================================================
#       Dependency Model
#===========================================================================

class DependencyModel:
    def __init__(self):
        self.pair = ()

    def _compute_model_parameters(self, side):
        best_pair = None
        max_prob = 0
        raw_bigram = {}
        s = next_sent(side)
        while s != None:
            for dep_pair in ngrams(s, 2):
                if raw_bigram.has_key(dep_pair):
                    raw_bigram[dep_pair] += 1
                    #due to performance gain, compute max while creating bigrams
                    if raw_bigram[dep_pair] > max_prob:
                        best_pair = dep_pair
                        max_prob = raw_bigram[dep_pair]
                else:
                    raw_bigram[dep_pair] = 1

            s = next_sent(side)        

        model_probability = 0
        model_sum = float(sum(raw_bigram.values()))

        #due to performance gain
        view = raw_bigram.values()
        for value in view:
            p = value/model_sum
            model_probability += p * log(p,2)

        return {"model": model_probability, "pair": best_pair}

    def get_dependency(self):
        #first iteration
        if self.pair == ():
            res = self._compute_model_parameters(1)
            self.pair = res["pair"]

        return self.pair   

    def decide_side(self):
        res1 = self._compute_model_parameters(1)
        res2 = self._compute_model_parameters(2)
        
        print("Left model: {0}, right model: {1}".format(res1["model"], res2["model"]))
        side = "left"
        self.pair = res1["pair"]
        if (res2["model"] > res1["model"]):
            self.pair = res2["pair"]
            side = "right"
        
        return side

#===========================================================================
#       HAC Implementation
#===========================================================================

c1 = pickle.load(open("a.p", "rb")) # for dependency with h->d
c2 = copy.deepcopy(c1)  # for dependency with d<-h
ln = 0  # sentence iterator
lv = 0  # reduction level
pcnt = 0 # proposal count

cs = list() # complete sentence
cs.append(('DT',1,1))
cs.append(('NN',-1,-1))

def main():
    global dep_model
    dep_model = DependencyModel()
    global c1
    global c2
    global pcnt
    print 'Corpus before reduction:'
    #print_raw_corpus()
    #print_corpus()
    while reduce():
        #side = choose_side()
        side = dep_model.decide_side()
        if side == 'left':
            c2 = copy.deepcopy(c1)
        else:
            c1 = c2
            c2 = copy.deepcopy(c1)
    print 'Corpus after reduction:'
    print_raw_corpus()
    pickle.dump(c1, open("b.p", "wb"))    

def reduce():
    global dep_model
    global c1
    global c2
    global lv
    global pcnt
    reduced = False
    pair = dep_model.get_dependency()
    #pair = propose()
    print 'Porposed pair: {}'.format(pair)
    pcnt += 1
    if pair == None:
        # no more proposal
        return False
    [tg1, tg2] = pair
    #print (tg1, tg2)
    for sidx,s in enumerate(c1):
        if complete(s):
            continue
        h = -2 # head index
        skip = 0
        for i in range(len(s)):
            if not valid(s[i]):
                skip += 1
                continue
            if s[i][0] == tg2 and i == h + skip + 1:
                # begin reduce
                reduced = True
                s[i] = (tg2, h, lv)
                print 'c1 suggests to set sentence {} word {} to {}'.format(sidx, i, s[i])
                skip += 1
                continue
            if s[i][0] == tg1:
                skip = 0
                h = i
    for sidx,s in enumerate(c2):
        if complete(s):
            continue
        leng = len(s)
        h = leng + 1
        skip = 0
        for ii in range(leng):
            i = leng - ii - 1
            if not valid(s[i]):
                skip += 1
                continue
            if s[i][0] == tg1 and i == h - skip -1:
                reduced = True
                s[i] = (tg1, h, lv)
                print 'c2 suggests to set sentence {} word {} to {}'.format(sidx, i, s[i])
                skip += 1
                continue
            if s[i][0] == tg2:
                skip = 0
                h = i
    lv += 1
    return reduced

def print_raw_corpus():
    for s in c1:
        print s

def print_corpus():
    s = next_sent(1)
    while s != None:
        print s
        s = next_sent(1)

        
def choose_side():
    return 'left'
    
def next_sent(flag):
    global ln
    global c1
    global c2
    if flag == 1:
        c = c1
    else:
        c = c2
    if ln == len(c):
        ln = 0
        return None
    while complete(c[ln]):
        ln += 1
        if ln == len(c):
            ln = 0
            return None
    ret = list()
    for t in c[ln]:
        if valid(t):
            ret.append(t[0])
    ln += 1
    return ret


def propose():
    # get most probable tag pair in the current run
    pair = list()
    for sent in c1:
        if not complete(sent):
            for t in sent:
                if valid(t):
                    pair.append(t)
                if len(pair) == 2:
                    return (pair[0][0], pair[1][0])
    return None


def valid(t):
    # check if the token has not been reduced
    return t[1] == -1

def complete(s):
    # check if parsing is complete for this sentence
    return llen(s) < 2

def llen(s):
    # returns count of unreduced tokens in a sentence
    cnt = 0
    for t in s:
        if valid(t):
            cnt += 1
    return cnt


if __name__ == "__main__":
    main()
