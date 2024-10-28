import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Graduate Employment Survey")
st.title("Garduate Employment Survey")
st.write(
    """
    This app visualizes data from "Graduate Employment Survey - NTU, NUS, SIT, SMU, SUSS & SUTD".
    It shows the emplyment rate and the gross pay of the graduate from respective local uni and school. The data is from Jan 2013 to 2022.
    This data assists prospective students to make informed course decisions.
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/survey.csv")
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
university = st.multiselect(
    "University",
    df.university.unique(),
    ["Nanyang Technological University", "National University of Singapore", "Singapore Management University", "Singapore Institute of Technology"],
)

School = st.multiselect(
    "School",
    df.school.unique(),
    ["College of Engineering"],
)

Degree = st.multiselect(
    "Degree",
    df.degree.unique(),
    ["English"],
)

# Show a slider widget with the years using `st.slider`.
years = st.slider("Year", 1986, 2006, (2013, 2022))

# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["university"].isin(university)) & (df["year"].between(years[0], years[1])) & (df["school"].isin(School)) & (df["degree"].isin(Degree))]
#df_reshaped = df_filtered.pivot_table(
#    index="year", columns=["university"], values="employment_rate_overall", aggfunc="sum", fill_value=0
#)
df_reshaped = df_filtered[["university", "school", "degree", "year", "employment_rate_overall", "basic_monthly_mean"]]
df_reshaped = df_reshaped.sort_values(by="year", ascending=False)
#df_reshaped = df_reshaped[["university","year"]].shape

#.pivot_table(
#    index="year", columns="university", values="employment_rate_overall", aggfunc="sum", fill_value=0
#)


# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_reshaped,
    use_container_width=True,
    column_config={"year": st.column_config.TextColumn("Year"), "university": st.column_config.TextColumn("Uni")}, hide_index="True", 
)

# Display the data as an Altair chart using `st.altair_chart`.
df_chart = pd.melt(
    df_reshaped.reset_index(), id_vars="year", var_name="university", value_name="employment_rate_overall"
)
chart = (
    alt.Chart(df_chart)
    .mark_line()
    .encode(
        x=alt.X("year:N", title="Year"),
        y=alt.Y("gross:Q", title="Gross earnings ($)"),
        color="genre:N",
    )
    .properties(height=320)
)
st.altair_chart(chart, use_container_width=True)
