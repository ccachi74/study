import pandas as pd

data = {'1':'윤지호', '2':'윤치선', '3':'남지은'}
df = pd.DataFrame.from_dict(data, orient='index').rename(columns={0:"name"})

print(df)