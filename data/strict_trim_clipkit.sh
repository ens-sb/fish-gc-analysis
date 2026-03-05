#!/bin/bash -
set -o nounset # Treat unset variables as an error

clipkit -m gappy --codon merged_codon_alns.fas -o fish178_struct_trimmed_codon_aln.fas -g 0.01 -t 32
