#!/usr/bin/env python3

"""
COUNT MINORITY OPPORTUNITY DISTRICTS & RELATED SCORES FOR AN ENSEMBLE OF MAPS

For example:

$ scripts/debug.py \
--state NC \
--plans ../../iCloud/fileout/tradeoffs/NC/ensembles/NC20C_plans.json \
--data ../rdabase/data/NC/NC_2020_data.csv \
--moredata ../tradeoffs/EI_estimates/NC_2020_est_votes.csv \
--shapes ../rdabase/data/NC/NC_2020_shapes_simplified.json \
--graph ../rdabase/data/NC/NC_2020_graph.json \
--scores temp/NC20C_score_WITH_MOD.csv \
--no-debuG

For documentation, type:

$ scripts/debug.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Any, List, Dict, Callable, OrderedDict

import random

import warnings

warnings.warn = lambda *args, **kwargs: None

from rdabase import (
    require_args,
    read_json,
    write_csv,
    write_json,
    load_data,
    load_shapes,
    load_graph,
    load_metadata,
    read_csv,
    Assignment,
)
from rdaei import load_EI_votes, add_scores


def main() -> None:
    args: argparse.Namespace = parse_args()

    data: Dict[str, Dict[str, int | str]] = load_data(args.data)
    shapes: Dict[str, Any] = load_shapes(args.shapes)
    graph: Dict[str, List[str]] = load_graph(args.graph)
    metadata: Dict[str, Any] = load_metadata(args.state, args.data, args.plantype)

    more_data: Dict[str, Any] = load_EI_votes(args.moredata)
    more_scores_fn: Callable[..., Dict[str, float | int]] = lambda *args, **kwargs: {}

    sample_plan: List[Dict[str, Any]] = read_csv(args.plan, [str, int])
    assert "GEOID" in sample_plan[0] or "GEOID20" in sample_plan[0]
    assert "DISTRICT" in sample_plan[0] or "District" in sample_plan[0]
    geoid_field: str = "GEOID20" if "GEOID20" in sample_plan[0] else "GEOID"
    district_field: str = "District" if "District" in sample_plan[0] else "DISTRICT"
    assignments: List[Assignment] = [
        Assignment(geoid=row[geoid_field], district=row[district_field])
        for row in sample_plan
    ]

    N: int = int(metadata["D"])
    by_district: List[Dict[str, float]] = [
        {
            "reock": random.random(),
            "polsby": random.random(),
            "spanning_tree_score": random.randint(500, 1000),
            "district_splitting": random.random() + 1.0,
        }
        for _ in range(N)
    ]

    more_scores: Dict[str, float | int] = add_scores(
        OrderedDict(),
        [],
        assignments,
        data,
        shapes,
        graph,
        metadata,
        more_data=more_data,
    )

    print(more_scores)

    pass


def parse_args():
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Generate a collection of random maps."
    )

    parser.add_argument(
        "--state",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "--plantype",
        type=str,
        default="congress",
        help="The type of districts (congress, upper, lower)",
    )
    parser.add_argument(
        "--plan",
        type=str,
        help="The sample plan to score",
    )
    parser.add_argument(
        "--data",
        type=str,
        help="Data file",
    )
    parser.add_argument(
        "--moredata",
        type=str,
        help="Path to file with more data for more scores",
    )
    parser.add_argument(
        "--shapes",
        type=str,
        help="Shapes abstract file",
    )
    parser.add_argument(
        "--graph",
        type=str,
        help="Graph file",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    # Enable debug/explicit mode
    parser.add_argument("--debug", default=True, action="store_true", help="Debug mode")
    parser.add_argument(
        "--no-debug", dest="debug", action="store_false", help="Explicit mode"
    )

    args: Namespace = parser.parse_args()

    # Default values for args in debug mode
    debug_defaults: Dict[str, Any] = {
        "state": "NC",
        "plantype": "congress",
        "plan": "testdata/NC20C_root_map.csv",
        "data": "../rdabase/data/NC/NC_2020_data.csv",
        "shapes": "../rdabase/data/NC/NC_2020_shapes_simplified.json",
        "graph": "../rdabase/data/NC/NC_2020_graph.json",
        "moredata": "data/NC_2020_est_votes.csv",
        "verbose": True,
    }
    args = require_args(args, args.debug, debug_defaults)

    return args


if __name__ == "__main__":
    main()

### END ###
