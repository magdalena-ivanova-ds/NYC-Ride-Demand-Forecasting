import pandas as pd

def merge_on_timestamp(left: pd.DataFrame, right: pd.DataFrame, how: str = "left") -> pd.DataFrame:
    return left.merge(right, on="timestamp", how=how)
