#!/bin/bash -
set -o nounset # Treat unset variables as an error

for job in $(find ./jobs -name "*.sh"); do
	echo $job
	sbatch --time=7-00 --mem=128gb --cpus-per-task=32 --export=ALL -- "$job"
done
