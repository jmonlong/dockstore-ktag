#!/usr/bin/env python

import pysam
import argparse

parser = argparse.ArgumentParser(description='Tags reads according to ' +
                                 'the presence/absence of specific khmers.')
parser.add_argument('-b', dest='bam', help='the BAM file', required=True)
parser.add_argument('-k', dest='klist', required=True,
                    help='the file with the list of khmer to use')
parser.add_argument('-o', dest='output', help='the output file', required=True)

args = parser.parse_args()

# Read khmer list
kmer_list = []
for km in open(args.klist, "r"):
    kmer_list.append(km.strip())

# FOR DEBUG
# args.bam = "../../data/LP6005058-DNA_B01.subsampled0001.bam"
# kmer_list = ["ATTAT", "AATAA", "ATATA"]

# Open BAM file
bam = pysam.AlignmentFile(args.bam, "rb")
if(not bam.has_index()):
    print 'Input BAM must be indexed.'
    quit()
totalReads = bam.mapped + bam.unmapped

# Init output file
outf = open(args.output, "w")
outf.write('#' + str(kmer_list) + '\n')
outf.write('#' + str(totalReads) + '\n')

# Tag all reads
reads = bam.fetch(until_eof=True)
for read in reads:
    tag = 0
    for ii, km in enumerate(kmer_list):
        if(km in read.seq):
            tag += 2 << ii
    if(tag > 0):
        outf.write(str(tag) + '\n')

# Close output file
outf.close()
