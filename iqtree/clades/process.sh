#!/bin/bash -
set -o nounset # Treat unset variables as an error

../scripts/process_clades.py --neg Selected_Clades_neg_3.tsv \
	--pos Selected_Clades_pos_3.tsv \
	--un Selected_Clades_un_3.tsv \
	--outdir processed