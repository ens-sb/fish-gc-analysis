#!/bin/bash -
set -o nounset # Treat unset variables as an error
seqkit grep -f akrab_pos.tsv ../../../data/fish178_struct_trimmed_codon_sites3_aln.fas -o fish178_struct_trimmed_codon_sites3_aln_akrab_pos.fas
