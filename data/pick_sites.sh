#!/bin/bash -
set t -o nounset # Treat unset variables as an error

../scripts/pick_third_sites.py -i fish178_struct_trimmed_codon_aln.fas -o fish178_struct_trimmed_codon_sites3_aln.fas
../scripts/remove_third_sites.py -i fish178_struct_trimmed_codon_aln.fas -o fish178_struct_trimmed_codon_sites12_aln.fas
