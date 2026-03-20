#!/usr/bin/env python

import argparse
import pandas as pd
from collections import defaultdict
import pickle

def parse_args():
    parser = argparse.ArgumentParser(description="Process clades TSVs.")
    parser.add_argument("--pos", help="Path to the positive clades TSV file.")
    parser.add_argument("--neg", help="Path to the negative clades TSV file.")
    parser.add_argument("--un", help="Path to the unknown caldes TSV file.")
    parser.add_argument("--outdir", help="Path to the output directory.")
    return parser.parse_args()

def parse_clades(df, status):
    clades = defaultdict(dict)
    for row in df.itertuples():
        clade_id = row.clade
        clades[clade_id]["id"] = clade_id
        clades[clade_id]["status"] = status
        if "leaves" not in clades[clade_id]:
            clades[clade_id]["leaves"] = []
        clades[clade_id]["leaves"].append(row.label)

    return clades


def main():
    args = parse_args()

    pos = pd.read_csv(args.pos, sep="\t")
    neg = pd.read_csv(args.neg, sep="\t")
    un = pd.read_csv(args.un, sep="\t")

    pos_clades = parse_clades(pos, "aKRAB_POS")
    neg_clades = parse_clades(neg, "aKRAB_NEG")
    un_clades = parse_clades(un, "aKRAB_UNK")

    for clds in [pos_clades, neg_clades, un_clades]:
        for clade_id, clade_info in clds.items():
            out_path = f"{args.outdir}/{clade_info['status']}_{clade_id}.pk"
            with open(out_path, "wb") as out_f:
                pickle.dump(clade_info, out_f)


if __name__ == "__main__":
    main()