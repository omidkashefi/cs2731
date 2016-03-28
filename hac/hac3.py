import pickle
import copy

c1 = pickle.load(open("a.p", "rb")) # for dependency with h->d
c2 = copy.deepcopy(c1)  # for dependency with d<-h
ln = 0  # sentence iterator
lv = 0  # reduction level
pcnt = 0 # proposal count

cs = list() # complete sentence
cs.append(('DT',1,1))
cs.append(('NN',-1,-1))

def main():
    global c1
    global c2
    global pcnt
    print 'Corpus before reduction:'
    print_raw_corpus()
    while reduce():
        side = choose_side()
        if side == 'left':
            c2 = copy.deepcopy(c1)
        else:
            c1 = c2
            c2 = copy.deepcopy(c1)
    print 'Corpus after reduction:'
    print_raw_corpus()
    pickle.dump(c1, open("b.p", "wb"))    

def reduce():
    global c1
    global c2
    global lv
    global pcnt
    reduced = False
    pair = propose()
    print 'Porposed pair: {}'.format(pair)
    pcnt += 1
    if pair == None:
        # no more proposal
        return False
    [tg1, tg2] = pair
    print (tg1, tg2)
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
