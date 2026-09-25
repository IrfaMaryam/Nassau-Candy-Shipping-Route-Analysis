import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Nassau Candy Shipping Route Efficiency",
    layout="wide"
)

st.title("Nassau Candy Shipping Route Efficiency Dashboard")

st.write(
    "Analysis of shipping lead time, route volume, geographic patterns, "
    "and ship mode performance for Nassau Candy Distributor."
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("Nassau_Candy_Cleaned.csv")

# Dates in the CSV are in DD-MM-YYYY format
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    format="%d-%m-%Y"
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Dashboard Filters")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

regions = sorted(df["Region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

states = sorted(df["State/Province"].dropna().unique())

selected_states = st.sidebar.multiselect(
    "State",
    states,
    default=states
)

ship_modes = sorted(df["Ship Mode"].dropna().unique())

selected_ship_modes = st.sidebar.multiselect(
    "Ship Mode",
    ship_modes,
    default=ship_modes
)

max_lead_time = int(df["Shipping Lead Time"].max())

lead_time_threshold = st.sidebar.slider(
    "Maximum Lead Time (Days)",
    min_value=0,
    max_value=max_lead_time,
    value=max_lead_time
)

# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= date_range[0])
        &
        (filtered_df["Order Date"].dt.date <= date_range[1])
    ]

filtered_df = filtered_df[
    filtered_df["Region"].isin(selected_regions)
]

filtered_df = filtered_df[
    filtered_df["State/Province"].isin(selected_states)
]

filtered_df = filtered_df[
    filtered_df["Ship Mode"].isin(selected_ship_modes)
]

filtered_df = filtered_df[
    filtered_df["Shipping Lead Time"] <= lead_time_threshold
]

# =========================================================
# ROUTE EFFICIENCY OVERVIEW
# =========================================================

st.subheader("Route Efficiency Overview")

route_count = filtered_df["Route"].nunique()

if len(filtered_df) > 0:
    average_lead_time = filtered_df["Shipping Lead Time"].mean()
else:
    average_lead_time = 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Shipments",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Shipping Lead Time",
        f"{average_lead_time:.2f} days"
    )

with col3:
    st.metric(
        "Total Routes",
        route_count
    )

# =========================================================
# CHART 1
# =========================================================

st.subheader("1. Average Shipping Lead Time by Region")

region_lead_time = (
    filtered_df
    .groupby("Region")["Shipping Lead Time"]
    .mean()
    .reset_index()
)

fig_region_lead = px.bar(
    region_lead_time,
    x="Region",
    y="Shipping Lead Time",
    title="Average Shipping Lead Time by Region",
    labels={
        "Shipping Lead Time": "Average Lead Time (Days)"
    }
)

st.plotly_chart(
    fig_region_lead,
    use_container_width=True
)

# =========================================================
# CHART 2
# =========================================================

st.subheader("2. Total Shipments by Region")

region_shipments = (
    filtered_df
    .groupby("Region")
    .size()
    .reset_index(name="Total Shipments")
)

fig_region_shipments = px.bar(
    region_shipments,
    x="Region",
    y="Total Shipments",
    title="Total Shipments by Region",
    labels={
        "Total Shipments": "Number of Shipments"
    }
)

st.plotly_chart(
    fig_region_shipments,
    use_container_width=True
)

# =========================================================
# CHART 3
# =========================================================

st.subheader("3. Average Shipping Lead Time by Ship Mode")

ship_mode_lead_time = (
    filtered_df
    .groupby("Ship Mode")["Shipping Lead Time"]
    .mean()
    .reset_index()
)

fig_ship_mode_lead = px.bar(
    ship_mode_lead_time,
    x="Ship Mode",
    y="Shipping Lead Time",
    title="Average Shipping Lead Time by Ship Mode",
    labels={
        "Shipping Lead Time": "Average Lead Time (Days)"
    }
)

st.plotly_chart(
    fig_ship_mode_lead,
    use_container_width=True
)

# =========================================================
# CHART 4
# =========================================================

st.subheader("4. Total Shipments by Ship Mode")

ship_mode_shipments = (
    filtered_df
    .groupby("Ship Mode")
    .size()
    .reset_index(name="Total Shipments")
)

fig_ship_mode_shipments = px.bar(
    ship_mode_shipments,
    x="Ship Mode",
    y="Total Shipments",
    title="Total Shipments by Ship Mode",
    labels={
        "Total Shipments": "Number of Shipments"
    }
)

st.plotly_chart(
    fig_ship_mode_shipments,
    use_container_width=True
)

# =========================================================
# CHART 5
# =========================================================

st.subheader("5. Top 10 Routes by Shipment Volume")

top_routes = (
    filtered_df
    .groupby("Route")
    .size()
    .reset_index(name="Total Shipments")
    .sort_values(
        "Total Shipments",
        ascending=False
    )
    .head(10)
)

fig_top_routes = px.bar(
    top_routes,
    x="Route",
    y="Total Shipments",
    title="Top 10 Routes by Shipment Volume",
    labels={
        "Total Shipments": "Number of Shipments"
    }
)

st.plotly_chart(
    fig_top_routes,
    use_container_width=True
)

# =========================================================
# CHART 6
# =========================================================

st.subheader("6. Average Shipping Lead Time by State")

state_lead_time = (
    filtered_df
    .groupby("State/Province")["Shipping Lead Time"]
    .mean()
    .reset_index()
    .sort_values(
        "Shipping Lead Time",
        ascending=True
    )
)

fig_state_lead = px.bar(
    state_lead_time,
    x="Shipping Lead Time",
    y="State/Province",
    orientation="h",
    title="Average Shipping Lead Time by State",
    labels={
        "Shipping Lead Time": "Average Lead Time (Days)",
        "State/Province": "State"
    }
)

st.plotly_chart(
    fig_state_lead,
    use_container_width=True
)

# =========================================================
# GEOGRAPHIC SHIPPING OVERVIEW
# =========================================================

st.subheader("7. Geographic Shipping Overview")

st.info(
    "The dataset does not contain factory-location or latitude/longitude "
    "fields. Therefore, this geographic view uses available U.S. "
    "state-level customer information and is not a factory-to-customer map."
)

state_codes = {
    "Alabama": "AL",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC"
}

us_data = filtered_df[
    filtered_df["Country/Region"] == "United States"
].copy()

us_data["State Code"] = (
    us_data["State/Province"].map(state_codes)
)

us_state_data = (
    us_data
    .dropna(subset=["State Code"])
    .groupby(
        ["State/Province", "State Code"]
    )["Shipping Lead Time"]
    .mean()
    .reset_index()
)

fig_map = px.choropleth(
    us_state_data,
    locations="State Code",
    locationmode="USA-states",
    color="Shipping Lead Time",
    scope="usa",
    title="Average Shipping Lead Time by U.S. State",
    hover_name="State/Province",
    color_continuous_scale="Blues",
    labels={
        "Shipping Lead Time": "Average Lead Time (Days)"
    }
)

st.plotly_chart(
    fig_map,
    use_container_width=True
)

# =========================================================
# ROUTE EFFICIENCY BENCHMARKING
# =========================================================

st.subheader("8. Route Efficiency Benchmarking")

route_summary = (
    filtered_df
    .groupby("Route")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Average_Lead_Time=("Shipping Lead Time", "mean"),
        Lead_Time_Variability=("Shipping Lead Time", "std")
    )
    .reset_index()
)

