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

columns = {
    "fa": {
        "title": "FA (Fractional Anisotropy)",
        "unit": "Normalized fraction of anisotropic component"
    },
    "ad": {
        "title": "AD (Axial Diffusivity)",
        "unit": "microm^2/msec",
    },
    "md": {
        "title": "MD (Mean Diffusivity)",
        "unit": "microm^2/msec",
    },
    "rd": {
        "title": "RD (Radial Diffusivity)",
        "unit": "microm^2/msec",
    }
}

if not os.path.exists("secondary"):
    os.mkdir("secondary")
if not os.path.exists("output"):
    os.mkdir("output")

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
    if not os.path.exists("output/tractmeasures.csv"):
        os.symlink("../"+config["csv"], "output/tractmeasures.csv")

    refStructures = {}
    with open('reference/tractmeasures_references_v1.json') as reference_json:
        references = json.load(reference_json)
        #split into separate structures
        for ref in references:
            name = ref["structurename"]
            if not name in refStructures:
                refStructures[name] = []
            refStructures[name].append(ref)

    try:
        csv = pandas.read_csv(config["csv"])
        #organize into each structures
        structures = csv.groupby(by=["structureID"])
        #print(structures)
        #print(structures.groups.keys())

        #detect left/right
        #for key in structures.groups.keys():
        #groups = []
        ##for key in [ key for key, _ in structures ]:
        #for key, table in structures:
        #    name = key

        #    #detect left/rigth
        #    left=False
        #    right=False
        #    if "left" in key:
        #        left = True
        #        name = key.replace("left", "")
        #    if "right" in key:
        #        right = True
        #        name = key.replace("right", "")

        #    print(left, right, key, name) 

        #    #sorty by nodeID just in case..
        #    if "nodeID" in table:
        #        table.sort_values(by='nodeID')

        #    #convert table to plotly data
        #    #create plotly graphs for each structure
        #    data = []
        #    for measure in columns.keys():
        #        info = columns[measure]
        #        if measure in table: #subjectID       structureID  nodeID        ad        fa        md        rd

        #            #add main graph
        #            node=0
        #            trace = { "x": [], "y": [], "type": "scatter", "name": "This Data" }
        #            for row in table[measure]:
        #                trace["x"].append(node)
        #                trace["y"].append(round(row, 3))
        #                node=node+1
        #            data.append(trace)
        #            nodecount=node 

        #            #add reference data
        #            if name in refStructures:
        #                for ref in refStructures[name]:
        #                    if measure in ref:
        #                        node=0
        #                        trace = { "x": [], "y": [], "type": "scatter", "name": ref["source"]+" ref.", "yaxis2": measure}
        #                        scale = nodecount/len(ref[measure]["mean"])
        #                        for value in ref[measure]["mean"]:
        #                            trace["x"].append(node*scale)
        #                            trace["y"].append(round(value, 3)) 
        #                            node=node+1
        #                        data.append(trace)

        #    results["brainlife"].append({
        #        "type": "plotly",
        #        "data": data,
        #        "name": name+" "+measure,
        #        "layout": {
        #            "title": info["title"],
        #            "yaxis": {
        #                "title": info["unit"],
        #            }
        #            #"grid": {"rows":1, "columns": 4, "pattern": "independent"}
        #        },
        #    }) 

        #    break #debug

    except:
        results["errors"].append(str(sys.exc_info()))

print("saving proeuct.json")
with open("product.json", "w") as fp:
    json.dump(results, fp)

if len(results["errors"]) > 0:
    print("errors detected")
    print(results["errors"])

if len(results["warnings"]) > 0:
    print("warnings detected")
    print(results["warnings"])


