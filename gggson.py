import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(
    page_title="Warehouse Inventory Pro",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)


INV_FILE = "inventory_data.csv"
SALES_FILE = "sales_history.csv"


def load_inventory():
    return pd.read_csv(INV_FILE)

def save_inventory(df):
    df.to_csv(INV_FILE, index=False)

def load_sales():
    return pd.read_csv(SALES_FILE)

def save_sales(df):
    df.to_csv(SALES_FILE, index=False)

df_inventory = load_inventory()
df_sales = load_sales()

st.sidebar.title("📦 Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Go to",
    ["📊 Dashboard", "📋 View Stock", "➕ Add / Update Stock", "🛒 Sell Stock", "🗑️ Remove Stock"]
)

if page == "📊 Dashboard":
    st.title("📊 Warehouse Dashboard")
    st.markdown("Overview of your current inventory and sales performance.")
    
    total_items = df_inventory['Quantity'].sum()
    total_value = (df_inventory['Quantity'] * df_inventory['Price']).sum()
    total_sales = df_sales['Revenue'].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Items in Stock", f"{total_items:,}")
    col2.metric("Total Inventory Value", f"${total_value:,.2f}")
    col3.metric("Total Sales Revenue", f"${total_sales:,.2f}")
    
    st.markdown("---")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Current Stock Levels")
        fig_stock = px.bar(
            df_inventory, 
            x='Name', 
            y='Quantity', 
            color='Category',
            text_auto=True,
            title="Stock Quantity by Item"
        )
        fig_stock.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_stock, use_container_width=True)
        
    with col_chart2:
        st.subheader("Sales History Trends")
        df_sales_grouped = df_sales.groupby('Date')['Revenue'].sum().reset_index()
        fig_sales = px.line(
            df_sales_grouped, 
            x='Date', 
            y='Revenue', 
            markers=True,
            title="Daily Revenue Trend"
        )
        st.plotly_chart(fig_sales, use_container_width=True)


elif page == "📋 View Stock":
    st.title("📋 Current Inventory")
    
    col1, col2 = st.columns(2)
    
    with col1:
        category_filter = st.selectbox("Filter by Category", ["All"] + list(df_inventory['Category'].unique()))
    with col2:
        search_query = st.text_input("Search by Item Name")
        
    filtered_df = df_inventory.copy()
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]
    if search_query:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_query, case=False, na=False)]
        
    def highlight_low_stock(val):
        color = '#ff9999' if type(val) == int and val < 20 else ''
        return f'background-color: {color}'

    st.dataframe(
        filtered_df.style.map(highlight_low_stock, subset=['Quantity']),
        use_container_width=True,
        hide_index=True
    )


elif page == "➕ Add / Update Stock":
    st.title("➕ Add New or Update Existing Stock")
    
    tab1, tab2 = st.tabs(["Update Existing Item", "Add Completely New Item"])
    
    with tab1:
        with st.form("update_stock_form"):
            selected_item = st.selectbox("Select Item to Update", df_inventory['Name'].tolist())
            qty_to_add = st.number_input("Quantity to Add", min_value=1, step=1)
            submit_update = st.form_submit_button("Update Stock")
            
            if submit_update:
                df_inventory.loc[df_inventory['Name'] == selected_item, 'Quantity'] += qty_to_add
                save_inventory(df_inventory)
                st.success(f"Added {qty_to_add} units to {selected_item}. Inventory updated!")
                st.rerun()

    with tab2:
        with st.form("add_new_item_form"):
            new_id = st.text_input("Item ID (e.g., ITM-1005)")
            new_name = st.text_input("Item Name")
            new_cat = st.selectbox("Category", ["Electronics", "Furniture", "Accessories", "Stationery", "Other"])
            new_qty = st.number_input("Initial Quantity", min_value=0, step=1)
            new_price = st.number_input("Unit Price ($)", min_value=0.0, step=0.5)
            
            submit_new = st.form_submit_button("Add New Item")
            
            if submit_new:
                if new_id in df_inventory['Item_ID'].values or new_name in df_inventory['Name'].values:
                    st.error("Item ID or Name already exists! Use the 'Update' tab instead.")
                elif not new_id or not new_name:
                    st.error("Please fill in ID and Name.")
                else:
                    new_row = pd.DataFrame([{
                        'Item_ID': new_id, 'Name': new_name, 'Category': new_cat, 
                        'Quantity': new_qty, 'Price': new_price
                    }])
                    df_inventory = pd.concat([df_inventory, new_row], ignore_index=True)
                    save_inventory(df_inventory)
                    st.success(f"Successfully added new item: {new_name}")
                    st.rerun()


