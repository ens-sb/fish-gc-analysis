#!/usr/bin/env python

import argparse
import pickle
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Process clades TSVs.")
    parser.add_argument("--indir", help="Path to the clades pickle directory.")
    parser.add_argument("--outdir", help="Path to the output directory.")
    return parser.parse_args()


def main():
    args = parse_args()

    pickles = [f for f in os.listdir(args.indir) if f.endswith(".pk")]
    print(f"Found {len(pickles)} pickle files in {args.indir}.")
    for pk in pickles:
        with open(os.path.join(args.indir, pk), "rb") as in_f:
            clade_info = pickle.load(in_f)
            gen_jobs(clade_info, args.outdir)

def gen_jobs(clade, outdir):
    resdir="RES_ROOT"
    datadir="DATA_ROOT"
    alns = {
        "3": "merged_codon_sites3.fas",
        "12": "merged_codon_sites12.fas", 
    }

    for aln_type, aln_file in alns.items():
        pass
        sh = f"{clade['status']}_{clade['id']}_s{aln_type}.sh"
        print(f"Generating: {sh}")
        script = f"""#!/bin/bash -
        set -o nounset # Treat unset variables as an error
        WORKDIR=$RES_ROOT/{clade['status']}_{clade['id']}_s{aln_type}/
        mkdir -p $WORKDIR
        cd $WORKDIR

        seqkit grep -n -p "{','.join(clade['leaves'])}" $DATA_ROOT/{aln_file} > {clade['status']}_{clade['id']}_s{aln_type}.fas

        iqtree3 -s {clade['status']}_{clade['id']}_s{aln_type}.fas -m "12.12+R3" -pre {clade['status']}_{clade['id']}_s{aln_type} -m "12.12+R3" --redo --nonrev-model -asr -T 32
        """

        with open(os.path.join(outdir, sh), "w") as out_f:
            out_f.write(script)


if __name__ == "__main__":
    main()