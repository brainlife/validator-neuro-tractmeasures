#!/usr/bin/env python3

import os
import sys
import json
import shutil
import pandas
import numpy
import csv

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

if not os.path.exists("output"):
    os.mkdir("output")

if not os.path.exists("secondary"):
    os.mkdir("secondary")

#backward compatibility - #if csv doesn't exist where we expect, then try the old name
if not os.path.exists(config["csv"]):
    oldname = os.path.dirname(config["csv"])+"/output_FiberStats.csv"
    if os.path.exists(oldname):
        results["warnings"].append("output contains outdated file name 'output_FiberStats.csv'. App should be updated to output 'tractmeasures.csv' instead.")
        config["csv"] = oldname

#if it doesn't exist still, then no good
if not os.path.exists(config["csv"]):
    results["errors"].append("csv[%s] file does not exist" % config["csv"])
else:

    #with open(config["csv"]) as csvfile:
    #    reader = csv.reader(csvfile)
    #    header = next(reader, None)

    #    for i,col in enumerate(header):
    #        if col.endswith("_mean"):
    #            short=col[0:-5]
    #            header[i] = short
    #            results["warnings"].append("updating column name '%s' to '%s' "%(col, short))

    #    with open("output/tractmeasures.csv", "w") as outcsvfile:
    #        writer = csv.writer(outcsvfile)
    #        writer.writerow(header)
    #        for row in reader:
    #            writer.writerow(row)

    #let's just by-pass tractmeausres.csv (nothing to do)
    if not os.path.exists("output/tractmeasures.csv"):
        os.symlink("../"+config["csv"], "output/tractmeasures.csv")


print("saving proeuct.json")
with open("product.json", "w") as fp:
    json.dump(results, fp)

if len(results["errors"]) > 0:
    print("errors detected")
    print(results["errors"])

if len(results["warnings"]) > 0:
    print("warnings detected")
    print(results["warnings"])


