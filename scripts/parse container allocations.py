import pandas as pd

csv_file_path = 'data\Container_Inventory-Allocations_Glasswing_Produce_5_version_1.xlsm'
df = pd.read_excel(csv_file_path)
print(df.columns)

rowcount = 0
dfout = pd.DataFrame(columns=["Week","Container", "BOL", "Ship", "Arrival Data","Total Cases", "Size", "Customer Name", "Customer PO", "Glasswing PO", "Total Cases","Date Shipped", "Balance of Cases", "Comment"])

for ind in df.index:
    #print(ind)
    if not pd.isna(df['Container'][ind]):  # Check if the value is not NaN
        containernumber = df['Container'][ind]  # Update containernumber with the valid value
    else:
        df.at[ind, 'Container'] = containernumber 

    if not pd.isna(df['Week'][ind]):  # Check if the value is not NaN
        weekNumber = df['Week'][ind]  # Update containernumber with the valid value
    else:
        df.at[ind, 'Week'] = weekNumber
    
    if not pd.isna(df['BOL'][ind]):  # Check if the value is not NaN
        bol = df['BOL'][ind]  # Update containernumber with the valid value
    else:
        df.at[ind, 'BOL'] = bol 

    if not pd.isna(df['Ship'][ind]):  # Check if the value is not NaN
        ship = df['Ship'][ind]  # Update containernumber with the valid value
    else:
        df.at[ind, 'Ship'] = ship 
    if not pd.isna(df['Arrival Date '][ind]):  # Check if the value is not NaN
        aDate = df['Arrival Date '][ind]  # Update containernumber with the valid value
    else:
        df.at[ind, 'Arrival Date '] = aDate 
    #print(containernumber)
    #print(weekNumber)
    row_data = [weekNumber,containernumber,bol,ship,aDate,df['Total Cases '][ind],df['Size'][ind],df['Customer Name'][ind],df['Customer PO'][ind],df['Glasswing PO'][ind],df['Total Cases'][ind],df['Date Shipped'][ind],df['Balance of Cases '][ind],df['Comment'][ind]]
    dfout.loc[rowcount] = row_data
    rowcount+=1 
    #Delete rows that do nothave size and do not say nothing shipped
    # if df['Container'][ind] != "Nothing Shipped":
    #     print(ind,df['Container'][ind])
    # else:
    #     print(ind,df['Container'][ind])
dfout.to_csv("../containerAllocationsFiltered.csv", index=False)
print("completed")