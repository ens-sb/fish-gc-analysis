#!/bin/bash -
set t -o nounset # Treat unset variables as an error

../scripts/map_ids.py -f ../../data/fish178_struct_trimmed_codon_aln.fas -t ../../data/rooted_corefu_iqtree_nuc_sites3.treefile \
	-p fish178_struct_trimmed_codon_aln_safe.phy -o rooted_corefu_iqtree_nuc_sites3_safe.nwk
