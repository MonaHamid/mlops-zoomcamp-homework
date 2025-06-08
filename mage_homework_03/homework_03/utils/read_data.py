import requests
import pandas as pd
from typing import List
from io import BytesIO

def read(ano: int, mes_ini: int, mes_fin_excluyendo: int) -> pd.DataFrame:
    dfs: List[pd.DataFrame] = []

    for i in range(mes_ini, mes_fin_excluyendo):
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{ano}-{i:02d}.parquet"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(response.text)

        df = pd.read_parquet(BytesIO(response.content))
        dfs.append(df)

    return pd.concat(dfs)

