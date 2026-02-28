"""
Example code loaded with Snowflake Streamlit app.
"""

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

# Get the current credentials
session = get_active_session()

# Use an interactive slider to get user input
hifives_val = st.slider(
  "Number of high-fives in Q3",
  min_value=0,
  max_value=90,
  value=60,
  help="Use this to enter the number of high-fives you gave in Q3",
)

#  Create an example dataframe
#  Note: this is just some dummy data, but you can easily connect to your Snowflake data
#  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
created_dataframe = session.create_dataframe(
  [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
  schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
)

# Execute the query and convert it into a Pandas dataframe
queried_data = created_dataframe.to_pandas()

# Create a simple bar chart
# See docs.streamlit.io for more types of charts
st.subheader("Number of high-fives")
st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

st.subheader("Underlying data")
st.dataframe(queried_data, use_container_width=True)

"""
Example code connecting to with Snowflake tables from Streamlit app.
"""

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(f"Example Streamlit App {st.__version__}")
st.write(
  """Now pulling data from Snowflake's sample data:
  **SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER**"""
)

# Get the current credentials
session = get_active_session()

# Simple query: just grab a few rows
df = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER").limit(10)

# Convert to Pandas for Streamlit
pdf = df.to_pandas()

# Display a chart (e.g. customer balance by name)
st.subheader("Customer balances (sample)")
st.bar_chart(data=pdf, x="C_NAME", y="C_ACCTBAL")

st.subheader("Underlying data")
st.dataframe(pdf, use_container_width=True)