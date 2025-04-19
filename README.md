# smart-store-kjleopold
BI and Analytics Project

## Project Setup
### 1. Create a Repository in GitHub
1. Name repository smart-store-kjleopold.
2. Make sure Public is selected.
3. Make sure to add README.md.
4. Create repository.

### 2. Clone Repo to Local
1. Copy URL to the GitHub Repository.
2. Open a terminal in the root (Project) folder.
3. Enter into terminal:
```
git clone (past URL)
```
4. Check that everything cloned as expected.

### 3. Create .gitignore and requirements.txt
1. Create new file in root project folder named: `.gitignore`
2. Create new file in root project folder named: `requirements.txt`
3. Find `.gitignore` file in course repo and copy/paste into local `.gitignore`
4. Find `requirements.txt` file in course repo and copy/paste into local `requirements.txt`

### 4. Git Add/Commit/Push
```
git add .
git commit -m "Add meaningful comment"
git push
```

### 5. Create Virtual Environment
1. From the root project folder:
```
py -m venv .venv
```
2. Accept VS Code suggestions.

### 6. Activate Virtual Environment
```
.venv\Scripts\activate
```

### 7. Install Dependencies
1. Verify .venv is activated (will have a green .venv in terminal)
2. Enter the following commands in PowerShell:
```
py -m pip install --upgrade pip setuptools wheel
py -m pip install -r requirements.txt
```

### 8. Select VS Code Interperter
1. Open the Command Pallette: `Ctrl+Shift+P`
2. Search for "Python: Select Interpreter"
3. Select local .venv option
4. Restart terminal
5. Activate .venv

### 9. Create Folders
1. data
   - raw
   - prepared
2. scripts
3. utils

### 10. Download Data Files
Find raw data .csv files in course repo and download to data\raw folder
- customers_data.csv
- products_data.csv
- sales_data.csv

### 11. Download and Install Power BI

### 12. Create logger.py and data_prep.py
1. Create `logger.py` file under utils folder
2. Find `logger.py` file in course repo and copy/paste contents into local `logger.py`
3. Create `data_prep.py` file under scripts folder
4. Find `data_prep.py` file under `smart-sales-starter-files` repo and copy/paste into local `data_prep.py`
5. Execute Python script:
```
py scripts\data_prep.py
```

### 13. Data Collection
1. Add to `customers_data.csv`: LoyaltyPoints and PreferredContactMethod columns
2. Add to `products_data.csv`: Quantity and Supplier columns
3. Add to `sales_data.csv`: BonusPoints and State
4. Add fake data to all the new columns
   
### 14. Data Cleaning & ETL Preparation
1. Create `data_preparation` subfolder in the `scripts` folder
2. Create a Python file fr each table
   * prepare_customers_data.py
   * prepare_products_data.py
   * prepare_sales_data.py
3. Copy/paste the Module 3 example scripts found in GitHub into each Python file
4. Make adjustments to the scripts as needed to clean the raw data files

### 15. Prepare Data for ETL
1. Create `data_scrubber.py` file in the `data_preparation` folder
2. Copy/Paste the example `data_scrubber.py` from GitHub into the new file
3. Complete the TODO within the `data_scrubber.py`
4. Create `tests` folder in the root project folder
5. Create `test_data_scrubber.py` file in the `tests` folder
6. Copy/Paste the example `test_data_scrubber.py` from GitHub into the new file
7. Run the test script from the root project folder
```
py tests\test_data_scrubber.py
```
8. Make sure all tests pass
9. DataScrubber can now be added to `data_preparation` files

### 16. Complete Data Preparation
1. Run `data_prep.py`

### 17. Design Data Warehouse
1. Create schema using the Star Schema
* Fact Table: Sales
   - Primary Key: transaction_id
   - Foreign Keys: customer_id and product_id
* Dimension Tables: Customers, Products
   - Primary Keys: customer_id, product_id
* Dates work best as TEXT data type in SQLite

### 18. Create Data Warehouse
1. Define the schema for the fact and dimension tables
2. Ensure fact table includes foreign keys that reference the primary keys of the dimension tables
3. Follow conventions for naming tables and columns
4. Run the python file to create the `dw` folder with the `smart_sales.db` data warehouse
```
py scripts\create_dw.py
```

### 19. Implement DW
* Add the data from the prepared CSV files to the data warehouse
```
py scripts\etl_to_dw.py
```

Examples:
![Screenshot](screenshots/customers.jpg)
![Screenshot](screenshots/products.jpg)
![Screenshot](screenshots/sales.jpg)

### 20. Power BI Query and Dashboard
* The below code was used to transform the customer data table to a table that sorted the customers by the amount they spent. ChatGPT was a big help with converting the SQL code to M code for use in Power BI Advanced Editor.
```
let
    // Connect to the data source
    Source = Odbc.DataSource("dsn=SmartSalesDSN", [HierarchicalNavigation=true]),

    // Load the sale and customer tables
    sale_Table = Source{[Name="sale", Kind="Table"]}[Data],
    customer_Table = Source{[Name="customer", Kind="Table"]}[Data],

    // Join sale with customer on customer_id
    MergedTables = Table.NestedJoin(sale_Table, "customer_id", customer_Table, "customer_id", "CustomerData", JoinKind.Inner),

    // Expand the customer name from the joined table
    ExpandedTable = Table.ExpandTableColumn(MergedTables, "CustomerData", {"name"}),

    // Group by customer name and sum the sale_amount
    GroupedTable = Table.Group(ExpandedTable, {"name"}, {{"total_spent", each List.Sum([sale_amount]), type number}}),

    // Sort the results by total_spent in descending order
    SortedTable = Table.Sort(GroupedTable, {{"total_spent", Order.Descending}})
in
    SortedTable
```

