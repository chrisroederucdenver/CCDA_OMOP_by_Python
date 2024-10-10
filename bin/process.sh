#!/usr/bin/env bash

# install packages into mamba environment
# 1. shell command from Matt, must be run at start of workspace
# mamba install -y -q lxml
# mamba install -y -q duckdb
# mamba install -y -q pandas 


# 2 python repl command from "packages" here in Jupyter (doesn't work)
# !maestro env pip install lxml==5.2.2
# !maestro env pip install duckdb

mkdir logs 2> /dev/null
mkdir output 2> /dev/null

rm -f logs/*
rm -f output/*
python3 -m prototype_2.layer_datasets -d resources # ../CCDA-data/resources
python3 -m omop.setup_omop