route_summary["Lead_Time_Variability"] = (
    route_summary["Lead_Time_Variability"]
    .fillna(0)
)

if len(route_summary) > 1:

    min_route_time = (
        route_summary["Average_Lead_Time"].min()
    )

    max_route_time = (
        route_summary["Average_Lead_Time"].max()
    )

    if max_route_time != min_route_time:

        route_summary["Route Efficiency Score"] = (
            100
            -
            (
                (
                    route_summary["Average_Lead_Time"]
                    - min_route_time
                )
                /
                (
                    max_route_time
                    - min_route_time
                )
            )
            * 100
        )

    else:
        route_summary["Route Efficiency Score"] = 100

else:
    route_summary["Route Efficiency Score"] = 100

route_summary["Route Efficiency Score"] = (
    route_summary["Route Efficiency Score"]
    .round(2)
)

benchmark_col1, benchmark_col2 = st.columns(2)

with benchmark_col1:

    st.write("Top 10 Most Efficient Routes")

    top_efficient = (
        route_summary
        .sort_values(
            "Average_Lead_Time",
            ascending=True
        )
        .head(10)
    )

    st.dataframe(
        top_efficient[
            [
                "Route",
                "Total_Shipments",
                "Average_Lead_Time",
                "Lead_Time_Variability",
                "Route Efficiency Score"
            ]
        ],
        use_container_width=True
    )

