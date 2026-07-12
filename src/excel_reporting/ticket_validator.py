"""Validazione deterministica dei ticket IT."""

from dataclasses import dataclass

import pandas as pd


VALIDATION_ERRORS_COLUMN = "validation_errors"


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Contiene i record validi e quelli rifiutati dalla validazione."""

    valid_records: pd.DataFrame
    rejected_records: pd.DataFrame


def validate_tickets(
    dataframe: pd.DataFrame,
    report_datetime: pd.Timestamp,
) -> ValidationResult:
    """Separa i ticket validi da quelli che violano le regole approvate."""

    working_dataframe = dataframe.copy(deep=True)

    ticket_id_as_text = working_dataframe["ticket_id"].astype("string")
    missing_ticket_id = (
        working_dataframe["ticket_id"].isna()
        | ticket_id_as_text.str.strip().eq("")
    )

    validation_errors = [
        ["VAL-001"] if is_missing else []
        for is_missing in missing_ticket_id.fillna(False)
    ]

    working_dataframe[VALIDATION_ERRORS_COLUMN] = validation_errors

    rejected_mask = (
        working_dataframe[VALIDATION_ERRORS_COLUMN]
        .str.len()
        .gt(0)
    )

    valid_records = (
        working_dataframe.loc[~rejected_mask]
        .drop(columns=VALIDATION_ERRORS_COLUMN)
        .copy()
    )
    rejected_records = working_dataframe.loc[rejected_mask].copy()

    return ValidationResult(
        valid_records=valid_records,
        rejected_records=rejected_records,
    )