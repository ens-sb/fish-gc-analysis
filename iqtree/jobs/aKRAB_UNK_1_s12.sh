#!/bin/bash -
        set -o nounset # Treat unset variables as an error
        WORKDIR=$RES_ROOT/aKRAB_UNK_1_s12/
        mkdir -p $WORKDIR
        cd $WORKDIR

        seqkit grep -n -p "GCA_035084275.1_Hydrolagus_colliei,GCF_010909765.2_Amblyraja_radiata,GCA_963514005.1_Raja_brachyura,GCF_036971445.1_Narcine_bancroftii,GCF_009764475.1_Pristis_pectinata,GCF_030144855.1_Hypanus_sabinus,GCF_030028105.1_Mobula_birostris,GCF_044704955.1_Pristiophorus_japonicus,GCF_035084215.1_Heptranchias_perlo,GCF_036365525.1_Heterodontus_francisci,GCF_030684315.1_Stegostoma_tigrinum,GCF_020745735.1_Hemiscyllium_ocellatum,GCF_902713615.1_Scyliorhinus_canicula,GCA_964213995.1_Mustelus_asterias,GCF_017639515.1_Carcharodon_carcharias,GCA_964194155.1_Cetorhinus_maximus" $DATA_ROOT/merged_codon_sites12.fas > aKRAB_UNK_1_s12.fas

        iqtree3 -s aKRAB_UNK_1_s12.fas -m "12.12+R3" -pre aKRAB_UNK_1_s12 -m "12.12+R3" --redo --nonrev-model -asr -T 32
        