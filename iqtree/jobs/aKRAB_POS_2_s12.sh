#!/bin/bash -
        set -o nounset # Treat unset variables as an error
        WORKDIR=$RES_ROOT/aKRAB_POS_2_s12/
        mkdir -p $WORKDIR
        cd $WORKDIR

        seqkit grep -n -p "GCA_048544225.1_Coilia_mystus,GCA_963457725.1_Sprattus_sprattus,GCF_963854185.1_Sardina_pilchardus,GCF_018492685.1_Alosa_sapidissima" $DATA_ROOT/merged_codon_sites12.fas > aKRAB_POS_2_s12.fas

        iqtree3 -s aKRAB_POS_2_s12.fas -m "12.12+R3" -pre aKRAB_POS_2_s12 -m "12.12+R3" --redo --nonrev-model -asr -T 32
        