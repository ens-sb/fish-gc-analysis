#!/bin/bash -
        set -o nounset # Treat unset variables as an error
        WORKDIR=$RES_ROOT/aKRAB_NEG_4_s12/
        mkdir -p $WORKDIR
        cd $WORKDIR

        seqkit grep -n -p "GCF_900634625.1_Parambassis_ranga,GCA_963514085.1_Chelon_labrosus,GCA_049082185.1_Cristiceps_australis,GCF_902148845.1_Salarias_fasciatus,GCA_963422515.1_Blennius_ocellaris,GCA_963383615.1_Lipophrys_pholis,GCA_020510985.1_Pholidichthys_leucotaenia,GCF_007364275.1_Archocentrus_centrarchus,GCA_963969265.1_Rhamphochromis_sp._chilingali,GCA_965226115.1_Aulonocara_stuartgranti,GCA_964374335.1_Astatotilapia_calliptera,GCA_014839995.1_Xenentodon_cancila,GCA_037039145.1_Fundulus_diaphanus,GCF_021462225.1_Girardinichthys_multiradiatus,GCA_014839685.1_Anableps_anableps,GCF_017639745.1_Melanotaenia_boesemani,GCA_933228915.1_Telmatherina_bonti,GCA_048628825.1_Menidia_menidia,GCA_027942865.1_Odontesthes_bonariensis" $DATA_ROOT/merged_codon_sites12.fas > aKRAB_NEG_4_s12.fas

        iqtree3 -s aKRAB_NEG_4_s12.fas -m "12.12+R3" -pre aKRAB_NEG_4_s12 -m "12.12+R3" --redo --nonrev-model -asr -T 32
        