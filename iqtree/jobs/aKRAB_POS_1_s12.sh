#!/bin/bash -
        set -o nounset # Treat unset variables as an error
        WORKDIR=$RES_ROOT/aKRAB_POS_1_s12/
        mkdir -p $WORKDIR
        cd $WORKDIR

        seqkit grep -n -p "GCF_013368585.1_Megalops_cyprinoides,GCF_963514075.1_Conger_conger,GCF_013347855.1_Anguilla_anguilla" $DATA_ROOT/merged_codon_sites12.fas > aKRAB_POS_1_s12.fas

        iqtree3 -s aKRAB_POS_1_s12.fas -m "12.12+R3" -pre aKRAB_POS_1_s12 -m "12.12+R3" --redo --nonrev-model -asr -T 32
        