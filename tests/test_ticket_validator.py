import pandas as pd

from src.excel_reporting.ticket_validator import ValidationResult


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