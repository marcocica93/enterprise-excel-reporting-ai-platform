from pathlib import Path

import pandas as pd
import pytest

from src.excel_reporting.ticket_business_rules import (
    ELAPSED_HOURS_COLUMN,
    LIFECYCLE_STATUS_COLUMN,
    SLA_STATUS_COLUMN,
    calculate_ticket_elapsed_hours,
    classify_ticket_lifecycle,
    classify_ticket_sla,
)
from src.excel_reporting.excel_loader import load_excel_tickets
from src.excel_reporting.ticket_cleaner import clean_tickets
from src.excel_reporting.ticket_validator import validate_tickets


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


@pytest.mark.parametrize(
    ("elapsed_hours", "sla_target_hours", "expected_status"),
    [
        (23.0, 24.0, "MET"),
        (24.0, 24.0, "MET"),
        (25.0, 24.0, "BREACHED"),
        (0.0, 1.0, "MET"),
        (1.25, 1.5, "MET"),
        (1.5, 1.5, "MET"),
        (1.5 - 1 / 3600, 1.5, "MET"),
        (1.5 + 1 / 3600, 1.5, "BREACHED"),
    ],
)
def test_classify_ticket_sla_applies_inclusive_threshold(
    elapsed_hours: float,
    sla_target_hours: float,
    expected_status: str,
) -> None:
    dataframe = pd.DataFrame({
        ELAPSED_HOURS_COLUMN: [elapsed_hours],
        "sla_target_hours": [sla_target_hours],
    })

    result = classify_ticket_sla(dataframe)

    assert result[SLA_STATUS_COLUMN].tolist() == [expected_status]


def test_classify_ticket_sla_preserves_source_and_is_deterministic() -> None:
    dataframe = pd.DataFrame({
        "ticket_id": ["TCK-003", "TCK-001", "TCK-002"],
        ELAPSED_HOURS_COLUMN: [3.0, 1.0, 2.0],
        "sla_target_hours": [2.0, 2.0, 2.0],
        LIFECYCLE_STATUS_COLUMN: ["COMPLETED", "BACKLOG", "BACKLOG"],
    }, index=[8, 3, 3])
    original = dataframe.copy(deep=True)

    result = classify_ticket_sla(dataframe)
    repeated = classify_ticket_sla(dataframe)

    assert result is not dataframe
    pd.testing.assert_frame_equal(dataframe, original)
    pd.testing.assert_frame_equal(result[dataframe.columns], original)
    pd.testing.assert_frame_equal(result, repeated)
    assert result[SLA_STATUS_COLUMN].tolist() == ["BREACHED", "MET", "MET"]


def test_classify_ticket_sla_handles_empty_input() -> None:
    dataframe = pd.DataFrame({
        ELAPSED_HOURS_COLUMN: pd.Series(dtype="float64"),
        "sla_target_hours": pd.Series(dtype="float64"),
    })

    result = classify_ticket_sla(dataframe)

    assert result.empty
    assert SLA_STATUS_COLUMN in result.columns
    pd.testing.assert_frame_equal(result[dataframe.columns], dataframe)


def test_sla_pipeline_matches_approved_synthetic_baseline() -> None:
    dataset_path = (
        Path(__file__).resolve().parents[1]
        / "examples/input/synthetic_it_ticket_dataset.xlsx"
    )
    source = load_excel_tickets(dataset_path)
    original = source.copy(deep=True)
    report_datetime = pd.Timestamp("2026-07-01 12:00")
    validation = validate_tickets(source, report_datetime)
    cleaned = clean_tickets(validation.valid_records)
    lifecycle = classify_ticket_lifecycle(cleaned)
    elapsed = calculate_ticket_elapsed_hours(lifecycle, report_datetime)

    result = classify_ticket_sla(elapsed)

    assert len(source) == 30
    assert len(result) == 20
    assert len(validation.rejected_records) == 10
    assert result[SLA_STATUS_COLUMN].value_counts().to_dict() == {
        "MET": 10, "BREACHED": 10,
    }
    assert set(result["status"]) == {"OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"}
    boundary = result[ELAPSED_HOURS_COLUMN].eq(result["sla_target_hours"])
    assert boundary.any()
    assert result.loc[boundary, SLA_STATUS_COLUMN].eq("MET").all()
    assert result.index.equals(validation.valid_records.index)
    assert result.index.intersection(validation.rejected_records.index).empty
    pd.testing.assert_frame_equal(result[elapsed.columns], elapsed)
    pd.testing.assert_frame_equal(source, original)
