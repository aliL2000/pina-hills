import pandas as pd

csv_file_path = 'data\Production_Analysis_To_Dos.xlsx'
df = pd.read_excel(csv_file_path,3)
dfout = pd.DataFrame(columns=["GFID","Date", "Start Date", "End Date", "Days"])
rowcount = 0

temp_data = []

for ind in df.index:
    row_data = [df['GFID'][ind],df['Date'][ind]]
    temp_data.append(row_data)
    # new_row_data = [row_data[0],row_data[1],i+5,row_data[i+2],row_data[8]]
        
        
    # dfout.loc[rowcount] = new_row_data
    # rowcount+=1 

df = pd.DataFrame(temp_data, columns=['GFID', 'Date'])

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Group the DataFrame by 'GFID', calculate min and max dates, and calculate days
result_df = df.groupby('GFID').agg(Start_date=('Date', 'min'), End_date=('Date', 'max')).reset_index()
result_df['Days'] = (result_df['End_date'] - result_df['Start_date']).dt.days +1

# Rename columns as needed
result_df.rename(columns={'GFID': 'GFID', 'Start_date': 'Start date', 'End_date': 'End date', 'Days': 'Days'}, inplace=True)

# Display the result DataFrame
print(result_df)
result_df.to_csv("../actual_schedule_output.csv", index=False)