import pandas as pd

df_customers = pd.read_csv('data/raw/customers_data.csv')
df_products = pd.read_csv('data/raw/products_data.csv')
df_sales = pd.read_csv('data/raw/sales_data.csv')

most_common_region = df_customers['Region'].value_counts().idxmax()
min_value = df_products['UnitPrice'].min()
max_value = df_products['UnitPrice'].max()
min_sales = df_sales['SaleAmount'].min()
max_sales = df_sales['SaleAmount'].max()
avg_sales = df_sales['SaleAmount'].mean()

print(f"Most Common Location: {most_common_region}")
print(f"Highest Product Price: {max_value}")
print(f"Lowest Product Price: {min_value}")
print(f"Average Sales: {avg_sales}")
print(f"Min Sales: {min_sales}")
print(f"Max Sales: {max_sales}")

