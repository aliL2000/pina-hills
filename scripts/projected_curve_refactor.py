import pandas as pd

csv_file_path = 'data\Project_Curve.xlsx'
df = pd.read_excel(csv_file_path)
dfout = pd.DataFrame(columns=["Farm","Harvest Date", "Size", "# Boxes", "GFID"])
rowcount = 0

for ind in df.index:
    row_data = [df['Farm'][ind],df['HARVEST DATE'][ind],df['Box5'][ind],df['Box6'][ind],df['Box7'][ind],df['Box8'][ind],df['Box9'][ind],df['Box10'][ind],df['GFID'][ind]]
    for i in range(6):
        new_row_data = [row_data[0],row_data[1],i+5,row_data[i+2],row_data[8]]
        dfout.loc[rowcount] = new_row_data
        rowcount+=1 

dfout.to_csv("../projected_curve_output.csv", index=False)