import pandas as pd
import re  # ← Don't forget this!

# Load the CSV
df_sales = pd.read_csv('data/prepared/sales_data_prepared.csv')

# Function to convert to snake_case
def to_snake_case(col):
    col = re.sub(r'(?<!^)(?=[A-Z])', '_', col).lower()
    col = col.replace(' ', '_')
    return col

# Apply to column names
df_sales.columns = [to_snake_case(col) for col in df_sales.columns]

# Save it back to CSV
df_sales.to_csv('data/prepared/sales_data_prepared.csv', index=False)