"""Validazione deterministica dei ticket IT."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Contiene i record validi e quelli rifiutati dalla validazione."""

    valid_records: pd.DataFrame
    rejected_records: pd.DataFrame