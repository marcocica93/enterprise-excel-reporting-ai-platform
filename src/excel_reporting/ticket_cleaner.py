"""Normalizzazione deterministica dei ticket validati."""

import pandas as pd


def clean_tickets(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Normalizza i tipi tecnici dei ticket validati."""

    cleaned_dataframe = dataframe.copy(deep=True)

    cleaned_dataframe["created_at"] = pd.to_datetime(
        cleaned_dataframe["created_at"]
    )

    cleaned_dataframe["closed_at"] = pd.to_datetime(
        cleaned_dataframe["closed_at"]
    )

    cleaned_dataframe["sla_target_hours"] = pd.to_numeric(
        cleaned_dataframe["sla_target_hours"]
    )

    return cleaned_dataframe