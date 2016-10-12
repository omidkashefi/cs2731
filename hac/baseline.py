import pickle
import random

def main():
    c = pickle.load(open("a.p", "rb"))

    for sent in c:
        if len(sent) > 0:
            vb_idx = list()
            for tidx,t in enumerate(sent):
                if t[0].startswith("VB"):
                    vb_idx.append(tidx)
            if len(vb_idx) == 0:
                # skip sentence without a verb
                continue
            root = random.choice(vb_idx)
            for i in range(root-1,-1,-1):
                sent[i] = (sent[i][0],root,-1)
            for i in range(root+1,len(sent)):
                sent[i] = (sent[i][0],root,-1)

    pickle.dump(c, open("b_baseline.p", "wb"))


if __name__ == "__main__":
    main()
