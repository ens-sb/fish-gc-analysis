#!/bin/bash -
        set -o nounset # Treat unset variables as an error
        WORKDIR=$RES_ROOT/aKRAB_NEG_1_s12/
        mkdir -p $WORKDIR
        cd $WORKDIR

        seqkit grep -n -p "GCF_029633855.1_Hoplias_malabaricus,GCF_030463535.1_Salminus_brasiliensis,GCF_023375975.1_Astyanax_mexicanus,GCF_015220715.1_Pygocentrus_nattereri,GCF_030014385.1_Trichomycterus_rosablanca,GCA_946808225.1_Silurus_aristotelis,GCA_024256435.1_Clarias_gariepinus,GCF_027579695.1_Neoarius_graeffei,GCF_027358585.1_Pangasianodon_hypophthalmus" $DATA_ROOT/merged_codon_sites12.fas > aKRAB_NEG_1_s12.fas

        iqtree3 -s aKRAB_NEG_1_s12.fas -m "12.12+R3" -pre aKRAB_NEG_1_s12 -m "12.12+R3" --redo --nonrev-model -asr -T 32
        