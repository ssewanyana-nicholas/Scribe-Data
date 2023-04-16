"""
Format Verbs
------------

Formats the verbs queried from Wikidata using query_verbs.sparql.
"""

# pylint: disable=invalid-name

import collections
import json
import os
import sys

from scribe_data.load.update_utils import get_path_from_et_dir

LANGUAGE = "German"
PATH_TO_SCRIBE_ORG = os.path.dirname(sys.path[0]).split("Scribe-Data")[0]
PATH_TO_SCRIBE_DATA_SRC = f"{PATH_TO_SCRIBE_ORG}Scribe-Data/src"
sys.path.insert(0, PATH_TO_SCRIBE_DATA_SRC)

file_path = sys.argv[0]

update_data_in_use = False  # check if update_data.py is being used
if f"{LANGUAGE}/verbs/" not in file_path:
    with open("verbs_queried.json", encoding="utf-8") as f:
        verbs_list = json.load(f)
else:
    update_data_in_use = True
    with open(f"./{LANGUAGE}/verbs/verbs_queried.json", encoding="utf-8") as f:
        verbs_list = json.load(f)

verbs_formatted = {}

all_keys = [
    "pastParticiple",
    "auxiliaryVerb",
    "presFPS",
    "presSPS",
    "presTPS",
    "presFPP",
    "presSPP",
    "presTPP",
    "pretFPS",
    "pretSPS",
    "pretTPS",
    "pretFPP",
    "pretSPP",
    "pretTPP",
    "perfFPS",
    "perfSPS",
    "perfTPS",
    "perfFPP",
    "perfSPP",
    "perfTPP",
]


def assign_past_participle(verb, tense):
    """
    Assigns the past participle after the auxiliary verb or by itself.
    """
    if verbs_formatted[verb["infinitive"]][tense] not in ["", verb["pastParticiple"]]:
        verbs_formatted[verb["infinitive"]][tense] += " " + verb["pastParticiple"]
    else:
        verbs_formatted[verb["infinitive"]][tense] = verb["pastParticiple"]


for verb_vals in verbs_list:
    if (
        "infinitive" in verb_vals.keys()
        and verb_vals["infinitive"] not in verbs_formatted
    ):
        non_infinitive_conjugations = {
            k: v for k, v in verb_vals.items() if k != "infinitive"
        }
        verbs_formatted[verb_vals["infinitive"]] = non_infinitive_conjugations

        for k in all_keys:
            if k not in verbs_formatted[verb_vals["infinitive"]].keys():
                verbs_formatted[verb_vals["infinitive"]][k] = ""

        if "auxiliaryVerb" in verb_vals.keys():
            # Sein
            if verb_vals["auxiliaryVerb"] == "L1761":
                verbs_formatted[verb_vals["infinitive"]]["auxiliaryVerb"] = "sein"

                verbs_formatted[verb_vals["infinitive"]]["perfFPS"] += "bin"
                verbs_formatted[verb_vals["infinitive"]]["perfSPS"] += "bist"
                verbs_formatted[verb_vals["infinitive"]]["perfTPS"] += "ist"
                verbs_formatted[verb_vals["infinitive"]]["perfFPP"] += "sind"
                verbs_formatted[verb_vals["infinitive"]]["perfSPP"] += "seid"
                verbs_formatted[verb_vals["infinitive"]]["perfTPP"] += "sind"

            # Haben
            elif verb_vals["auxiliaryVerb"] == "L4179":
                verbs_formatted[verb_vals["infinitive"]]["auxiliaryVerb"] = "haben"

                verbs_formatted[verb_vals["infinitive"]]["perfFPS"] += "habe"
                verbs_formatted[verb_vals["infinitive"]]["perfSPS"] += "hast"
                verbs_formatted[verb_vals["infinitive"]]["perfTPS"] += "hat"
                verbs_formatted[verb_vals["infinitive"]]["perfFPP"] += "haben"
                verbs_formatted[verb_vals["infinitive"]]["perfSPP"] += "habt"
                verbs_formatted[verb_vals["infinitive"]]["perfTPP"] += "haben"

    # The verb has two entries and thus has forms with both sein and haben.
    elif (
        "auxiliaryVerb" in verb_vals.keys()
        and verbs_formatted[verb_vals["infinitive"]]["auxiliaryVerb"]
        != verb_vals["auxiliaryVerb"]
    ):
        verbs_formatted[verb_vals["infinitive"]]["auxiliaryVerb"] = "sein/haben"

        verbs_formatted[verb_vals["infinitive"]]["perfFPS"] = "bin/habe"
        verbs_formatted[verb_vals["infinitive"]]["perfSPS"] = "bist/hast"
        verbs_formatted[verb_vals["infinitive"]]["perfTPS"] = "ist/hat"
        verbs_formatted[verb_vals["infinitive"]]["perfFPP"] = "sind/haben"
        verbs_formatted[verb_vals["infinitive"]]["perfSPP"] = "seid/habt"
        verbs_formatted[verb_vals["infinitive"]]["perfTPP"] = "sind/haben"

    if "pastParticiple" in verb_vals.keys():
        assign_past_participle(verb=verb_vals, tense="perfFPS")
        assign_past_participle(verb=verb_vals, tense="perfSPS")
        assign_past_participle(verb=verb_vals, tense="perfTPS")
        assign_past_participle(verb=verb_vals, tense="perfFPP")
        assign_past_participle(verb=verb_vals, tense="perfSPP")
        assign_past_participle(verb=verb_vals, tense="perfTPP")

verbs_formatted = collections.OrderedDict(sorted(verbs_formatted.items()))

org_path = get_path_from_et_dir()
export_path = "../formatted_data/verbs.json"
if update_data_in_use:
    export_path = f"{org_path}/Scribe-Data/src/scribe_data/extract_transform/{LANGUAGE}/formatted_data/verbs.json"

with open(export_path, "w", encoding="utf-8",) as file:
    json.dump(verbs_formatted, file, ensure_ascii=False, indent=0)

print(f"Wrote file verbs.json with {len(verbs_formatted)} verbs.")
