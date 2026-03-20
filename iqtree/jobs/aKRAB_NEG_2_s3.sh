#!/bin/bash -
        set -o nounset # Treat unset variables as an error
        WORKDIR=$RES_ROOT/aKRAB_NEG_2_s3/
        mkdir -p $WORKDIR
        cd $WORKDIR

        seqkit grep -n -p "GCA_947034865.1_Barbatula_barbatula,GCA_944039275.1_Danio_rerio,GCF_963082965.1_Carassius_carassius,GCA_936440315.1_Barbus_barbus,GCA_949357685.1_Gobio_gobio,GCA_048301585.1_Rhinogobio_nasutus,GCA_965113295.1_Leuciscus_leuciscus,GCA_963993115.1_Abramis_brama,GCA_951802725.1_Rutilus_rutilus,GCA_964197995.1_Scardinius_erythrophthalmus,GCA_949319135.1_Squalius_cephalus,GCA_949152265.1_Phoxinus_phoxinus,GCA_038024135.1_Cyprinella_venusta" $DATA_ROOT/merged_codon_sites3.fas > aKRAB_NEG_2_s3.fas

        iqtree3 -s aKRAB_NEG_2_s3.fas -m "12.12+R3" -pre aKRAB_NEG_2_s3 -m "12.12+R3" --redo --nonrev-model -asr -T 32
        