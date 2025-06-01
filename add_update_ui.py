import streamlit as st
from datetime import datetime
import requests
API_URL = "http://127.0.0.1:8000"


def add_update_tab():
   expense_dt = st.date_input("Enter the date : ",datetime(2024,8,1))
#    formatted_date = expense_dt.strftime("%Y-%m-%d")
   response = requests.get(f"{API_URL}/expenses/{expense_dt}")
   if response.status_code == 200:
        existing_expenses = response.json()
        st.write(existing_expenses)
   else:
        st.error('Failed to retrieve expenses')
        existing_expenses = []
#    st.write("Data type of existing_expenses:", type(existing_expenses))
   categories = ["Rent","Food","Shopping","Entertainment","Other","Groceries","Day-out with her","Mac Book"]
   with st.form("expense_form"):
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")   
        with col3:
            st.subheader("Notes")    
        expenses = []
        for i in range(5):
         if i < len(existing_expenses):
          amount = existing_expenses[i]['amount']
          category = existing_expenses[i]['category']
          notes = existing_expenses[i]['notes']
         else:
          amount = 0.0
          category = "Shopping"
          notes = ""

    # Create 3 columns for each row
         col1, col2, col3 = st.columns(3)

         with col1:
          amount_input = st.number_input(
                label="Amount",
                min_value=0.0,
                value=amount,
                step=5.0,
                key=f"amount_{i}"
            )

         with col2:
          category_selection = st.selectbox(
                label="Category",
                options=categories,
                index=categories.index(category) if category in categories else 0,
                key=f"category_{i}"
            )       

         with col3:
          notes_input = st.text_input(
                label="Notes",
                value=notes,
                key=f"notes_{i}"
            )

    # Append the filled-in data to the expenses list
         expenses.append({
                'expense_date': expense_dt.strftime("%Y-%m-%d"),
                'amount': amount_input,
                'category': category_selection,
                'notes': notes_input
            })

                              
        submit_button = st.form_submit_button("Submit")     

            # expenses.append()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount']>0]
            response = requests.post(f"{API_URL}/expenses/{expense_dt}", json = filtered_expenses)
            if response.status_code == 200:
             st.success("Record Updated Successfully")
            else:
                st.error("Failed to update expenses.")
                
