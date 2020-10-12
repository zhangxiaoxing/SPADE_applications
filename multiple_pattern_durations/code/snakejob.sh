#!/usr/bin/env bash
snakemake --jobs 240\
          --cluster "sbatch -n {cluster.n} --time {cluster.time} --mail-type=FAIL"\
          --cluster-config cluster.json\
          --jobname "{jobid}.{rulename}"\
          --keep-going\
          --rerun-incomplete\
          --use-conda

