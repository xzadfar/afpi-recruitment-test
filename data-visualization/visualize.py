import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="db-afpi-recruitment-test",
    user="irsyad",
    password="irsyad-afpi-test",
    host="localhost",     # or your host
    port="5432"           # default PostgreSQL port
)

# Load data into a DataFrame
query = "SELECT bulan, ticket_size FROM DWH.TICKET_SIZE where RIGHT(bulan, 4) = '2024' ORDER BY id "
df = pd.read_sql(query, conn)

# Close connection
conn.close()

# Optional: convert data1 to datetime if needed
df['bulan'] = pd.to_datetime(df['bulan'])

# Plot line chart
plt.subplots(figsize=(10, 6), num="ticket size line chart visualization")
plt.plot(df['bulan'], df['ticket_size'], marker='o', linestyle='-', color='blue')
plt.title('Ticket Size Trends by Month')
plt.xlabel('Month')
plt.ylabel('Ticket')
plt.grid(True)
# plt.tight_layout()
plt.xticks(rotation=45)
plt.show()
