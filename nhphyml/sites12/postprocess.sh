#!/bin/bash -
set -o nounset # Treat unset variables as an error

../scripts/remap_ids.py -t fish178_struct_trimmed_codon_aln_safe.phy_nhPhymlGC.tree -m ../data/id_mapping.tsv -o fish178_nhphyml_sites12_gc.nwk

../scripts/remap_ids.py -t fish178_struct_trimmed_codon_aln_safe.phy_nhPhymlGC.tree -m ../data/id_mapping.tsv -o fish178_nhphyml_sites12_gc_lab.nwk -k

../scripts/remap_ids.py -t fish178_struct_trimmed_codon_aln_safe.phy_nhPhymlEq.tree -m ../data/id_mapping.tsv -o fish178_nhphyml_sites12_eq.nwk

../scripts/remap_ids.py -t fish178_struct_trimmed_codon_aln_safe.phy_nhPhymlEq.tree -m ../data/id_mapping.tsv -o fish178_nhphyml_sites12_eq_lab.nwk -k
