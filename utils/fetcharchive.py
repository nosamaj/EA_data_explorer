import datetime
import pandas as pd
import pandas.io.common


start = datetime.datetime.strptime("01-0-2021", "%d-%m-%Y")
date_generated = pd.date_range(start, periods=365)
print(date_generated.strftime("%Y-%m-%d"))

datemask = ("%Y-%m-%d")

df_main = pd.DataFrame()

try:
    for d in date_generated:
        try:
            date = d.strftime("%Y-%m-%d")
            print(date)
            df = pd.read_csv(f"https://environment.data.gov.uk/flood-monitoring/archive/readings-{date}.csv")
            df.to_csv(f"./EAdata/{date}")
        except Exception:
            pass
        #df.to_csv(f"./EAdata/{date}")
except Exception:
    print('failed')