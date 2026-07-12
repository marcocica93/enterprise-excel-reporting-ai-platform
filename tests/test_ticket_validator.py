import pandas as pd
import pytest

from src.excel_reporting.ticket_validator import (
    ValidationResult,
    validate_tickets,
)


REPORT_DATETIME = pd.Timestamp("2026-07-01 12:00")


def make_valid_ticket(**overrides: object) -> dict[str, object]:
    """Crea un ticket valido modificabile per testare una singola regola."""

    ticket: dict[str, object] = {
        "ticket_id": "TCK-001",
        "created_at": pd.Timestamp("2026-06-30 10:00"),
        "closed_at": pd.NaT,
        "status": "OPEN",
        "priority": "P3",
        "assigned_team": "Service Desk",
        "sla_target_hours": 24,
    }
    ticket.update(overrides)
    return ticket


def test_validation_result_keeps_valid_and_rejected_records() -> None:
    valid_records = pd.DataFrame(
        {"ticket_id": ["TCK-001"]}
    )
    rejected_records = pd.DataFrame(
        {
            "ticket_id": ["TCK-002"],
            "validation_errors": [["VAL-001"]],
        }
    )

    result = ValidationResult(
        valid_records=valid_records,
        rejected_records=rejected_records,
    )

    pd.testing.assert_frame_equal(result.valid_records, valid_records)
    pd.testing.assert_frame_equal(result.rejected_records, rejected_records)


@pytest.mark.parametrize(
    "invalid_ticket_id",
    [None, "", "   "],
)
def test_validate_tickets_rejects_missing_ticket_id(
    invalid_ticket_id: object,
) -> None:
    dataframe = pd.DataFrame(
        [
            make_valid_ticket(),
            make_valid_ticket(ticket_id=invalid_ticket_id),
        ]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    assert result.valid_records["ticket_id"].tolist() == ["TCK-001"]
    assert len(result.rejected_records) == 1
    assert result.rejected_records.iloc[0]["validation_errors"] == ["VAL-001"]
def test_validate_tickets_does_not_modify_source_dataframe() -> None:


    dataframe = pd.DataFrame(
        [
            make_valid_ticket(),
            make_valid_ticket(ticket_id=None),
        ]
    )
    original_dataframe = dataframe.copy(deep=True)

    validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original_dataframe,
    )
def test_validate_tickets_rejects_all_duplicate_ticket_ids() -> None:
    dataframe = pd.DataFrame(
        [
            make_valid_ticket(ticket_id="TCK-DUP"),
            make_valid_ticket(ticket_id="TCK-DUP"),
            make_valid_ticket(ticket_id="TCK-UNIQUE"),
        ]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    assert result.valid_records["ticket_id"].tolist() == ["TCK-UNIQUE"]
    assert result.rejected_records["ticket_id"].tolist() == [
        "TCK-DUP",
        "TCK-DUP",
    ]
    assert result.rejected_records["validation_errors"].tolist() == [
        ["VAL-002"],
        ["VAL-002"],
    ]


@pytest.mark.parametrize(
    "invalid_created_at",
    [None, "", "not-a-date"],
)
def test_validate_tickets_rejects_invalid_created_at(
    invalid_created_at: object,
) -> None:
    dataframe = pd.DataFrame(
        [
            make_valid_ticket(ticket_id="TCK-001"),
            make_valid_ticket(
                ticket_id="TCK-002",
                created_at=invalid_created_at,
            ),
        ]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    assert result.valid_records["ticket_id"].tolist() == ["TCK-001"]
    assert result.rejected_records["ticket_id"].tolist() == ["TCK-002"]
    assert result.rejected_records.iloc[0]["validation_errors"] == [
        "VAL-003"
    ]