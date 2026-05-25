import pandas as pd

def process_excel(df: pd.DataFrame) -> pd.DataFrame:
    # Get first column (Column A)
    first_col = df.columns[0]

    # Convert all values in Column A to uppercase
    df[first_col] = df[first_col].astype(str).str.upper()

    return df