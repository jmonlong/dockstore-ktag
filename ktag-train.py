#!/usr/bin/env python

import argparse
import pickle
from sklearn.ensemble import RandomForestClassifier

parser = argparse.ArgumentParser(description='Train a RF classifer using ' +
                                 'the presence/absence of specific khmers.')
parser.add_argument('-i', dest='tfile', help='the file with training data', required=True)
parser.add_argument('-k', dest='klist', required=True,
                    help='the file with the list of khmer to use')
parser.add_argument('-t', dest='ntrees', default=10, type=int,
                    help='the file with the list of khmer to use')
parser.add_argument('-o', dest='output', default='ktag_classifier.pkl',
                    help='the output file')

args = parser.parse_args()

# Read khmer list
kmer_list = []
for km in open(args.klist, "r"):
    kmer_list.append(km.strip())

# Read training data
inf = open(args.tfile, "r")
X = []
Y = []
headers = inf.next()
for read in inf:
    x = []
    read = read.rstrip()
    read = read.split('\t')
    for km in kmer_list:
        if(km in read[0]):
            x.append(True)
        else:
            x.append(False)
    X.append(x)
    Y.append(read[1])
inf.close()

# Random Forest
rfc = RandomForestClassifier(n_estimators=args.ntrees, oob_score=True)
rfc = rfc.fit(X, Y)
print 'OOB score:' + str(rfc.oob_score_)

# Save classifier
pickle.dump(rfc, open(args.output, "wb"))