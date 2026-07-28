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

SUPPORTED_PRIORITIES = (
    "P1",
    "P2",
    "P3",
    "P4",
)

ACTIVE_STATUSES = (
    "OPEN",
    "IN_PROGRESS",
)

COMPLETED_STATUSES = (
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

    completed_without_closed_at = (
        working_dataframe["status"].isin(COMPLETED_STATUSES)
        & working_dataframe["closed_at"].isna()
    )

    for position, is_missing_closed_at in enumerate(
        completed_without_closed_at
    ):
        if is_missing_closed_at:
            validation_errors[position].append("VAL-006")

    active_with_closed_at = (
        working_dataframe["status"].isin(ACTIVE_STATUSES)
        & working_dataframe["closed_at"].notna()
    )

    for position, has_closed_at in enumerate(active_with_closed_at):
        if has_closed_at:
            validation_errors[position].append("VAL-007")

    parsed_closed_at = pd.to_datetime(
        working_dataframe["closed_at"],
        errors="coerce",
    )

    invalid_closed_at = (
        working_dataframe["closed_at"].notna()
        & parsed_closed_at.isna()
    )

    for position, is_invalid in enumerate(invalid_closed_at):
        if is_invalid:
            validation_errors[position].append("VAL-009")

    closed_at_before_created_at = (
        parsed_closed_at.notna()
        & parsed_created_at.notna()
        & parsed_closed_at.lt(parsed_created_at)
    )

    for position, is_before_created_at in enumerate(
        closed_at_before_created_at
    ):
        if is_before_created_at:
            validation_errors[position].append("VAL-008")

    unsupported_priority = ~working_dataframe["priority"].isin(
        SUPPORTED_PRIORITIES
    )

    for position, is_unsupported in enumerate(unsupported_priority):
        if is_unsupported:
            validation_errors[position].append("VAL-010")

    assigned_team_as_text = working_dataframe["assigned_team"].astype(
        "string"
    )
    missing_assigned_team = (
        working_dataframe["assigned_team"].isna()
        | assigned_team_as_text.str.strip().eq("")
    )

    for position, is_missing in enumerate(
        missing_assigned_team.fillna(False)
    ):
        if is_missing:
            validation_errors[position].append("VAL-011")

    sla_target_hours_as_text = working_dataframe["sla_target_hours"].astype(
        "string"
    )
    missing_sla_target_hours = (
        working_dataframe["sla_target_hours"].isna()
        | sla_target_hours_as_text.str.strip().eq("")
    )

    for position, is_missing in enumerate(
        missing_sla_target_hours.fillna(False)
    ):
        if is_missing:
            validation_errors[position].append("VAL-012")

    numeric_sla_target_hours = pd.to_numeric(
        working_dataframe["sla_target_hours"],
        errors="coerce",
    )
    non_numeric_sla_target_hours = (
        numeric_sla_target_hours.isna()
        & ~missing_sla_target_hours.fillna(False)
    )

    for position, is_non_numeric in enumerate(
        non_numeric_sla_target_hours
    ):
        if is_non_numeric:
            validation_errors[position].append("VAL-012")

    non_positive_sla_target_hours = (
        numeric_sla_target_hours.notna()
        & numeric_sla_target_hours.le(0)
    )

    for position, is_non_positive in enumerate(
        non_positive_sla_target_hours
    ):
        if is_non_positive:
            validation_errors[position].append("VAL-012")

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
