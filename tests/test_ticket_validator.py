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
    pd.testing.assert_frame_equal(
        result.rejected_records,
        rejected_records,
    )


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
    assert result.rejected_records.iloc[0]["validation_errors"] == [
        "VAL-001"
    ]


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


@pytest.mark.parametrize(
    ("created_at", "expected_errors"),
    [
        (REPORT_DATETIME, []),
        (REPORT_DATETIME + pd.Timedelta(seconds=1), ["VAL-004"]),
    ],
)
def test_validate_tickets_applies_created_at_report_datetime_boundary(
    created_at: pd.Timestamp,
    expected_errors: list[str],
) -> None:
    dataframe = pd.DataFrame(
        [make_valid_ticket(created_at=created_at)]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    if expected_errors:
        assert result.valid_records.empty
        assert result.rejected_records.iloc[0]["validation_errors"] == (
            expected_errors
        )
    else:
        assert result.rejected_records.empty
        assert result.valid_records["ticket_id"].tolist() == ["TCK-001"]


@pytest.mark.parametrize(
    ("status", "closed_at"),
    [
        ("OPEN", pd.NaT),
        ("IN_PROGRESS", pd.NaT),
        ("RESOLVED", pd.Timestamp("2026-06-30 12:00")),
        ("CLOSED", pd.Timestamp("2026-06-30 12:00")),
    ],
)
def test_validate_tickets_accepts_supported_statuses(
    status: str,
    closed_at: pd.Timestamp,
) -> None:
    dataframe = pd.DataFrame(
        [make_valid_ticket(status=status, closed_at=closed_at)]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    assert result.rejected_records.empty
    assert result.valid_records["status"].tolist() == [status]


@pytest.mark.parametrize(
    "invalid_status",
    [None, "", "PENDING", "open", " OPEN "],
)
def test_validate_tickets_rejects_unsupported_status(
    invalid_status: object,
) -> None:
    dataframe = pd.DataFrame(
        [make_valid_ticket(status=invalid_status)]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    assert result.valid_records.empty
    assert result.rejected_records.iloc[0]["validation_errors"] == [
        "VAL-005"
    ]


def test_validate_tickets_accumulates_created_at_and_status_errors() -> None:
    dataframe = pd.DataFrame(
        [
            make_valid_ticket(
                created_at="not-a-date",
                status="PENDING",
            )
        ]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    assert result.valid_records.empty
    assert result.rejected_records.iloc[0]["validation_errors"] == [
        "VAL-003",
        "VAL-005",
    ]


@pytest.mark.parametrize(
    "completed_status",
    ["RESOLVED", "CLOSED"],
)
def test_validate_tickets_rejects_completed_ticket_without_closed_at(
    completed_status: str,
) -> None:
    dataframe = pd.DataFrame(
        [
            make_valid_ticket(
                status=completed_status,
                closed_at=pd.NaT,
            )
        ]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    assert result.valid_records.empty
    assert result.rejected_records["status"].tolist() == [
        completed_status
    ]
    assert result.rejected_records.iloc[0]["validation_errors"] == [
        "VAL-006"
    ]


@pytest.mark.parametrize(
    "active_status",
    ["OPEN", "IN_PROGRESS"],
)
def test_validate_tickets_rejects_active_ticket_with_closed_at(
    active_status: str,
) -> None:
    dataframe = pd.DataFrame(
        [
            make_valid_ticket(
                status=active_status,
                closed_at=pd.Timestamp("2026-06-30 12:00"),
            )
        ]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    assert result.valid_records.empty
    assert result.rejected_records["status"].tolist() == [
        active_status
    ]
    assert result.rejected_records.iloc[0]["validation_errors"] == [
        "VAL-007"
    ]


@pytest.mark.parametrize(
    ("closed_at", "expected_errors"),
    [
        (pd.Timestamp("2026-06-30 10:00"), []),
        (pd.Timestamp("2026-06-30 09:59:59"), ["VAL-008"]),
    ],
)
def test_validate_tickets_applies_closed_at_created_at_boundary(
    closed_at: pd.Timestamp,
    expected_errors: list[str],
) -> None:
    dataframe = pd.DataFrame(
        [
            make_valid_ticket(
                status="CLOSED",
                created_at=pd.Timestamp("2026-06-30 10:00"),
                closed_at=closed_at,
            )
        ]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    if expected_errors:
        assert result.valid_records.empty
        assert result.rejected_records.iloc[0]["validation_errors"] == (
            expected_errors
        )
    else:
        assert result.rejected_records.empty
        assert result.valid_records["ticket_id"].tolist() == ["TCK-001"]


@pytest.mark.parametrize(
    "invalid_closed_at",
    [
        "",
        "   ",
        "not-a-date",
        "2026-02-30",
    ],
)
def test_validate_tickets_rejects_invalid_closed_at(
    invalid_closed_at: str,
) -> None:
    dataframe = pd.DataFrame(
        [
            make_valid_ticket(
                status="CLOSED",
                closed_at=invalid_closed_at,
            )
        ]
    )

    result = validate_tickets(
        dataframe=dataframe,
        report_datetime=REPORT_DATETIME,
    )

    assert result.valid_records.empty
    assert result.rejected_records["ticket_id"].tolist() == ["TCK-001"]
    assert result.rejected_records.iloc[0]["validation_errors"] == [
        "VAL-009"
    ]