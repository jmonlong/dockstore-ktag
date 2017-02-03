#!/usr/bin/env python

import pysam
import argparse

parser = argparse.ArgumentParser(description='Tags reads according to ' +
                                 'the presence/absence of specific khmers.')
parser.add_argument('-b', dest='bam', help='the BAM file', required=True)
parser.add_argument('-k', dest='klist', required=True,
                    help='the file with the list of khmer to use')
parser.add_argument('-o', dest='output', default='ktag_output.txt',
                    help='the output file')

args = parser.parse_args()

# Read khmer list
kmer_list = []
for km in open(args.klist, "r"):
    kmer_list.append(km.strip())

# Open BAM file
bam = pysam.AlignmentFile(args.bam, "rb")

# Init output file
outf = open(args.output, "w")
outf.write('#' + str(kmer_list) + '\n')

# Tag all reads
totalReads = 0
reads = bam.fetch(until_eof=True)
for read in reads:
    totalReads += 1
    tag = 0
    for ii, km in enumerate(kmer_list):
        if(km in read.seq):
            tag += 2 << ii
    if(tag > 0):
        outf.write(str(tag) + '\n')

# Record the total number of reads
outf.write('#' + str(totalReads) + '\n')

# Close output file
outf.close()
