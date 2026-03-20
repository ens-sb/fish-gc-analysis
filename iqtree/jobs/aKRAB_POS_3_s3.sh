#!/bin/bash -
        set -o nounset # Treat unset variables as an error
        WORKDIR=$RES_ROOT/aKRAB_POS_3_s3/
        mkdir -p $WORKDIR
        cd $WORKDIR

        seqkit grep -n -p "GCA_963989245.1_Nansenia_antarctica,GCA_951799395.1_Argentina_silus,GCF_011004845.1_Esox_lucius,GCA_964263955.1_Coregonus_lavaretus,GCA_901001165.2_Salmo_trutta,GCA_036784965.1_Salvelinus_alpinus,GCA_949987555.1_Borostomias_antarcticus,GCF_963692335.1_Osmerus_eperlanus,GCA_038355195.1_Osmerus_mordax,GCA_017639675.1_Aplochiton_taeniatus,GCA_963971535.1_Notolepis_coatsi,GCA_963921795.1_Nannobrachium_achirus,GCA_951216825.1_Electrona_antarctica,GCA_964188405.1_Protomyctophum_parallelum,GCA_046255685.1_Amblyopsis_spelaea,GCA_964030765.1_Micromesistius_poutassou,GCF_902167405.1_Gadus_morhua,GCA_048537225.1_Polymixia_cf._hollisterae,GCA_047511565.1_Polymixia_lowei" $DATA_ROOT/merged_codon_sites3.fas > aKRAB_POS_3_s3.fas

        iqtree3 -s aKRAB_POS_3_s3.fas -m "12.12+R3" -pre aKRAB_POS_3_s3 -m "12.12+R3" --redo --nonrev-model -asr -T 32
        