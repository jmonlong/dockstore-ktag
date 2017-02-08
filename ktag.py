#!/usr/bin/env python

import pysam
import argparse
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy

parser = argparse.ArgumentParser(description='Tags reads according to ' +
                                 'the presence/absence of specific khmers.')
parser.add_argument('-b', dest='bam', help='the BAM file', required=True)
parser.add_argument('-k', dest='klist', required=True,
                    help='the file with the list of khmer to use')
parser.add_argument('-rf', dest='rff', required=True,
                    help='the trained RF classifier')
parser.add_argument('-s', dest='chunkSize', default=10000, type=int,
                    help='number of reads analyzed in a chunk')
parser.add_argument('-o', dest='output', default='ktag_output.tsv',
                    help='the output file')

args = parser.parse_args()

# Read khmer list
kmer_list = []
for km in open(args.klist, "r"):
    kmer_list.append(km.strip())

# Load random forest classifier
rfc = RandomForestClassifier()
rfc = joblib.load(args.rff)

# Open BAM file
bam = pysam.AlignmentFile(args.bam, "rb")

# Init output file
outf = open(args.output, "w")
outf.write('#khmers:' + str(kmer_list) + '\n')
outf.write('#RF: ' + args.rff + '\n')

# Tag all reads
totalReads = 0
reads = bam.fetch(until_eof=True)
pred_counts = numpy.zeros((4, len(rfc.classes_)))
X = []
for read in reads:
    totalReads += 1
    if(totalReads % args.chunkSize == 0):
        predprobs = rfc.predict_proba(X)
        pred_counts[0, ] += sum(predprobs > .5)
        pred_counts[1, ] += sum(predprobs > .9)
        pred_counts[2, ] += sum(predprobs > .95)
        pred_counts[3, ] += sum(predprobs > .99)
        X = []
    x = [km in read.seq for km in kmer_list]
    X.append(x)
if(len(X) > 0):
    predprobs = rfc.predict_proba(X)
    pred_counts[0, ] += sum(predprobs > .5)
    pred_counts[1, ] += sum(predprobs > .9)
    pred_counts[2, ] += sum(predprobs > .95)
    pred_counts[3, ] += sum(predprobs > .99)

# Write counts
for ii, c in enumerate(rfc.classes_):
    outf.write('.5\t' + c + '\t' + str(pred_counts[0, ii]) + '\n')
    outf.write('.9\t' + c + '\t' + str(pred_counts[1, ii]) + '\n')
    outf.write('.95\t' + c + '\t' + str(pred_counts[2, ii]) + '\n')
    outf.write('.99\t' + c + '\t' + str(pred_counts[3, ii]) + '\n')

# Record the total number of reads
outf.write('0\ttotal\t' + str(totalReads) + '\n')

# Close output file
outf.close()