with benchmark_col2:

    st.write("Bottom 10 Least Efficient Routes")

    bottom_efficient = (
        route_summary
        .sort_values(
            "Average_Lead_Time",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        bottom_efficient[
            [
                "Route",
                "Total_Shipments",
                "Average_Lead_Time",
                "Lead_Time_Variability",
                "Route Efficiency Score"
            ]
        ],
        use_container_width=True
    )

# =========================================================
# DELAY FREQUENCY
# =========================================================

st.subheader("9. Delay Frequency")

delay_threshold = st.number_input(
    "Delay Threshold (Days)",
    min_value=0,
    max_value=max_lead_time,
    value=int(df["Shipping Lead Time"].median()),
    step=1
)

if len(filtered_df) > 0:

    delayed_shipments = (
        filtered_df["Shipping Lead Time"]
        > delay_threshold
    ).sum()

    delay_frequency = (
        delayed_shipments
        / len(filtered_df)
    ) * 100

else:

    delayed_shipments = 0
    delay_frequency = 0

delay_col1, delay_col2 = st.columns(2)

with delay_col1:
    st.metric(
        "Shipments Above Threshold",
        delayed_shipments
    )

with delay_col2:
    st.metric(
        "Delay Frequency",
        f"{delay_frequency:.2f}%"
    )

# =========================================================
# ROUTE DRILL-DOWN
# =========================================================

st.subheader("10. Route Drill-Down")

available_routes = sorted(
    filtered_df["Route"]
    .dropna()
    .unique()
)

if len(available_routes) > 0:

    selected_route = st.selectbox(
        "Select a Route",
        available_routes
    )

    selected_route_data = filtered_df[
        filtered_df["Route"] == selected_route
    ]

    route_shipments = len(selected_route_data)

    route_average = (
        selected_route_data[
            "Shipping Lead Time"
        ].mean()
    )

    route_std = (
        selected_route_data[
            "Shipping Lead Time"
        ].std()
    )

    if pd.isna(route_std):
        route_std = 0

    route_col1, route_col2, route_col3 = st.columns(3)

    with route_col1:
        st.metric(
            "Route Shipments",
            route_shipments
        )

    with route_col2:
        st.metric(
            "Average Lead Time",
            f"{route_average:.2f} days"
        )

    with route_col3:
        st.metric(
            "Lead Time Variability",
            f"{route_std:.2f} days"
        )

    route_mode_data = (
        selected_route_data
        .groupby("Ship Mode")
        .size()
        .reset_index(name="Shipments")
    )

    fig_route_mode = px.bar(
        route_mode_data,
        x="Ship Mode",
        y="Shipments",
        title=f"Shipments by Ship Mode — {selected_route}",
        labels={
            "Shipments": "Number of Shipments"
        }
    )

    st.plotly_chart(
        fig_route_mode,
        use_container_width=True
    )

else:
    st.warning(
        "No routes are available for the selected filters."
    )

# =========================================================
# DATASET PREVIEW
# =========================================================

st.subheader("Dataset Preview")

st.dataframe(
    filtered_df.head(10),
    use_container_width=True
)

# =========================================================
# DATA QUALITY NOTE
# =========================================================

st.subheader("Data Quality Note")

st.write(
    "The calculated shipping lead times in this dataset are unusually "
    "large for normal shipping operations. These values were calculated "
    "directly from the provided Order Date and Ship Date fields and were "
    "not removed because they are positive date differences. They should "
    "be treated as observed dataset values and investigated before being "
    "used as real-world delivery benchmarks."
)