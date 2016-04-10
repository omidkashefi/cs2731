import pickle

default_head_idx = -1

def main():
    sent_idx = 0
    sents = pickle.load(open('b.p', 'rb'))
    with open('c.txt', 'w') as f:
        for sent in sents:
            f.write(str(sent_idx))
            for tidx,t in enumerate(sent):
                if t[1] != default_head_idx:
                    f.write(",{}-{}".format(t[1],tidx))
            f.write('\n')
            sent_idx += 1


if __name__ == "__main__":
    main()
