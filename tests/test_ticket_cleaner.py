import pandas as pd

from src.excel_reporting.ticket_cleaner import clean_tickets


def test_clean_tickets_normalizes_processing_types() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["TCK-001", "TCK-002"],
            "created_at": [
                "2026-06-30 10:00",
                "2026-06-29 09:30",
            ],
            "closed_at": [
                None,
                "2026-06-30 09:30",
            ],
            "status": [
                "OPEN",
                "CLOSED",
            ],
            "priority": [
                "P3",
                "P2",
            ],
            "assigned_team": [
                "Service Desk",
                "Infrastructure",
            ],
            "sla_target_hours": [
                "24",
                "48",
            ],
        }
    )

    result = clean_tickets(dataframe)

    assert pd.api.types.is_datetime64_any_dtype(result["created_at"])
    assert pd.api.types.is_datetime64_any_dtype(result["closed_at"])
    assert pd.api.types.is_numeric_dtype(result["sla_target_hours"])

def test_clean_tickets_does_not_modify_source_dataframe() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["TCK-001"],
            "created_at": ["2026-06-30 10:00"],
            "closed_at": [None],
            "status": ["OPEN"],
            "priority": ["P3"],
            "assigned_team": ["Service Desk"],
            "sla_target_hours": ["24"],
        }
    )

    original_dataframe = dataframe.copy(deep=True)

    clean_tickets(dataframe)

    pd.testing.assert_frame_equal(
        dataframe,
        original_dataframe,
    )

def test_clean_tickets_preserves_missing_closed_at_as_nat() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["TCK-001"],
            "created_at": ["2026-06-30 10:00"],
            "closed_at": [None],
            "status": ["OPEN"],
            "priority": ["P3"],
            "assigned_team": ["Service Desk"],
            "sla_target_hours": ["24"],
        }
    )

    result = clean_tickets(dataframe)

    assert pd.isna(result.loc[0, "closed_at"])

def test_clean_tickets_preserves_sla_target_value() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["TCK-001"],
            "created_at": ["2026-06-30 10:00"],
            "closed_at": [None],
            "status": ["OPEN"],
            "priority": ["P3"],
            "assigned_team": ["Service Desk"],
            "sla_target_hours": ["24"],
        }
    )

    result = clean_tickets(dataframe)

    assert result.loc[0, "sla_target_hours"] == 24

def test_clean_tickets_preserves_datetime_values() -> None:
    dataframe = pd.DataFrame(
        {
            "ticket_id": ["TCK-001"],
            "created_at": ["2026-06-30 10:00"],
            "closed_at": ["2026-06-30 18:30"],
            "status": ["CLOSED"],
            "priority": ["P3"],
            "assigned_team": ["Service Desk"],
            "sla_target_hours": ["24"],
        }
    )

    result = clean_tickets(dataframe)

    assert result.loc[0, "created_at"] == pd.Timestamp(
        "2026-06-30 10:00"
    )
    assert result.loc[0, "closed_at"] == pd.Timestamp(
        "2026-06-30 18:30"
    )