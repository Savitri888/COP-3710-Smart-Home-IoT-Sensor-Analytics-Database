import pandas as pd
import numpy as np
import glob
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

all_home_files = glob.glob("home*.csv")
li = []

for filename in all_home_files:
    df_temp = pd.read_csv(filename)
    df_temp['HomeID'] = os.path.splitext(filename)[0]
    li.append(df_temp)

master_df = pd.concat(li, axis=0, ignore_index=True)

# ----------------------------------------------------------------------
# 1. smart home

smart_home_df = master_df[["HomeID"]].drop_duplicates().copy()
needed = 105 - len(smart_home_df)
if needed > 0:
    synth = pd.DataFrame({"HomeID": [f"H{1000 + i}" for i in range(len(smart_home_df), 105)]})
    smart_home_df = pd.concat([smart_home_df, synth], ignore_index=True)

smart_home_df["OwnerEmail"] = "resident@home.com"
smart_home_df["SquareFootage"] = 2200
smart_home_df["SecondaryContact"] = [f"contact{i}@email.com" if i % 3 == 0 else "555-0199" for i in range(105)]

# --------------------------------------------------------------------
# 2. sensor

sensor_df = pd.DataFrame({
    "LocalDeviceID": [f"S{str(i).zfill(2)}" for i in range(1, 106)],
    "SensorType": ["Temperature", "Humidity", "Gas", "Wind", "Pressure"] * 21,
    "InstallationDate": "2024-01-01"
})

# --------------------------------------------------------------------------
# 3. system health profile

health_df = pd.DataFrame({
    "ProfileID": [f"HP{str(i).zfill(3)}" for i in range(11, 116)],
    "UptimePercentage": 99.1,
    "PartitionKey": np.random.choice(["N", "S", "E", "W"], 105) 
})

# ---------------------------------------------------------------------------------------
# 4. weather condition

weather_df = pd.DataFrame({
    "ConditionType": ["Sunny", "Cloudy", "Windy", "Rain", "Thunderstorm"],
    "SeverityLevel": [1, 2, 3, 4, 5]
})

# -----------------------------------------------------------------------------------
# 5. sensor reading

sensor_reading_df = pd.DataFrame()
sensor_reading_df["ReadingID"] = [f"R{str(i).zfill(5)}" for i in range(21, 21 + len(master_df))]
sensor_reading_df["HomeID"] = master_df["HomeID"]
sensor_reading_df["LocalDeviceID"] = np.random.choice(sensor_df["LocalDeviceID"], len(master_df))
sensor_reading_df["ConditionType"] = np.random.choice(weather_df["ConditionType"], len(master_df))
sensor_reading_df["Value"] = master_df["temperature"]
sensor_reading_df["Timestamp"] = pd.to_datetime(master_df["time"], unit='s')

# ----------------------------------------------------------------------------------------------------

smart_home_df.to_csv("smart_home.csv", index=False)
sensor_df.to_csv("sensor.csv", index=False)
health_df.to_csv("system_health_profile.csv", index=False)
weather_df.to_csv("weather_condition.csv", index=False)
sensor_reading_df.to_csv("sensor_reading.csv", index=False)

print("Done.")
print("Saved: sensor_reading.csv")
print("Saved: sensor.csv")
print("Saved: smart_home.csv")
print("Saved: system_health_profile.csv")
print("Saved: weather_condition.csv")