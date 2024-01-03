#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
from ipywidgets import widgets, interact, Output, VBox, HBox
from IPython.display import display

# Function to toggle the search method and update the interface accordingly
def toggle_search_method(change):
    search_method = change.new
    if search_method == 'By School Code':
        school_code_input.disabled = False
        school_name_input.disabled = True
        dropdown_school_codes.layout.visibility = 'visible'
        dropdown_school_names.layout.visibility = 'hidden'
        dropdown_states.disabled = True
        manual_search_code_button.disabled = False
        manual_search_name_button.disabled = True
        manual_search_state_button.disabled = True
    elif search_method == 'By School Name':
        school_code_input.disabled = True
        school_name_input.disabled = False
        dropdown_school_codes.layout.visibility = 'hidden'
        dropdown_school_names.layout.visibility = 'visible'
        dropdown_states.disabled = True
        manual_search_code_button.disabled = True
        manual_search_name_button.disabled = False
        manual_search_state_button.disabled = True
    elif search_method == 'By State':
        school_code_input.disabled = True
        school_name_input.disabled = True
        dropdown_school_codes.layout.visibility = 'hidden'
        dropdown_school_names.layout.visibility = 'hidden'
        dropdown_states.disabled = False
        manual_search_code_button.disabled = True
        manual_search_name_button.disabled = True
        manual_search_state_button.disabled = False

# Read school data from the Excel file into a DataFrame
excel_file_url = 'https://github.com/sharman1209/TM/raw/main/4221%20TM%20UNIFIBIZ.xlsx'
school_df = pd.read_excel(excel_file_url, sheet_name='List TM Interim Sites')

# Function to filter school codes based on the entered query (case-insensitive)
def filter_school_codes(query):
    query_lower = query.lower()
    return school_df[school_df['KOD SEKOLAH'].str.lower().str.contains(query_lower)]['KOD SEKOLAH'].tolist()

# Function to filter school names based on the entered query (case-insensitive)
def filter_school_names(query):
    query_lower = query.lower()
    return school_df[school_df['NAMA SEKOLAH'].str.lower().str.contains(query_lower)]['NAMA SEKOLAH'].tolist()

# Function to filter schools based on the selected state
def filter_schools_by_state(selected_state):
    return school_df[school_df['NEGERI'] == selected_state]

# Function to capitalize the input text
def capitalize_text(change):
    change.new = change.new.upper()
    return change

# Function to handle code dropdown selection
def handle_code_dropdown_selection(change):
    selected_code = change.new
    if selected_code:
        school_code_input.value = selected_code

# Function to handle name dropdown selection
def handle_name_dropdown_selection(change):
    selected_name = change.new
    if selected_name:
        school_name_input.value = selected_name

# Function to handle state dropdown selection
def handle_state_dropdown_selection(change):
    selected_state = change.new
    if selected_state:
        manual_search_state_button.disabled = False

# Function to search for and display school information based on the selected school code
def search_school_info_by_code(selected_code):
    selected_school_info = school_df[school_df['KOD SEKOLAH'] == selected_code]
    display_search_results(selected_school_info)

# Function to search for and display school information based on the selected school name
def search_school_info_by_name(selected_name):
    selected_school_info = school_df[school_df['NAMA SEKOLAH'] == selected_name]
    display_search_results(selected_school_info)

# Function to search for and display school information based on the selected state
def search_school_info_by_state(selected_state):
    selected_schools_by_state = filter_schools_by_state(selected_state)
    display_search_results(selected_schools_by_state)

