import pickle
import copy

c1 = pickle.load(open("a.p", "rb")) # for dependency with h->d
c2 = copy.deepcopy(c1)  # for dependency with d<-h
ln = 0  # sentence iterator
lv = 0  # reduction level
rec = False # true if in the recursive reduction
pair = tuple()  # current dependency pair
pcnt = 0    # proposal count
side = 'left' # means which side of the dependency is the head

cs = list() # complete sentence
cs.append(('DT',1,1))
cs.append(('NN',-1,-1))

def main():
    """
    Main function of the whole program.
    Comment out the print statements before processing big dataset.
    """
    global c1
    global c2
    global rec
    global pcnt
    global side
    print_corpus()
    while True:
        reduced = reduce()
        if not rec and not reduced:
            break
        elif not rec and reduced:
            # change to NgramModule.choose_side() method, which returns 'left' (c1 has higher prob) or 'right'
            side = choose_side()
            rec = True
        elif rec and not reduced:
            rec = False
        else:
            # use the initial side for the dependency pair in recursive reduction
            print 'Use previous direction "{}" in recursive reduction for dependency {}'.format(side, pair)
            pass
        if reduced:
            if side == 'left':
                c2 = copy.deepcopy(c1)
            else:
                c1 = c2
                c2 = copy.deepcopy(c1)
    print 'Proposed {} times.'.format(pcnt)
    pickle.dump(c1, open("b.p", "wb"))    

def reduce():
    global c1
    global c2
    global lv
    global rec
    global pair
    global pcnt
    reduced = False
    if not rec:
        # change here to NgramModule.propose() method, which returns a tuple of two tags
        # After each proposal, a new N-gram model is to be created
        pair = propose()
        pcnt += 1
    else:
        pass
    if pair == None:
        # no more proposal
        return False
    tg1, tg2 = pair
    print 'Recurrent reduction: {}, Porposed pair: {}'.format(rec, pair)
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
                print 'c1 suggests to reduce {} at sentence {} word {}'.format(s[i], sidx, i)
                break
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
                print 'c2 suggests to reduce {} at sentence {} word {}'.format(s[i], sidx, i)
                break 
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
    """
    Args:
        flag: flag=1 to get next sentence from c1, flag=2 for c2

    Returns:
        Next sentence as a list of strings or 'None' if reaches end of corpus

    Raises:

    """
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
