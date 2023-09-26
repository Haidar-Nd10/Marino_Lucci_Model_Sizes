# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 13:48:42 2023

@author: Haidar
"""

import streamlit as st
import pandas as pd
import base64

# Load your inventory dataset
inventory = pd.read_csv(r'C:\Users\Haidar\Desktop\Marino Lucci\inventory for photography.csv', encoding='ISO-8859-1')

# Initialize an empty list to store outfit data in session state
if 'outfits_data' not in st.session_state:
    st.session_state.outfits_data = []

# Streamlit App
st.title("Model Size Creator")

# Create a dictionary to store selected values
selected_values = {
    'Kind': None,
    'Brand': None,
    'Fabric': None,
    'Cut': None,
    'Product_Code': None,
    'Size': None,
}

# Streamlit App
st.sidebar.title("Assign Rules")

# Selectbox for Kind
unique_kinds = ['None'] + list(inventory['Kind'].unique())
selected_values['Kind'] = st.sidebar.selectbox('Kind', unique_kinds)

# Filtered inventory based on Kind selection
filtered_inventory = inventory.copy()
if selected_values['Kind'] != 'None':
    filtered_inventory = filtered_inventory[filtered_inventory['Kind'] == selected_values['Kind']]

# Selectbox for Brand
unique_brands = ['None'] + list(filtered_inventory['Brand'].unique())
selected_values['Brand'] = st.sidebar.selectbox('Brand', unique_brands)

# Filtered inventory based on Brand selection
if selected_values['Brand'] != 'None':
    filtered_inventory = filtered_inventory[filtered_inventory['Brand'] == selected_values['Brand']]

# Selectbox for Fabric
unique_fabrics = ['None'] + list(filtered_inventory['Fabric'].unique())
selected_values['Fabric'] = st.sidebar.selectbox('Fabric', unique_fabrics)

# Filtered inventory based on Fabric selection
if selected_values['Fabric'] != 'None':
    filtered_inventory = filtered_inventory[filtered_inventory['Fabric'] == selected_values['Fabric']]

# Selectbox for Cut
unique_cuts = ['None'] + list(filtered_inventory['Cut'].unique())
selected_values['Cut'] = st.sidebar.selectbox('Cut', unique_cuts)

# Filtered inventory based on Cut selection
if selected_values['Cut'] != 'None':
    filtered_inventory = filtered_inventory[filtered_inventory['Cut'] == selected_values['Cut']]

# Selectbox for Product Code
unique_product_codes = ['None'] + list(filtered_inventory['Product_Code'].unique())
selected_values['Product_Code'] = st.sidebar.selectbox('Product Code', unique_product_codes)

# Input box for Size
selected_values['Size'] = st.sidebar.text_input('Size')

# Add a button to add the outfit to the DataFrame
if st.sidebar.button("Add New Rule"):
    # Append the selected values to the list in session state
    st.session_state.outfits_data.append(selected_values)
    
    # Reset selectbox values to None
    selected_values = {
        'Kind': None,
        'Brand': None,
        'Fabric': None,
        'Cut': None,
        'Product_Code': None,
        'Size': None,
    }

# Remove Row
st.sidebar.subheader('Remove Row')
if len(st.session_state.outfits_data) > 0:
    row_to_remove = st.sidebar.selectbox('Select Row to Remove', list(range(len(st.session_state.outfits_data))))
    if st.sidebar.button("Remove Selected Row"):
        # Remove the selected row from the list in session state
        st.session_state.outfits_data.pop(row_to_remove)

# Display the updated Outfit DataFrame
st.write("Rules DataFrame:")
if len(st.session_state.outfits_data) > 0:
    df = pd.DataFrame(st.session_state.outfits_data)
    st.write(df)

# Add a button to download the DataFrame as a CSV file
if len(st.session_state.outfits_data) > 0:
    csv_data = df.to_csv(index=False, encoding='utf-8-sig')
    b64 = base64.b64encode(csv_data.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="model_size.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