elif page == "🛒 Sell Stock":
    st.title("🛒 Process a Sale")
    st.markdown("Record a sale. This will deduct from inventory and update the sales history graph.")
    
    with st.form("sell_stock_form"):
        item_options = [f"{row['Name']} (Available: {row['Quantity']})" for _, row in df_inventory.iterrows()]
        selected_option = st.selectbox("Select Item to Sell", item_options)
        
        actual_name = selected_option.split(" (Available")[0]
        current_qty = df_inventory.loc[df_inventory['Name'] == actual_name, 'Quantity'].values[0]
        item_price = df_inventory.loc[df_inventory['Name'] == actual_name, 'Price'].values[0]
        
        qty_to_sell = st.number_input("Quantity to Sell", min_value=1, max_value=int(current_qty) if current_qty > 0 else 1, step=1)
        
        submit_sale = st.form_submit_button("Complete Sale")
        
        if submit_sale:
            if current_qty < qty_to_sell:
                st.error(f"Cannot sell {qty_to_sell}. Only {current_qty} left in stock!")
            else:
                df_inventory.loc[df_inventory['Name'] == actual_name, 'Quantity'] -= qty_to_sell
                save_inventory(df_inventory)
                
                revenue = qty_to_sell * item_price
                today_str = datetime.today().strftime('%Y-%m-%d')
                
                new_sale = pd.DataFrame([{
                    'Date': today_str,
                    'Item_Name': actual_name,
                    'Quantity_Sold': qty_to_sell,
                    'Revenue': revenue
                }])
                df_sales = pd.concat([df_sales, new_sale], ignore_index=True)
                save_sales(df_sales)
                
                st.success(f"Sale successful! Sold {qty_to_sell}x {actual_name} for ${revenue:,.2f}.")
                st.rerun()


elif page == "🗑️ Remove Stock":
    st.title("🗑️ Remove or Adjust Stock")
    st.markdown("Use this to remove damaged goods or completely delete discontinued items.")
    
    tab1, tab2 = st.tabs(["Reduce Quantity (Damage/Loss)", "Delete Item Completely"])
    
    with tab1:
        with st.form("reduce_stock_form"):
            selected_item_reduce = st.selectbox("Select Item", df_inventory['Name'].tolist())
            current_qty = df_inventory.loc[df_inventory['Name'] == selected_item_reduce, 'Quantity'].values[0]
            
            qty_to_remove = st.number_input(f"Amount to Remove (Current: {current_qty})", min_value=1, max_value=int(current_qty) if current_qty>0 else 1, step=1)
            reason = st.text_input("Reason (Optional, e.g., Damaged)")
            
            submit_reduce = st.form_submit_button("Remove Quantity")
            
            if submit_reduce:
                df_inventory.loc[df_inventory['Name'] == selected_item_reduce, 'Quantity'] -= qty_to_remove
                save_inventory(df_inventory)
                st.warning(f"Removed {qty_to_remove} units of {selected_item_reduce}.")
                st.rerun()

    with tab2:
        with st.form("delete_item_form"):
            st.error("⚠️ Warning: This will completely delete the item from the database.")
            selected_item_delete = st.selectbox("Select Item to Delete", df_inventory['Name'].tolist())
            
            submit_delete = st.form_submit_button("Permanently Delete Item")
            
            if submit_delete:
                df_inventory = df_inventory[df_inventory['Name'] != selected_item_delete]
                save_inventory(df_inventory)
                st.success(f"Item '{selected_item_delete}' has been deleted from inventory.")
                st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Warehouse Inventory System v1.0")