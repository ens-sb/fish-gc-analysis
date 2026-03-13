#!/bin/bash -
set -o nounset # Treat unset variables as an error

iqtree3 -s fish178_struct_trimmed_codon_sites3_aln_akrab_neg.fas -mset 12.12,6.7a,3.3a -m MFP --redo --merit AICc --nonrev-model -safe
