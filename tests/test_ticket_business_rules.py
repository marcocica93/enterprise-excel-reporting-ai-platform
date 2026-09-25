import pandas as pd
import pytest

from src.excel_reporting.ticket_business_rules import (
    ELAPSED_HOURS_COLUMN,
    LIFECYCLE_STATUS_COLUMN,
    calculate_ticket_elapsed_hours,
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

def test_calculate_ticket_elapsed_hours_uses_correct_end_datetime() -> None:
    dataframe = pd.DataFrame(
        {
            "created_at": [
                pd.Timestamp("2026-06-30 12:00"),
                pd.Timestamp("2026-06-29 08:00"),
            ],
            "closed_at": [
                pd.NaT,
                pd.Timestamp("2026-06-30 20:00"),
            ],
            "status": [
                "OPEN",
                "CLOSED",
            ],
        }
    )

    report_datetime = pd.Timestamp("2026-07-01 12:00")

    result = calculate_ticket_elapsed_hours(
        dataframe,
        report_datetime,
    )

    assert result[ELAPSED_HOURS_COLUMN].tolist() == [
        24.0,
        36.0,
    ]

def test_calculate_ticket_elapsed_hours_does_not_modify_source_dataframe() -> None:
    dataframe = pd.DataFrame(
        {
            "created_at": [
                pd.Timestamp("2026-06-30 12:00"),
            ],
            "closed_at": [
                pd.NaT,
            ],
            "status": [
                "OPEN",
            ],
        }
    )

    original_dataframe = dataframe.copy(deep=True)

    calculate_ticket_elapsed_hours(
        dataframe,
        pd.Timestamp("2026-07-01 12:00"),
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original_dataframe,
    )

def test_calculate_ticket_elapsed_hours_rejects_unsupported_status() -> None:
    dataframe = pd.DataFrame(
        {
            "created_at": [
                pd.Timestamp("2026-06-30 12:00"),
            ],
            "closed_at": [
                pd.NaT,
            ],
            "status": [
                "CANCELLED",
            ],
        }
    )

    with pytest.raises(
        ValueError,
        match="Unsupported ticket status: CANCELLED",
    ):
        calculate_ticket_elapsed_hours(
            dataframe,
            pd.Timestamp("2026-07-01 12:00"),
        )

def test_calculate_ticket_elapsed_hours_preserves_fractional_hours() -> None:
    dataframe = pd.DataFrame(
        {
            "created_at": [
                pd.Timestamp("2026-07-01 10:30"),
            ],
            "closed_at": [
                pd.NaT,
            ],
            "status": [
                "OPEN",
            ],
        }
    )

    result = calculate_ticket_elapsed_hours(
        dataframe,
        pd.Timestamp("2026-07-01 12:00"),
    )

    assert result[ELAPSED_HOURS_COLUMN].tolist() == [
        1.5,
    ]