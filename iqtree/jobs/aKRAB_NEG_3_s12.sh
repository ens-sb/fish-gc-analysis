#!/bin/bash -
        set -o nounset # Treat unset variables as an error
        WORKDIR=$RES_ROOT/aKRAB_NEG_3_s12/
        mkdir -p $WORKDIR
        cd $WORKDIR

        seqkit grep -n -p "GCF_901000725.2_Takifugu_rubripes,GCF_900634775.1_Gouania_willdenowi,GCF_009829125.3_Periophthalmus_magnuspinnatus,GCA_951799975.1_Gobius_niger,GCF_901709675.1_Syngnathus_acus,GCA_048301445.1_Syngnathus_typhle,GCA_044231675.1_Synchiropus_picturatus,GCA_044231665.1_Neosynchiropus_ocellatus" $DATA_ROOT/merged_codon_sites12.fas > aKRAB_NEG_3_s12.fas

        iqtree3 -s aKRAB_NEG_3_s12.fas -m "12.12+R3" -pre aKRAB_NEG_3_s12 -m "12.12+R3" --redo --nonrev-model -asr -T 32
        