* This is the resulting table.  
![Screenshot](screenshots/Top_Customers.jpg)

* This screenshot represents the model view for my tables.
![Screenshot](screenshots/PowerBI_Model_View.jpg)

* This screenshot represents the final dashboard I came up with.
![Screenshot](screenshots/PowerBI_Final_Dashboard.jpg)

## Module 6 OLAP Project
### 1. Business Goal
To identify sales trends by region across different categories and products.
### 2. Data Source
This project utilizes a data warehouse through an ODBC connection as well as a pre-computed cube.
* Product Table Columns (data warehouse): `product_name`, `category`  
* Multidimensional OLAP Cube Columns (pre-computed cube): `month_name`, `region`, `sale_amount_sum`
### 3. Tools
Power BI was used to get more practice with the capabilities the platform has to offer.
### 4. Workflow & Logic  
* Dimensions Used:  
  * Category: broad classification of products.
  * Product Name: specific items sold.
  * Region: geographic sales areas.
  * Time: Includes Year, Quarter, and Month via date hierarchy  
* Metrics Used:
  * Total Sales Amount: aggregated using SUM(sale_amount_sum).  
* OLAP Techniques Applied:  
  * Slicing: Time-based slicing across Year, Quarter, and Month.
  * Dicing: Focused analysis on combinations of Region and Product.
  * Drilldown: Enabled through a date hierarchy for time-based exploration.  
* Logic:  
  * Data is structured around key business dimensions (Region, Product, Time, and Category) and aggregated by total sales.
  * A date hierarchy is implemented to allow drilldown from Year to Month.
  * Filtering and grouping logic is applied to compare regional and product-level sales trends.
  * Data model relationships support cross-filtering between categories, products, and regions for deeper analysis.  
### 5. Results  
* Pie Chart – Regional Sales Totals 
The East region contributes over 50% of total sales, dominating all other regions. The North region underperforms, making up less than 5% of sales. South and West contribute 22% and 15%, respectively.  
* Line Chart – Regional Sales Trends (over time)  
The South and West regions follow similar trends, with the West peaking one month later. The East region experiences a sharp drop in May, followed by a major rebound in June–July. North remains stable.  
* Matrix – Number of Sales per Product 
Laptops are the top-selling product, while cables consistently underperform across the board.  
* Bar Chart – Regional Sales by Category  
Electronics lead in every region except the North, where Clothing takes the top spot. Sports is the lowest-selling category in all regions.  

This screenshot shows the completed dashboard.  
![Screenshot](screenshots/olap_dashboards_v2.jpg)
This screenshot shows how the visual changes when the slicer dates are adjusted.
![Screenshot](screenshots/olap_dashboards2.jpg)
### 6. Suggested Business Actions  
Based on the analysis, the East region is clearly pulling in the most sales, over 50%, so it makes sense to keep investing there. The North, on the other hand, might need some extra attention, like targeted marketing or special promotions, to help boost its performance. There’s a noticeable dip in East sales around mid-year, so some seasonal planning could help smooth that out. The South and West show similar trends, which could be a great chance to sync up inventory and campaigns between them. Laptops are top sellers and could do even better with bundles or more promotion, while cables aren’t doing so hot and might need to be rethought. Electronics are strong across the board, clothing does especially well in the North, and sports gear is lagging everywhere, so product strategies should be adjusted based on what’s working where.
### 7. Challenges
I had put in a lot of work to learn Power BI after the last module, so I didn't really run into any challenges or issues with this module. 

## Module 7 Project
### 1. Business Goal
To analyze a Spotify user survey dataset to improve Spotify's subscription conversion strategy.
### 2. Data Source
Main dataset was obtained from Kaggle: [Spotify User Behavior Survey](https://www.kaggle.com/datasets/coulsonlll/spotify-user-behavior-survey-data)  
I also manually created a price list from the Spotify website for the current premium plans and pricing: [Spotify Premium Plans](https://www.spotify.com/us/premium/)  
### 3. Tools Used
My chosen tools were to create a data warehouse using Python scripts and load the tables to Power BI to do my analysis and create visuals.
### 4. Workflow & Logic  
* Data Understanding & Cleaning
  * Dropped unneeded columns.
  * Tried to use script to replace "None" values to "Free", but could not get the script to work so I did it manually. It wasn't hard or time consuming for this project, but I will need to work more on figuring out how to do it in code for future projects that aren't as cut and dry.
* Dimensions Used:  
  * Age: to understand usage across demographics
  * Spotify Subscription Plan: to identify the popularity of different plans.
  * Premium Subscription Willingness: to measure conversion potential.
  * Preferred Premium Plan: to understand future preferences. 
* Metrics and Calculations Used:
  * Current premium revenue: sum calculated based on existing paid users and plan prices.
  * Potential revenue: sum calculated by users willing to convert to their preferred premium plan.
* Aggregations:
  * User counts by age, current plan, willingness, and preference.
  * Summing revenue to quantify current and potential earnings.
* OLAP Techniques Applied:  
  * Slice data by current plan.
  * Dice data by willingness to pay, preferred plan, and price.
  * Use hierarchies based on age to drill down to current and preferred plans. 
* Logic:  
  * Identify users on free plans who are willing to pay by performing aggregations on the data.
  * Analyze age, current plan, and preferences to find patters in usage and potential upgrades.
  * Calculate current vs. potential revenue based on users' preferred premium plans and pricing.

