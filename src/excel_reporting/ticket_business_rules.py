"""Applicazione deterministica delle business rule sui ticket."""

import pandas as pd

from .ticket_validator import (
    ACTIVE_STATUSES,
    COMPLETED_STATUSES,
    SUPPORTED_STATUSES,
)


LIFECYCLE_STATUS_COLUMN = "lifecycle_status"
ELAPSED_HOURS_COLUMN = "elapsed_hours"


def _raise_for_unsupported_statuses(
    dataframe: pd.DataFrame,
) -> None:
    """Interrompe l'elaborazione in presenza di stati non supportati."""

    unsupported_status_mask = ~dataframe["status"].isin(
        SUPPORTED_STATUSES
    )

    unsupported_statuses = (
        dataframe.loc[
            unsupported_status_mask,
            "status",
        ]
        .drop_duplicates()
        .tolist()
    )

    if unsupported_statuses:
        formatted_statuses = ", ".join(
            str(status) for status in unsupported_statuses
        )
        raise ValueError(
            f"Unsupported ticket status: {formatted_statuses}"
        )


def classify_ticket_lifecycle(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Classifica i ticket come backlog oppure completati."""

    classified_dataframe = dataframe.copy(deep=True)
    _raise_for_unsupported_statuses(classified_dataframe)

    classified_dataframe[LIFECYCLE_STATUS_COLUMN] = pd.NA

    classified_dataframe.loc[
        classified_dataframe["status"].isin(ACTIVE_STATUSES),
        LIFECYCLE_STATUS_COLUMN,
    ] = "BACKLOG"

    classified_dataframe.loc[
        classified_dataframe["status"].isin(COMPLETED_STATUSES),
        LIFECYCLE_STATUS_COLUMN,
    ] = "COMPLETED"

    return classified_dataframe


def calculate_ticket_elapsed_hours(
    dataframe: pd.DataFrame,
    report_datetime: pd.Timestamp,
) -> pd.DataFrame:
    """Calcola le ore trascorse dalla creazione del ticket."""

    elapsed_dataframe = dataframe.copy(deep=True)
    _raise_for_unsupported_statuses(elapsed_dataframe)

    completed_ticket_mask = elapsed_dataframe["status"].isin(
        COMPLETED_STATUSES
    )

    end_datetime = elapsed_dataframe["closed_at"].where(
        completed_ticket_mask,
        report_datetime,
    )

    elapsed_dataframe[ELAPSED_HOURS_COLUMN] = (
        end_datetime - elapsed_dataframe["created_at"]
    ).dt.total_seconds() / 3600

    return elapsed_dataframe
