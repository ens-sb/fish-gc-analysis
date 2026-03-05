#!/usr/bin/env python

import argparse
import re


def rescue_tree(tree_file, map_file, out_tree, keep_gc=False):
    # 1. Load Mapping
    mapping = {}
    print(f"Loading mapping from {map_file}...")
    with open(map_file, "r") as f:
        next(f)  # skip header
        for line in f:
            if line.strip():
                safe, orig = line.strip().split("\t")
                mapping[safe] = orig

    # 2. Load Raw Tree
    print(f"Reading raw tree from {tree_file}...")
    with open(tree_file, "r") as f:
        tree_text = f.read()

    # 3. The Pattern Match
    # We look for SXXXX followed by a space and then the GC number.
    # We want to replace "SXXXX 12.34" with "OriginalName 12.34"
    # or just "OriginalName" if you want the number gone.

    print("Replacing IDs...")
    for safe_id, orig_id in mapping.items():
        # Match safe_id, then any space and digits/dots that follow,
        # but stop before the colon or comma or paren.
        # This regex: r'S0001(\s+[\d\.]+)?'
        pattern = re.compile(re.escape(safe_id) + r"(\s+[\d\.]+)?")

        if keep_gc:
            tree_text = pattern.sub(lambda m: orig_id + (m.group(1) if m.group(1) else ""), tree_text)
        else:
            tree_text = pattern.sub(orig_id, tree_text)

    # 4. Save
    with open(out_tree, "w") as f:
        f.write(tree_text)

    print(f"Done! Saved to {out_tree}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tree", required=True)
    parser.add_argument("-m", "--mapping", required=True)
    parser.add_argument("-o", "--output", default="final_restored.nwk")
    parser.add_argument(
        "-k", "--keep-gc", action="store_true", help="Keep the leaf GC number instead of stripping it"
    )
    args = parser.parse_args()
    rescue_tree(args.tree, args.mapping, args.output, keep_gc=args.keep_gc)
