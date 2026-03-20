#!/bin/bash -
set -o nounset # Treat unset variables as an error

./scripts/gen_jobs.py --indir clades/processed --outdir jobs
