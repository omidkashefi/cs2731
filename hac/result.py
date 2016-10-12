import pickle

default_head_idx = -1

def main():
    sent_idx = 0
    sents = pickle.load(open('b_baseline.p', 'rb'))
    with open('c_baseline.txt', 'w') as f:
        for sent in sents:
            if len(sent) > 0:
                f.write(str("{}:0-0".format(sent_idx)))
                for tidx,t in enumerate(sent):
                    if t[1] != default_head_idx:
                        f.write(",{}-{}".format(tidx+1,t[1]+1))
                f.write('\n')
            sent_idx += 1


if __name__ == "__main__":
    main()
