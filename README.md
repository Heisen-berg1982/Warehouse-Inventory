# Warehouse-Inventory
Warehouse Inventory is a lightweight, local-first inventory management system built with Python and Streamlit. It allows warehouse managers to track stock levels, process sales, visualize trends, and manage their product catalog through an intuitive web interface.
📦 Warehouse Inventory 

Warehouse Inventory Pro is a professional-grade inventory management and sales tracking system built with Python, Streamlit, and Pandas. Designed for small to medium-sized warehouses, it provides an intuitive interface to manage stock, visualize business performance, and record sales transactions in real-time.

🚀 Features

📊 Dynamic Dashboard

Real-time Metrics: Tracks total stock volume, total inventory valuation, and total revenue.

Data Visualization: Interactive Plotly charts showing stock distribution by category and daily revenue trends.

📋 Inventory Control

Smart Viewing: Filter stock by category or search by item name.

Low Stock Alerts: Automatic red highlighting for items with low stock (below 20 units) to prevent stockouts.

🛒 Sales Processing

Automated Deductions: Selling an item automatically updates inventory levels.

Revenue Tracking: Every sale is logged into a sales history with timestamps for trend analysis.

➕ Stock Management

Update Existing: Quickly add units to current inventory.

New Entry: Register new items with ID, Category, and Pricing.

Disposal: Dedicated section to remove damaged goods or delete discontinued products.

🛠️ Installation

Follow these steps to get the system running locally:

1. Clone the Repository

git clone [Add the link of this repostory]
cd warehouse-inventory-pro


2. Install Dependencies

pip install streamlit pandas plotly


3. Setup Data Files

The app requires two CSV files in the root directory. If they don't exist, create them with the following headers:

inventory_data.csv

Item_ID,Name,Category,Quantity,Price


sales_history.csv

Date,Item_Name,Quantity_Sold,Revenue


4. Run the Application

streamlit run app.py


📂 Project Structure

app.py: The main Python script containing the Streamlit application logic.

inventory_data.csv: Local database for all current stock items.

sales_history.csv: Log of all completed sales transactions.

README.md: Project documentation.

🖥️ Requirements

Python: 3.8+

Libraries: - streamlit: Web interface

pandas: Data manipulation

plotly: Interactive charts
