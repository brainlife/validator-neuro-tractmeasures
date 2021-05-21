#!/usr/bin/env python3

import os
import sys
import json
import shutil
import pandas
import numpy

from json import encoder

with open('config.json') as config_json:
    config = json.load(config_json)

if config['csv'] is None:
    print("csv is not set in config.json")
    sys.exit(1)

results = {
    "errors": [], 
    "warnings": [], 
    "brainlife": [], 
    "datatype_tags": [], 
    "tags": [], 
    "meta": { "structureIDs": [] } 
}

if not os.path.exists("secondary"):
    os.mkdir("secondary")

if not os.path.exists("output"):
    os.mkdir("output")
    os.symlink("../"+config["csv"], "output/tractmeasures.csv")

if "output_FiberStats.csv" in config["csv"]:
    results["warnings"].append("output contains outdated file name 'output_FiberStats.csv'. App should be updated to output 'tractmeasures.csv' instead.")

if not os.path.exists(config["csv"]):
    results["errors"].append("csv[%s] file does not exist" % config["csv"])
else:
    csv = pandas.read_csv(config["csv"])

with open("product.json", "w") as fp:
    json.dump(results, fp)

if len(results["errors"]) > 0:
    print("errors detected")
    print(results["errors"])

if len(results["warnings"]) > 0:
    print("warnings detected")
    print(results["warnings"])


