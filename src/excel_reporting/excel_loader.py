"""Caricamento controllato dei dataset Excel dei ticket IT."""

from pathlib import Path

import pandas as pd


DEFAULT_SHEET_NAME = "Tickets"

REQUIRED_COLUMNS = {
    "ticket_id",
    "created_at",
    "closed_at",
    "status",
    "priority",
    "assigned_team",
    "sla_target_hours",
}
def load_excel_tickets(
    file_path: str | Path,
    sheet_name: str = DEFAULT_SHEET_NAME,
) -> pd.DataFrame:
    """Carica un dataset Excel di ticket IT."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File Excel non trovato: {path}")

    workbook = pd.ExcelFile(path)

    if sheet_name not in workbook.sheet_names:
        raise ValueError(
            f"Foglio '{sheet_name}' non trovato. "
            f"Fogli disponibili: {workbook.sheet_names}"
        )
    dataframe = pd.read_excel(workbook, sheet_name=sheet_name)

    missing_columns = REQUIRED_COLUMNS.difference(dataframe.columns)

    if missing_columns:
        missing_columns_text = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"Colonne obbligatorie mancanti: {missing_columns_text}"
        )

    return dataframe