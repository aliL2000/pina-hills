import pyodbc


def write_pina_hills_supplier_db(purchase_date,container_number,cost):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=../testDB/Cost Tracker.accdb;')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Glasswing1 WHERE [ContainerNumber] = ?", (container_number,))
    existing_row = cursor.fetchone()
    pinaHills = "PinaHills"
    if existing_row:
        # If the container number exists, update the row
        cursor.execute("UPDATE Glasswing1 SET [SupplierFruit] = ?, [Cost] = ?, [PurchaseDate] = ? WHERE [ContainerNumber] = ?", pinaHills, cost, purchase_date,container_number)
        conn.commit()
        print(f"Row updated for Container Number in Glasswing1: {container_number}")
    else:
        # If the container number does not exist, insert a new row
        cursor.execute("INSERT INTO Glasswing1 ([PurchaseDate], [ContainerNumber], [SupplierFruit], [Cost]) VALUES (?, ?, ?)",purchase_date, container_number, pinaHills, cost)
        conn.commit()
        print(f"Row inserted for Container Number in Glasswing1: {container_number}")

def write_pina_hills_cost_breakdown_db(container_number,type,quantity,unit_price,total):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=../testDB/Cost Tracker.accdb;')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Glasswing3 WHERE [ContainerNumber] = ? AND [Type] = ?", container_number,type)
    existing_row = cursor.fetchone()
    if existing_row:
        # If the container number exists, update the row
        cursor.execute("UPDATE Glasswing3 SET [UnitPrice] = ?, [Quantity] = ?, [Total] = ? WHERE [ContainerNumber] = ? AND [Type] = ?", unit_price, quantity, total,container_number,type)
        conn.commit()
        print(f"Row updated for Container Number in Glasswing3: {container_number}")
    else:
        # If the container number does not exist, insert a new row
        cursor.execute("INSERT INTO Glasswing3 ([ContainerNumber], [Type],[UnitPrice], [Quantity],[Total]) VALUES (?, ?, ?, ?, ?)",container_number, type, unit_price, quantity, total)
        conn.commit()
        print(f"Row inserted for Container Number in Glasswing3: {container_number}")

def write_pinahills_produce_inpsection_db(df_data):
    #print(df_data)
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=../testDB/Cost Tracker.accdb;')
    cursor = conn.cursor()
    pinaHillsProduceInspect = "PRODUCE  INSPECT  C.R. S.A."
    for index, row in df_data.iterrows():
        containerNumber = row['Container Number']
        qaPrice = row['QAInspection']

        # Check if the container number already exists in the database
        cursor.execute("SELECT * FROM Glasswing1 WHERE [ContainerNumber] = ?", (containerNumber,))
        existing_row = cursor.fetchone()
        if existing_row:
            # If the container number exists, update the row
            cursor.execute("UPDATE Glasswing1 SET [Supplier-QAInspection] = ?, [QAInspection] = ? WHERE [ContainerNumber] = ?",pinaHillsProduceInspect, qaPrice, containerNumber)
            conn.commit()
            print(f"Row updated for Container Number: {containerNumber}")
        else:
            # If the container number does not exist, insert a new row
            cursor.execute("INSERT INTO Glasswing1 ([ContainerNumber], [QAInspection], [Supplier-QAInspection]) VALUES (?, ?, ?)", containerNumber, qaPrice, pinaHillsProduceInspect)
            conn.commit()
            print(f"Row inserted for Container Number: {containerNumber}")

def write_shipping_db(df_data):
    #print(df_data)
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=../testDB/Cost Tracker.accdb;')
    cursor = conn.cursor()
    for index, row in df_data.iterrows():
        containerNumber = row['Container Number']
        shippingPrice = row['SealandFreight']

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

def set_customs_for_container_purchase(customs_price):
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=../testDB/Cost Tracker.accdb;')
    cursor = conn.cursor()

    cursor.execute("UPDATE Glasswing1 SET [Customs] = ? ",customs_price)
    conn.commit()
    print(f"Changed price of ALL pineapple purchases to {customs_price}")
