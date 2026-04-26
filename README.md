# COP-3710-Smart-Home-IoT-Sensor-Analytics-Database
Project by Savitri Harkhu

Designing an IoT database storing sensor readings and weather data. It will include anomaly detection queries and retention-based partitioning. The main focus scope of the domain will be on the weather and temperature data collected by the smart home systems that people have in their houses and buildings over the course of minutes, days and a year. This project's end goal is to successfully organize these datasets and be able to relate the large-scale domain through modeling & using a relational schema design.

Dataset Source - https://traces.cs.umass.edu/docs/traces/smartstar/#:~:text=Home%20A,Home%20A


Database Application: OracleSQL and Python via Visual Studio Code. Using Visual Studio Code will allow for efficient creation of different tables and schemas/users at once, in comparison to the ui of the OracleSQL, where the user writes one line at a time. I will be conncting to the database of Oracle throught the instant client to make it function. This application provides the user with queries that they can type in, with their results displayed in the command window. 

# Below is a Visual Representation of the Entity Relationships via Crow's Foot ER Diagram:
<img width="939" height="525" alt="image" src="https://github.com/user-attachments/assets/43e7e52a-dbbe-45df-934b-a1ec8fb72f4b" />

# How to use this repo:
Step 1: Use the “create_db.sql” to create the database. Downlaod the appropriate instant client.

Step 2: Change line 13 to line 18 in "dataload.py" to add your Oracle database credentials.

Step 3: To connect to the Oracle database, run the command: python -m pip install oracledb 

Step 4: Use the "dataload.py" to populate the Oracle database with the Smart Home data.

Step 5: Change line 15 to line 20 in "app.py" to add your Oracle database credentials.

Step 6: To be able to use streamlit, run the command: python -m pip install streamlit

Step 7: Run the "app.py" using the command: python -m streamlit run app.py

# App's Home Page:
<img width="1910" height="872" alt="image" src="https://github.com/user-attachments/assets/b65560c3-b3c9-4c09-aa06-bf2193d11135" />

