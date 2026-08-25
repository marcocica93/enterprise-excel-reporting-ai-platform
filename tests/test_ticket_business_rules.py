import pandas as pd
import pytest

from src.excel_reporting.ticket_business_rules import (
    LIFECYCLE_STATUS_COLUMN,
    classify_ticket_lifecycle,
)


def test_classify_ticket_lifecycle_groups_supported_statuses() -> None:
    dataframe = pd.DataFrame(
        {
            "status": [
                "OPEN",
                "IN_PROGRESS",
                "RESOLVED",
                "CLOSED",
            ]
        }
    )

    result = classify_ticket_lifecycle(dataframe)

    assert result[LIFECYCLE_STATUS_COLUMN].tolist() == [
        "BACKLOG",
        "BACKLOG",
        "COMPLETED",
        "COMPLETED",
    ]

def test_classify_ticket_lifecycle_rejects_unsupported_status() -> None:
    dataframe = pd.DataFrame(
        {
            "status": [
                "OPEN",
                "PENDING",
            ]
        }
    )

    with pytest.raises(
        ValueError,
        match="Unsupported ticket status: PENDING",
    ):
        classify_ticket_lifecycle(dataframe)

def test_classify_ticket_lifecycle_does_not_modify_source_dataframe() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["TCK-001"],
            "status": ["OPEN"],
        }
    )

    original_dataframe = dataframe.copy(deep=True)

    classify_ticket_lifecycle(dataframe)

    pd.testing.assert_frame_equal(
        dataframe,
        original_dataframe,
    )