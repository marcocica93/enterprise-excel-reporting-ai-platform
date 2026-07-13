"""Validazione deterministica dei ticket IT."""

from dataclasses import dataclass

import pandas as pd


VALIDATION_ERRORS_COLUMN = "validation_errors"
SUPPORTED_STATUSES = (
    "OPEN",
    "IN_PROGRESS",
    "RESOLVED",
    "CLOSED",
)


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

    duplicate_ticket_id = (
        ~missing_ticket_id.fillna(False)
        & working_dataframe["ticket_id"].duplicated(keep=False)
    )

    for position, is_duplicate in enumerate(duplicate_ticket_id):
        if is_duplicate:
            validation_errors[position].append("VAL-002")

    parsed_created_at = pd.to_datetime(
        working_dataframe["created_at"],
        errors="coerce",
    )
    invalid_created_at = parsed_created_at.isna()

    for position, is_invalid in enumerate(invalid_created_at):
        if is_invalid:
            validation_errors[position].append("VAL-003")

    created_at_after_report_datetime = (
        parsed_created_at.notna()
        & parsed_created_at.gt(report_datetime)
    )

    for position, is_after_report_datetime in enumerate(
        created_at_after_report_datetime
    ):
        if is_after_report_datetime:
            validation_errors[position].append("VAL-004")

    unsupported_status = ~working_dataframe["status"].isin(
        SUPPORTED_STATUSES
    )

    for position, is_unsupported in enumerate(unsupported_status):
        if is_unsupported:
            validation_errors[position].append("VAL-005")

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
