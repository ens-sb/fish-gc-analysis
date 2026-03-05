#!/bin/bash -
set -o nounset # Treat unset variables as an error

nhPhyml -format=s -sequences=fish178_struct_trimmed_codon_aln_safe.phy \
	-tree=../data/rooted_corefu_iqtree_nuc_sites3_safe.nwk -positions=12 -tstv=e -rates=4 -alpha=e \
	-topology=e -eqfreq=lim -numeqfreq=10 -eqfreqlow=0.4 -eqfrequpp=0.9
