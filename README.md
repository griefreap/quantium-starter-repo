# Quantium Starter Repo – Pink Morsel Sales Dashboard

This project processes Soul Foods' sales data and visualises **Pink Morsel sales** over time to answer:  
> Were sales higher before or after the price increase on **2021-01-15**?

It includes:  
* Data cleaning & processing scripts  
* A Dash web app for visualisation  
* A test suite to ensure the app works correctly  

---

## Project Structure

quantium-starter-repo/
├── data/ # Raw data files
├── cleaned_sales.csv # Processed output
├── app.py # Dash app
├── process_sales.py # Build cleaned_sales.csv
├── clean_data.py # Data cleaning script
├── check_products.py # Optional checks
├── tests/
│ └── test_app.py # Automated tests for the Dash app
├── requirements.txt # Dependencies
└── README.md # Project documentation
