#!/bin/bash - 
set -o nounset                              # Treat unset variables as an error

../../scripts/tanglegram ../../../data/rooted_corefu_iqtree_nuc_sites3.treefile ../fish178_nhphyml_sites3_gc.nwk corefu_prot_vs_nhphyml_sites3.pdf

