#!/usr/bin/env python

import pysam
import argparse
import pickle
from sklearn.ensemble import RandomForestClassifier

parser = argparse.ArgumentParser(description='Tags reads according to ' +
                                 'the presence/absence of specific khmers.')
parser.add_argument('-b', dest='bam', help='the BAM file', required=True)
parser.add_argument('-k', dest='klist', required=True,
                    help='the file with the list of khmer to use')
parser.add_argument('-rf', dest='rff', required=True,
                    help='the trained RF classifier')
parser.add_argument('-p', dest='probmin', default=.9, type=float,
                    help='the trained RF classifier')
parser.add_argument('-o', dest='output', default='ktag_output.txt',
                    help='the output file')

args = parser.parse_args()

# Read khmer list
kmer_list = []
for km in open(args.klist, "r"):
    kmer_list.append(km.strip())

# Load random forest classifier
rfc = RandomForestClassifier()
rfc = pickle.load(open(args.rff, "rb"))

# Open BAM file
bam = pysam.AlignmentFile(args.bam, "rb")

# Init output file
outf = open(args.output, "w")
outf.write('#khmers:' + str(kmer_list) + '\n')
outf.write('#RF: ' + args.rff + '\n')

# Tag all reads
totalReads = 0
reads = bam.fetch(until_eof=True)
pred = {}
for c in rfc.classes_:
    pred[c] = 0
for read in reads:
    totalReads += 1
    x = []
    for ii, km in enumerate(kmer_list):
        if(km in read.seq):
            x.append(True)
        else:
            x.append(False)
    predprobs = rfc.predict_proba([x])[0]
    for ii, prob in enumerate(predprobs):
        if(prob > args.probmin):
            pred[rfc.classes_[ii]] += 1

# Write counts
for c in rfc.classes_:
    outf.write(c + '\t' + str(pred[c]) + '\n')

# Record the total number of reads
outf.write('total\t' + str(totalReads) + '\n')

# Close output file
outf.close()
