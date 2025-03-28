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
   
### Data Cleaning & ETL Preparation
1. Create `data_preparation` subfolder in the `scripts` folder
2. Create a Python file fr each table
   * prepare_customers_data.py
   * prepare_products_data.py
   * prepare_sales_data.py
3. Copy/paste the Module 3 example scripts found in GitHub into each Python file
4. Make adjustments to the scripts as needed to clean the raw data files

### Prepare Data for ETL
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