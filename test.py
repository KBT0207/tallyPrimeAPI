import pandas as pd

# Define the flight data
data = {
    ("DXB-GOI", "IX 839", "Capacity"):       [2000, None, None, 2000, 2000, 2000, 2000],
    ("DXB-GOI", "IX 839", "Utilization"):    [1500, None, None, 0, 0, 2000, 0],
    ("DXB-GOI", "IX 839", "Util %"):         ["75%", None, None, "0%", "0%", "100%", "0%"],
    
    ("DXB-PNQ", "SG", "Capacity"):           [1700]*7,
    ("DXB-PNQ", "SG", "Utilization"):        [0]*7,
    ("DXB-PNQ", "SG", "Util %"):             ["0%"]*7,

    ("SHJ-GOX", "G9 493", "Capacity"):       [None, None, 2000, 2000, 2000, 2000, 2000],
    ("SHJ-GOX", "G9 493", "Utilization"):    [None, None, 1200, 0, 1200, 0, 1200],
    ("SHJ-GOX", "G9 493", "Util %"):         [None, None, "60%", "0%", "60%", "0%", "60%"],

    ("BAH-GOI", "GF 285", "Capacity"):       [2000, 2000, None, 2000, None, 2000, 2000],
    ("BAH-GOI", "GF 285", "Utilization"):    [0, 0, None, 0, None, 0, 0],
    ("BAH-GOI", "GF 285", "Util %"):         ["0%", "0%", None, "0%", None, "0%", "0%"],

    ("BAH-GOI", "GF 287", "Capacity"):       [None, None, 2000, None, 2000, None, None],
    ("BAH-GOI", "GF 287", "Utilization"):    [None, None, 600, None, 0, None, None],
    ("BAH-GOI", "GF 287", "Util %"):         [None, None, "30%", None, "0%", None, None]
}

# Create DataFrame
index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df = pd.DataFrame(data, index=index)

# Save to Excel
df.to_excel("Flight_Schedule_Report.xlsx")