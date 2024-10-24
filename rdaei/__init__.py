# rdaei/__init__.py

from .analyze import add_scores
from .minority import (
    InferredVotes,
    is_same_candidate_preferred,
    is_defined_opportunity_district,
    count_defined_opportunity_districts,
    load_EI_votes,
    aggregate_votes_by_district,
)

name: str = "rdaei"
