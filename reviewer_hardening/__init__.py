"""Independent exact oracles and certificate checkers used for reviewer hardening.

This package deliberately avoids importing the production implementation.  Its
purpose is differential validation, not an alternative fast path.
"""
from .affine_minimax import (
    AffinePiece,
    MinimaxCertificate,
    solve_exact_minimax,
    verify_minimax_certificate,
)
from .finite_domain_ve import (
    Factor,
    VETrace,
    brute_force_max,
    variable_elimination_max,
    verify_assignment,
)

__all__ = [
    "AffinePiece", "MinimaxCertificate", "solve_exact_minimax",
    "verify_minimax_certificate", "Factor", "VETrace", "brute_force_max",
    "variable_elimination_max", "verify_assignment",
]
