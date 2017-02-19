#!/usr/bin/env python

import pysam
import argparse
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy
import random
import subprocess

parser = argparse.ArgumentParser(description='Tags reads according to ' +
                                 'the presence/absence of specific khmers.')
parser.add_argument('-b', dest='bam', help='the BAM file')
parser.add_argument('-icgc', dest='icgc', help='the ICGC file id')
parser.add_argument('-k', dest='khmer_list', required=True,
                    help='the file with the list of khmer to use')
parser.add_argument('-rf', dest='rf_class', required=True,
                    help='the trained RF classifier')
parser.add_argument('-c', dest='chunk_size', default=10000, type=int,
                    help='number of reads analyzed in a chunk')
parser.add_argument('-s', dest='supsamp', default=.5, type=float,
                    help='proportion of reads to downsample.')
parser.add_argument('-o', dest='output', default='ktag_output.tsv',
                    help='the output file')

args = parser.parse_args()

# Read khmer list
kmer_list = []
for km in open(args.khmer_list, "r"):
    kmer_list.append(km.strip())

# Load random forest classifier
rfc = RandomForestClassifier()
rfc = joblib.load(args.rf_class)

# Open BAM file
if("bam" not in args and "icgc" not in args):
    print "At least on of '-b' or '-icgc' is needed."
if("bam" in args):
    bam = pysam.AlignmentFile(args.bam, "rb")
else:
    cmd = ['icgc-storage-client', 'download', '--object-id', args.icgc,
           '--output-dir', '.', '--output-layout', 'id']
    dump = open('/dev/null')
    cmd_out = subprocess.check_output(cmd, stderr=dump)
    dump.close()
    bam = pysam.AlignmentFile(args.icgc, "rb")

# Init output file
outf = open(args.output, "w")
outf.write('#khmers:' + str(kmer_list) + '\n')
outf.write('#RF: ' + args.rf_class + '\n')

# Tag all reads
total_reads = 0
reads = bam.fetch(until_eof=True)
pred_counts = numpy.zeros((4, len(rfc.classes_)))
X = []
for read in reads:
    if(len(X) > 0 and len(X) % args.chunk_size == 0):
        predprobs = rfc.predict_proba(X)
        pred_counts[0, ] += sum(predprobs > .5)
        pred_counts[1, ] += sum(predprobs > .9)
        pred_counts[2, ] += sum(predprobs > .95)
        pred_counts[3, ] += sum(predprobs > .99)
        X = []
    if(random.random() < args.subsamp):
        total_reads += 1
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
outf.write('0\ttotal\t' + str(total_reads) + '\n')

# Close output file
outf.close()
