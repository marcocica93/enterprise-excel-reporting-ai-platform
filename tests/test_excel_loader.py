import pytest
import pandas as pd

from pathlib import Path

from src.excel_reporting.excel_loader import (
    REQUIRED_COLUMNS,
    load_excel_tickets,
)


DATASET_PATH = Path("data/input/synthetic_it_ticket_dataset.xlsx")


def test_load_excel_tickets_returns_expected_dataframe() -> None:
    dataframe = load_excel_tickets(DATASET_PATH)

    assert dataframe.shape == (30, 7)
    assert REQUIRED_COLUMNS.issubset(dataframe.columns)
def test_load_excel_tickets_raises_error_when_file_is_missing() -> None:


    with pytest.raises(FileNotFoundError, match="File Excel non trovato"):
        load_excel_tickets("file_inesistente.xlsx")


def test_load_excel_tickets_raises_error_when_sheet_is_missing() -> None:
    with pytest.raises(ValueError, match="Foglio 'Foglio_Inesistente' non trovato"):
        load_excel_tickets(
            DATASET_PATH,
            sheet_name="Foglio_Inesistente",
        )


def test_load_excel_tickets_raises_error_when_columns_are_missing(
    tmp_path: Path,
) -> None:
    invalid_file = tmp_path / "dataset_incompleto.xlsx"

    pd.DataFrame(
        {"ticket_id": ["TCK-001"]}
    ).to_excel(
        invalid_file,
        sheet_name="Tickets",
        index=False,
    )

    with pytest.raises(ValueError, match="Colonne obbligatorie mancanti"):
        load_excel_tickets(invalid_file)