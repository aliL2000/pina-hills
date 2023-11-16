import pyodbc


def write_produce_inpsection_db(df_data):
    #print(df_data)
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=../testDB/Cost Tracker.accdb;')
    cursor = conn.cursor()
    for index, row in df_data.iterrows():
        containerNumber = row['Container Number']
        qaPrice = row['QA Inspection Price']

        # Check if the container number already exists in the database
        cursor.execute("SELECT * FROM Glasswing1 WHERE [ContainerNumber] = ?", (containerNumber,))
        existing_row = cursor.fetchone()
        if existing_row:
            # If the container number exists, update the row
            cursor.execute("UPDATE Glasswing1 SET [QAInspection] = ? WHERE [ContainerNumber] = ?", qaPrice, containerNumber)
            conn.commit()
            print(f"Row updated for Container Number: {containerNumber}")
        else:
            # If the container number does not exist, insert a new row
            cursor.execute("INSERT INTO Glasswing1 ([ContainerNumber], [QAInspection]) VALUES (?, ?)", containerNumber, qaPrice)
            conn.commit()
            print(f"Row inserted for Container Number: {containerNumber}")

def write_shipping_db(df_data):
    #print(df_data)
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=../testDB/Cost Tracker.accdb;')
    cursor = conn.cursor()
    for index, row in df_data.iterrows():
        containerNumber = row['Container Number']
        shippingPrice = row['Shipping Price']

        # Check if the container number already exists in the database
        cursor.execute("SELECT * FROM Glasswing1 WHERE [ContainerNumber] = ?", (containerNumber,))
        existing_row = cursor.fetchone()
        if existing_row:
            # If the container number exists, update the row
            cursor.execute("UPDATE Glasswing1 SET [SealandFreight] = ? WHERE [ContainerNumber] = ?", shippingPrice, containerNumber)
            conn.commit()
            print(f"Row updated for Container Number: {containerNumber}")
        else:
            # If the container number does not exist, insert a new row
            cursor.execute("INSERT INTO Glasswing1 ([ContainerNumber], [SealandFreight]) VALUES (?, ?)", containerNumber, shippingPrice)
            conn.commit()
            print(f"Row inserted for Container Number: {containerNumber}")