import oracledb
import csv
import os
import pandas as pd

#before running dataload.py, make sure to paste create_db.sql into your freesql and run it

#then paste 'python new_dataload.py'


# --- CONFIGURATION ---
# Path to your extracted Instant Client
LIB_DIR = r"C:\Users\Matthew\Documents\2026 sophmore\Database1\Oraclestuff (has important)\instantclient-basiclite-windows.x64-23.26.1.0.0\instantclient_23_0"

# Your Oracle Credentials
DB_USER = "MILEYFAMM_SCHEMA_D0P3M" 
DB_PASS = "IC26FEZOpHCR7367RAJPQ5JDP9!PLM" 
DB_DSN  = "db.freesql.com:1521/23ai_34ui2" 

# Initialize Client
if LIB_DIR:
    oracledb.init_oracle_client(lib_dir=LIB_DIR)
else: 
    oracledb.enable_thin_mode()

# Establish Connection
conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cursor = conn.cursor()
print("Connected to Oracle Database")

# Load Function
def load_csv_to_oracle(file_path, table_name, insert_sql):
    if not os.path.exists(file_path):
        print(f"Skipping {table_name}: {file_path} not found.")
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            all_data = [row for row in reader][:1000] # Only take the first 1000 rows to prevent freesql size issues
            
            chunk_size = 5000
            for i in range(0, len(all_data), chunk_size):
                chunk = all_data[i:i + chunk_size]
                cursor.executemany(insert_sql, chunk)
                conn.commit() 
                print(f"Uploaded {i + len(chunk)} / {len(all_data)} rows into {table_name}...")
                
            print(f"DONE: Successfully loaded {table_name}\n")
    except Exception as e:
        print(f"Error loading {table_name}: {e}")

# --- LOADING TASKS (ORDERED BY CONSTRAINTS) ---

# Load Parent Tables (No Foreign Keys)
load_csv_to_oracle('smart_home.csv', 'Smart_Home', 
                   "INSERT INTO Smart_Home (HomeID, OwnerEmail, SquareFootage, SecondaryContact) VALUES (:1, :2, :3, :4)")

load_csv_to_oracle('sensor.csv', 'Sensor', 
                   "INSERT INTO Sensor (LocalDeviceID, SensorType, InstallationDate) VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'))")

load_csv_to_oracle('weather_condition.csv', 'Weather_Condition', 
                   "INSERT INTO Weather_Condition (ConditionType, SeverityLevel) VALUES (:1, :2)")


# UPDATED: LINKING HEALTH TO HOMES (Requires Smart_Home to be loaded first)
try:
    # Read the local CSVs
    health_df_local = pd.read_csv('system_health_profile.csv')
    home_df_local = pd.read_csv('smart_home.csv')

    # Assign HomeID from the home file to the health file so they match
    health_df_local['HomeID'] = home_df_local['HomeID'].values
    
    # Save the linked version
    health_df_local.to_csv('system_health_profile_linked.csv', index=False)

    # Load into Oracle with the new 4th column (HomeID)
    load_csv_to_oracle(
        'system_health_profile_linked.csv', 
        'System_Health_Profile', 
        "INSERT INTO System_Health_Profile (ProfileID, UptimePercentage, PartitionKey, HomeID) VALUES (:1, :2, :3, :4)"
    )
except Exception as e:
    print(f"Error during linked health load: {e}")


# Load Child Table (Contains Foreign Keys)
load_csv_to_oracle('sensor_reading.csv', 'Sensor_Reading', 
                   "INSERT INTO Sensor_Reading (ReadingID, HomeID, LocalDeviceID, ConditionType, Value, Timestamp) VALUES (:1, :2, :3, :4, :5, TO_DATE(:6, 'YYYY-MM-DD HH24:MI:SS'))")

# Closing connection
cursor.close()
conn.close()
print("Oracle connection closed.")