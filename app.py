'''
If you are running this code first time, and you don't have streamlit installed, then follow this instruction:
1. open a terminal
2. enter this command
    pip install streamlit
'''

# to run type in terminal 'streamlit run app.py'

import streamlit as st
import oracledb
import datetime

# --- CONFIGURATION (Connecting to freesql) ---
LIB_DIR = r"Put Directory here"

# Your Oracle Credentials
DB_USER = "Username here" 
DB_PASS = "#" 
DB_DSN  = "#" 

@st.cache_resource
def init_db():
    if LIB_DIR:
        try:
            oracledb.init_oracle_client(lib_dir=LIB_DIR)
        except Exception as e:
            st.error(f"Error initializing Oracle Client: {e}")

init_db()

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)

# --- STREAMLIT UI ---
st.title("Smart Home Data Explorer")
    #Title self explanitory, keeps a big text in the middle of the page
st.sidebar.header("Navigation")
    #sidebar.header makes a sidebar on the left side with a name "Navigation"
menu = [
    "1. Houses by Rain/Time", 
    "2. Sensors by Date", 
    "3. Sensors by Owner", 
    "4. Avg Temp by Weather", 
    "5. Reading Count"
]
#Menu is a array which will be but into the selectbox command below
choice = st.sidebar.selectbox("Choose a Query", menu)
#choice is equal to what we select from the dropdown created by selectbox


# --- Houses that recorded rain at timestamp ---
if choice == "1. Houses by Rain/Time":
    st.subheader("Count Houses that Recorded Rain")
    #ts_input gets data from a text input that you type in, 2024-01-01 12:00:00 is put in the box
    ts_input = st.text_input("Enter Timestamp Format:(YYYY-MM-DD \"Hours in 24 hour format\":\"Minutes\":\"Seconds\") \n The database provided only has hourly timestamps from: 2014-01-01 12:00:00 to 2014-01-24 12:00:00", "2014-01-01 12:00:00")
    
    #once the query button is hit
    if st.button("Query"):
        try:
            #here the connection to fresql is established
            #conn holds the oracledb.Connection value that we get from inputing the right username and password
            conn = get_connection()
            cur = conn.cursor()
            #cur is a thingie (object) that lets you execute SQL commands (select, insert, etc)
            sql = """SELECT DISTINCT h.OwnerEmail 
                FROM Smart_Home h
                JOIN Sensor_Reading r ON h.HomeID = r.HomeID 
                WHERE r.ConditionType = 'Rain' 
                AND r.Timestamp = TO_DATE(:1, 'YYYY-MM-DD HH24:MI:SS')
            """
            #sql command to be executed by the cursor^
            #the command takes a count of all unique home ids from sensor reading where its rainy and
            #the time is equal to our input time
            cur.execute(sql, [ts_input])
            #execute our sql with our timestamp input
            data = cur.fetchall()
            
            if data:
                # Convert the list of tuples into a simple list of emails
                emails = [row[0] for row in data]
                st.write(f"Found {len(emails)} homes with rain at this time:")
                st.table(emails) # Displays the list of emails in a clean table
            else:
                st.info("No homes recorded rain at this specific timestamp.")
            cur.close()
            #ends the sql execution
            conn.close()
            #closes the sql connection
        except Exception as e:
            #display for the error
            st.error(f"Error: {e}")


# --- Sensor types by installation date ---
elif choice == "2. Sensors by Date":
    st.subheader("Find Sensors by Installation Date")
    
    # Check if your data is 2014 or 2024. 
    # Based on your dataload.py earlier, it was 2024.
    date_input = st.date_input("Select Installation Date", datetime.date(2024, 1, 1))

    if st.button("Find Sensor Types"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            
            # TRUNC ensures we compare only the Day/Month/Year
            sql = "SELECT DISTINCT SensorType FROM Sensor WHERE TRUNC(InstallationDate) = :1"
            
            cur.execute(sql, [date_input])
            data = cur.fetchall()
            
            if data:
                st.write("### Sensor Types Found:")
                # Display as a clean list
                for item in data:
                    st.write(f"- {item[0]}")
            else:
                st.info(f"No sensors found for {date_input}. Check if your data uses 2014 or 2024.")
                
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# --- Sensors by owner email ---
elif choice == "3. Sensors by Owner":
    st.subheader("Owner's Device Inventory")
    email_input = st.text_input("Enter Owner Email", "resident@home.com")
    
    if st.button("Fetch Sensors"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Join Smart_Home -> Sensor_Reading -> Sensor
            sql = """SELECT DISTINCT s.LocalDeviceID, s.SensorType 
                     FROM Sensor s
                     JOIN Sensor_Reading r ON s.LocalDeviceID = r.LocalDeviceID
                     JOIN Smart_Home h ON r.HomeID = h.HomeID
                     WHERE h.OwnerEmail = :1"""
            cur.execute(sql, [email_input])
            data = cur.fetchall()
            if data:
                st.table(data)
            else:
                st.info("No sensors found for this email.")
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# ---Average temperature for weather condition ---
elif choice == "4. Avg Temp by Weather":
    st.subheader("Average Temperature Analysis")
    cond_input = st.selectbox("Select Condition", ["Rain", "Sunny", "Cloudy", "Windy", "Thunderstorm"])
    
    if st.button("Calculate Average"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """
                SELECT AVG(r.Value) 
                FROM Sensor_Reading r
                JOIN Weather_Condition w ON r.ConditionType = w.ConditionType
                JOIN Smart_Home h ON r.HomeID = h.HomeID
                JOIN System_Health_Profile hp ON h.HomeID = hp.HomeID
                WHERE w.ConditionType = :1 
                AND hp.UptimePercentage > 99.0
            """
            cur.execute(sql, [cond_input])
            avg_temp = cur.fetchone()[0]
            if avg_temp:
                st.success(f"The average temperature during {cond_input} is {round(avg_temp, 2)}°")
            else:
                st.warning("No data found for this condition.")
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"Error: {e}")

# --- Readings count for Device at Home ---
elif choice == "5. Reading Count":
    st.subheader("Device Reading Frequency")
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Get list of HomeIDs for the dropdown
        cur.execute("SELECT HomeID FROM Smart_Home ORDER BY HomeID")
        home_list = [row[0] for row in cur.fetchall()]
        
        selected_home = st.selectbox("Select Home ID", home_list)
        device_id = st.text_input("Enter Local Device ID (e.g., S01-S105)")
        
        if st.button("Get Count"):
            sql = "SELECT COUNT(*) FROM Sensor_Reading WHERE HomeID = :1 AND LocalDeviceID = :2"
            cur.execute(sql, [selected_home, device_id])
            count = cur.fetchone()[0]
            st.info(f"Device {device_id} has {count} readings at Home {selected_home}.")
        
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Error fetching homes: {e}")
