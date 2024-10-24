"""
CALCULATE ADDITIONAL METRICS (SCORES)
"""

from typing import List, Dict, Any

from collections import defaultdict, OrderedDict

from rdabase import Assignment
from .minority import (
    InferredVotes,
    count_defined_opportunity_districts,
    aggregate_votes_by_district,
)


def add_scores(
    prev_scores: OrderedDict[str, Any],
    prev_by_district: List[Dict[str, float]],
    ###########################################################################
    assignments: List[Assignment],
    data: Dict[str, Dict[str, int | str]],
    shapes: Dict[str, Any],
    graph: Dict[str, List[str]],
    metadata: Dict[str, Any],
    more_data: Dict[str, Any] = dict(),  # Optional
    ###########################################################################
) -> Dict[str, float | int]:
    """Count defined minority opportunity districts (MOD)."""

    N: int = int(metadata["D"])

    aggregated_votes: Dict[int | str, InferredVotes] = aggregate_votes_by_district(
        assignments, more_data, N
    )
    votes_by_district: List[InferredVotes] = list(aggregated_votes.values())[1:]

    oppty_district_count: int
    mods: List[int | str]
    oppty_district_count, mods = count_defined_opportunity_districts(votes_by_district)

    mod_scores: Dict[str, float | int] = dict()
    mod_scores["mod_districts"] = oppty_district_count
    mod_averages: Dict[str, float] = defaultdict(float)
    for d in mods:
        i: int = int(d) - 1
        mod_averages["mod_reock"] += prev_by_district[i]["reock"]
        mod_averages["mod_polsby_popper"] += prev_by_district[i]["polsby"]
        mod_averages["mod_spanning_tree_score"] += prev_by_district[i][
            "spanning_tree_score"
        ]
        mod_averages["mod_district_splitting"] += prev_by_district[i][
            "district_splitting"
        ]
    mod_averages = {k: v / oppty_district_count for k, v in mod_averages.items()}
    mod_scores.update(mod_averages)

    return mod_scores


### END ###
