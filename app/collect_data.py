import pandas as pd
from pathvalidate import sanitize_filename
from tqdm import tqdm

df = pd.read_parquet("a.parquet")

df = df.sample(n=100, random_state=0)

for index, row in tqdm(df.iterrows()):

    filename = "data/" + sanitize_filename(str(row['id']) + "_" + row['title']).replace(" ", "_") + ".txt"

    with open(filename, "w") as f:
        f.write(row['text'])
    
    