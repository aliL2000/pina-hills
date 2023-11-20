import pandas as pd

csv_file_path = 'data/Consultados/ConsultaSaldos (6).csv'

df = pd.DataFrame()

columns = None

with open(csv_file_path, 'r') as file:
    columns = file.readline().strip().split(';')
    columns.pop()
    row_dataframes = []
    for line in file:
        temp=line.strip().split(';')
        temp.pop()
        row_df = pd.DataFrame([temp], columns=columns)
        row_dataframes.append(row_df)

df = pd.concat(row_dataframes, ignore_index=True)
df['fechaMovimiento'] = pd.to_datetime(df['fechaMovimiento'])
df['fechaMovimiento'] = df['fechaMovimiento'].dt.strftime('%m/%d/%Y')
print(df['fechaMovimiento'])
df.to_csv("data/Consultados/Consultados6FilteredCSV.csv", index=False)