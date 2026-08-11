import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

# ----------------------------------------------------
# PAGE CONFIGURATION
# ----------------------------------------------------
st.set_page_config(
    page_title="Restaurant Intelligence Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# ----------------------------------------------------
# MYSQL CONNECTION
# ----------------------------------------------------
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootroot",
        database="restaurant_db"
    )

conn = get_connection()

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM uber_eats_data"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    cursor.close()
    return pd.DataFrame(rows, columns=columns)

df = load_data()

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------
st.title("🍽️ Restaurant Intelligence Dashboard")
st.markdown("### Restaurant Data Analysis using Python, MySQL & Streamlit")

# ----------------------------------------------------
# SIDEBAR FILTERS
# ----------------------------------------------------
st.sidebar.header("Filters")

locations = sorted(df["location"].dropna().unique())
selected_location = st.sidebar.selectbox("Select Location", ["All"] + locations)

filtered_df = df.copy()
if selected_location != "All":
    filtered_df = filtered_df[filtered_df["location"] == selected_location]

# Search Restaurant
search = st.sidebar.text_input("🔍 Search Restaurant")
if search:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(search, case=False, na=False)
    ]

# ----------------------------------------------------
# DASHBOARD SUMMARY
# ----------------------------------------------------
st.subheader("Dashboard Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Restaurants", len(filtered_df))
col2.metric("Locations", filtered_df["location"].nunique())
col3.metric("Average Rating", round(filtered_df["rate"].mean(), 2))
col4.metric("Restaurant Types", filtered_df["rest_type"].nunique())

# ----------------------------------------------------
# DATASET
# ----------------------------------------------------
st.subheader("Restaurant Dataset")
st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------------------------
# TOP 10 LOCATIONS
# ----------------------------------------------------
st.subheader("Top 10 Restaurant Locations")
location_count = filtered_df["location"].value_counts().head(10)
fig1 = px.bar(
    x=location_count.index,
    y=location_count.values,
    labels={"x": "Location", "y": "Restaurants"},
    title="Top 10 Restaurant Locations"
)
st.plotly_chart(fig1, use_container_width=True, key="location_chart")

# ----------------------------------------------------
# TOP 10 HIGHEST RATED RESTAURANTS
# ----------------------------------------------------
st.subheader("Top Rated Restaurants")
top_restaurants = (
    filtered_df.sort_values("rate", ascending=False)[["name", "location", "rate"]].head(10)
)
st.dataframe(top_restaurants, use_container_width=True)

# ----------------------------------------------------
# RESTAURANT TYPES
# ----------------------------------------------------
st.subheader("Top Restaurant Types")
rest_type = filtered_df["rest_type"].value_counts().head(10)
fig2 = px.bar(
    x=rest_type.index,
    y=rest_type.values,
    labels={"x": "Restaurant Type", "y": "Count"},
    title="Top Restaurant Types"
)
st.plotly_chart(fig2, use_container_width=True, key="rest_type_chart")

# ----------------------------------------------------
# ONLINE ORDER AVAILABILITY
# ----------------------------------------------------
st.subheader("Online Order Availability")
online = filtered_df["online_order"].value_counts()
fig3 = px.pie(values=online.values, names=online.index, title="Online Order Distribution")
st.plotly_chart(fig3, use_container_width=True, key="online_chart")

# ----------------------------------------------------
# TABLE BOOKING AVAILABILITY
# ----------------------------------------------------
st.subheader("Table Booking Availability")

booking = filtered_df["book_table"].value_counts()

fig4 = px.pie(
    values=booking.values,
    names=booking.index,
    title="Table Booking Distribution"
)

st.plotly_chart(
    fig4,
    use_container_width=True,
    key="booking_chart"
)

# ----------------------------------------------------
# AVERAGE RATING BY LOCATION
# ----------------------------------------------------
st.subheader("Top Rated Locations")
avg_rating = (
    filtered_df.groupby("location")["rate"].mean().sort_values(ascending=False).head(10)
)
fig5 = px.bar(
    x=avg_rating.index,
    y=avg_rating.values,
    labels={"x": "Location", "y": "Average Rating"},
    title="Average Rating by Location"
)
st.plotly_chart(fig5, use_container_width=True, key="rating_chart")

# ----------------------------------------------------
# COST VS RATING
# ----------------------------------------------------
if "approx_cost(for two people)" in filtered_df.columns:
    st.subheader("Cost vs Rating")
    fig6 = px.scatter(
        filtered_df,
        x="approx_cost(for two people)",
        y="rate",
        color="online_order",
        hover_name="name",
        title="Cost vs Rating"
    )
    st.plotly_chart(fig6, use_container_width=True, key="scatter_chart")

# ----------------------------------------------------
# DOWNLOAD FILTERED DATA
# ----------------------------------------------------
st.subheader("Download Filtered Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="restaurant_data.csv",
    mime="text/csv"
)

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------
st.markdown("---")
st.success("✅ Restaurant Intelligence Dashboard Loaded Successfully")
st.markdown(
    """
    <div style="text-align:center; padding:10px;">
        <h3>👩‍💻 Developed by Priyanka R</h3>
        <p><b>Restaurant Intelligence Dashboard</b></p>
        <p>Python | MySQL | Streamlit | Plotly</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------
# CLOSE DATABASE CONNECTION
# ----------------------------------------------------
conn.close()