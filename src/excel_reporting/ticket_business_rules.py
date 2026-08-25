"""Applicazione deterministica delle business rule sui ticket."""

import pandas as pd

from .ticket_validator import (
    ACTIVE_STATUSES,
    COMPLETED_STATUSES,
    SUPPORTED_STATUSES,
)


LIFECYCLE_STATUS_COLUMN = "lifecycle_status"


def classify_ticket_lifecycle(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Classifica i ticket come backlog oppure completati."""

    classified_dataframe = dataframe.copy(deep=True)

    unsupported_status_mask = ~classified_dataframe["status"].isin(
        SUPPORTED_STATUSES
    )

    unsupported_statuses = (
        classified_dataframe.loc[
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