# Function to display search results as a list
def display_search_results(results_df):
    if not results_df.empty:
        # Display the desired columns
        columns_to_display = ['KOD SEKOLAH', 'NAMA SEKOLAH', 'NEGERI', 'PPD', 'KATEGORI', 'PNEW PAKEJ', 'PNEW ISP', 'PNEW TALIAN', 'TEKNOLOGI', 'LOKASI']
        result_output.clear_output()
        with result_output:
            print("Selected School Information:")
            for _, row in results_df[columns_to_display].iterrows():
                for column_name, value in row.items():
                    print(f"{column_name}: {value}")
                print("---")
            clear_result_button.layout.visibility = 'visible'
    else:
        with result_output:
            result_output.clear_output()
            print("No matching school found")
            clear_result_button.layout.visibility = 'hidden'

# Function to reset the interface
def reset_interface(b):
    search_method_dropdown.value = 'Select'
    school_code_input.value = ''
    school_name_input.value = ''
    dropdown_school_codes.options = []
    dropdown_school_names.options = []
    dropdown_states.value = 'Select'  # Reset the selected state
    result_output.clear_output()
    clear_result_button.layout.visibility = 'hidden'

# Function to clear the displayed search results manually
def clear_results(b):
    result_output.clear_output()
    clear_result_button.layout.visibility = 'hidden'

# Create dropdown widget to select search method
search_method_dropdown = widgets.Dropdown(options=['Select', 'By School Code', 'By School Name', 'By State'], description='Search Method:')
search_method_dropdown.observe(toggle_search_method, names='value')

# Create input box for searching by school code
school_code_input = widgets.Text(description="School Code:", disabled=False)

# Create input box for searching by school name
school_name_input = widgets.Text(description="School Name:", disabled=True)

# Create dropdown for school codes
dropdown_school_codes = widgets.Dropdown(options=[], description="Select School Code:")

# Create dropdown widget for school names
dropdown_school_names = widgets.Dropdown(options=[], description="Select School Name:")

# Create dropdown for selecting the state
dropdown_states = widgets.Dropdown(options=['Select'] + school_df['NEGERI'].unique().tolist(), description="Select State:")

# Observe changes in school codes dropdown
dropdown_school_codes.observe(handle_code_dropdown_selection, names='value')

# Observe changes in school names dropdown
dropdown_school_names.observe(handle_name_dropdown_selection, names='value')

# Link the input boxes to the capitalize_text function
school_code_input.observe(capitalize_text, names='value')
school_name_input.observe(capitalize_text, names='value')

# Create a button to reset the interface
reset_button = widgets.Button(description="Reset")
reset_button.on_click(reset_interface)

# Create a button to manually clear the search results
clear_result_button = widgets.Button(description="Clear Results")
clear_result_button.on_click(clear_results)
clear_result_button.layout.visibility = 'hidden'

# Create an output widget to display search results
result_output = Output()

# Create a button for manual search by code
manual_search_code_button = widgets.Button(description="Search", disabled=True)
manual_search_code_button.on_click(lambda b: search_school_info_by_code(school_code_input.value))

# Create a button for manual search by name
manual_search_name_button = widgets.Button(description="Search", disabled=True)
manual_search_name_button.on_click(lambda b: search_school_info_by_name(school_name_input.value))

# Create a button for manual search by state
manual_search_state_button = widgets.Button(description="Search", disabled=True)
manual_search_state_button.on_click(lambda b: search_school_info_by_state(dropdown_states.value))

# Attach event handlers to input boxes and dropdowns
search_method_dropdown.observe(toggle_search_method, names='value')
dropdown_school_codes.observe(handle_code_dropdown_selection, names='value')
dropdown_school_names.observe(handle_name_dropdown_selection, names='value')
dropdown_states.observe(handle_state_dropdown_selection, names='value')

# Create layout for the widgets
input_widgets = VBox([search_method_dropdown,
                      HBox([school_code_input, manual_search_code_button, dropdown_school_codes]),
                      HBox([school_name_input, manual_search_name_button, dropdown_school_names]),
                      HBox([dropdown_states, manual_search_state_button]),
                      result_output,
                      HBox([reset_button, clear_result_button])])

# Display the input widgets and result output
display(input_widgets)


# In[ ]:




