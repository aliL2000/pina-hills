import pandas as pd

csv_file_path = 'data\Project_Curve.xlsx'

df = pd.read_excel(csv_file_path)
print(df.columns)

#Add a new column

dfout = pd.DataFrame(columns=["Farm","Harvest Date", "Size", "# Boxes", "GFID"])
print(dfout.columns)

for idx in range(0,5):
    column_name = df.columns[idx]
    column_data = df.iloc[:, idx]  # Use iloc to select the entire column
    print(f"Column Name: {column_name}")
    print(column_data)
    print()
    # for i in range(5,11):
    #     print([df['Farm'][ind],df['HARVEST DATE'][ind],])

