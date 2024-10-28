import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('data/survey.csv')

# Streamlit app
st.title("School and Course Employment Data")

# Sidebar for filtering
st.sidebar.header("Filter Options")
#selected_school = st.sidebar.selectbox("Select School", data['school'].unique())
#selected_course = st.sidebar.selectbox("Select Degree", data['degree'].unique())

#----
# Initialize session state for selected_course if it doesn't exist
if 'selected_school' not in st.session_state:
    st.session_state.selected_school = ""

if 'selected_course' not in st.session_state:
    st.session_state.selected_course = ""

# Callback function to update course selection when school changes
def update_course(selected_school):
    # Clear the selected course when the school changes
    st.session_state.selected_course = ""

# School selection
selected_school = st.sidebar.selectbox("Select School", data['school'].unique(), 
                                        on_change=update_course, args=(st.session_state.selected_school,))

# Course selection, only show courses relevant to the selected school
if selected_school:
    filtered_courses = data[data['school'] == selected_school]['degree'].unique()
    selected_course = st.sidebar.selectbox("Select Degree", filtered_courses, index=0)
    st.session_state.selected_course = selected_course
else:
    selected_course = st.sidebar.selectbox("Select Degree", [])

# Filter data based on user selection
filtered_data = data[(data['school'] == selected_school) & (data['degree'] == st.session_state.selected_course)]


data['basic_monthly_mean'] = pd.to_numeric(data['basic_monthly_mean'], errors='coerce')
# User input for top 'N' courses
top_n = st.sidebar.number_input("Enter the number of top courses to display", min_value=1, max_value=20, value=5)

 # Chart for the top 5 courses based on graduate salary
st.subheader("Top 5 Graduate Salaries")
#top_5_courses = data.nlargest(5, 'basic_monthly_mean')
top_n_courses = data.nlargest(top_n, 'basic_monthly_mean')
if not top_n_courses.empty:
        fig, ax = plt.subplots()
        ax.bar(top_n_courses['degree'], top_n_courses['basic_monthly_mean'], color='lightblue')
        ax.set_ylabel('Graduate Salary ($)')
        ax.set_title(f'Top {top_n} Graduate Salaries')
        plt.xticks(rotation=80)
        st.pyplot(fig)
else:
        st.error("No data available to display the top salaries.")


st.write("--------------------------")
st.header("Filtered Result: ")
# Display filtered data (you can customize this part)
st.write(filtered_data)


#----


# Filter data based on user selection
#filtered_data = data[(data['school'] == selected_school) & (data['degree'] == selected_course)]

# Check if filtered data is empty
if filtered_data.empty:
    st.error("No data available for the selected school and course.")
else:
    # Tabs for data display
    tab1, tab2 = st.tabs(["Data Overview", "Detailed Stats"])

    with tab1:
        st.subheader("Data Overview")
        st.dataframe(filtered_data)

    with tab2:
        st.subheader("Detailed Statistics")
        employment_rate = filtered_data['employment_rate_overall'].values[0]
        myyear = filtered_data['year'].values[0]
        
        st.write(f"**Employment Rate:** {employment_rate}%")
        st.write(f"**Year:** {myyear}")

    
    