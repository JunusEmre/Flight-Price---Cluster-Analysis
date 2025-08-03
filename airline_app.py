import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os

# === Load Data ===
try:
    df_seg = pd.read_csv("cleaned_segmentation_data.csv")
    components = np.load("pca_components.npy")
except FileNotFoundError:
    st.error("🚫 Segmentation data files not found. Please run the preprocessing script first.")
    st.stop()

# Optional: Load airline data
airline_file = "airline_performance_table.csv"
airline_available = os.path.exists(airline_file)
if airline_available:
    airline_perf = pd.read_csv(airline_file)

# === Rename Clusters ===
cluster_map = {
    0: "🧳 Budget Nomads",
    1: "👑 Elite Gliders",
    2: "🌍 Balanced Explorers",
    3: "⚡️ Early Hustlers"
}
df_seg["Cluster Name"] = df_seg["cluster"].map(cluster_map)

color_map = {
    "🧳 Budget Nomads": "#1f77b4",
    "👑 Elite Gliders": "#ff7f0e",
    "🌍 Balanced Explorers": "#2ca02c",
    "⚡️ Early Hustlers": "#d62728"
}

# === Sidebar Choice ===
st.sidebar.title("🛫 Perspective")
mode = st.sidebar.radio("Choose your view:", ["Traveler", "Airline Analyst"])

# === TRAVELER MODE ===
if mode == "Traveler":
    st.title("🌍 Traveler Insights Dashboard")

    st.markdown("### 📊 Cluster Averages")
    st.dataframe(df_seg.groupby("Cluster Name").mean(numeric_only=True).round(2))

    st.markdown("### 🔎 Sample Profiles")
    sample_profiles = df_seg.groupby("Cluster Name").apply(lambda x: x.head(3)).reset_index(drop=True)
    st.dataframe(sample_profiles[["Cluster Name", "price", "duration", "class_enc", "departure_time_enc", "stops"]])

    st.markdown("### 🎨 Visual Cluster Distribution")
    fig, ax = plt.subplots()
    for name in df_seg["Cluster Name"].unique():
        mask = df_seg["Cluster Name"] == name
        ax.scatter(components[mask, 0], components[mask, 1], label=name, color=color_map[name])
    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    ax.legend()
    st.pyplot(fig)

    st.markdown("### 📡 Cluster Radar Profiles")
    radar_data = df_seg.groupby("Cluster Name").mean(numeric_only=True)[["price", "duration", "stops"]]
    radar_data["Cluster Name"] = radar_data.index
    radar_melted = pd.melt(radar_data, id_vars="Cluster Name", var_name="Attribute", value_name="Value")
    fig = px.line_polar(radar_melted, r="Value", theta="Attribute", color="Cluster Name", line_close=True)
    fig.update_traces(fill="toself")
    st.plotly_chart(fig)

        # 🧹 Clean & filter relevant stop values
    df_seg["stops"] = pd.to_numeric(df_seg["stops"], errors="coerce").astype(int)
    df_filtered = df_seg[df_seg["stops"].isin([0, 1, 2])]

    # 📊 Group and calculate average price
    price_by_stops = df_filtered.groupby("stops")["price"].mean().reset_index()
    price_by_stops["Stop Type"] = price_by_stops["stops"].map({0: "Non-stop", 1: "1 Stop", 2: "2 Stops"})

    # 🎨 Plot chart
    fig = px.bar(price_by_stops, x="Stop Type", y="price",
                color="Stop Type", title="💰 Avg Flight Price by Stop Count",
                labels={"price": "Avg Price ($)", "Stop Type": "Flight Type"},
                color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"])

    st.plotly_chart(fig)

# === AIRLINE ANALYST MODE ===
elif mode == "Airline Analyst":
    st.title("📊 Airline Strategy Dashboard")

    try:
        df_analysis = pd.read_csv("airline_analysis_dataset.csv")

        # Route Profitability
        st.markdown("### 💸 Top Profitable Routes")
        route_profit = df_analysis.groupby(["source_city", "destination_city"]).agg(
        avg_price=("price", "mean"),
        total_revenue=("price", "sum"),
        avg_duration=("duration", "mean"),
        num_flights=("airline", "count")
        ).reset_index().sort_values("total_revenue", ascending=False)

        # Round numeric columns
        route_profit = route_profit.round(2)
        st.dataframe(route_profit.head(10))

        # Time of Day Pricing
        time_labels = {
        0 : "Early Morning", 1: "Morning", 2: "Afternoon",
        3: "Evening", 4: "Night", 5: "Late Night"
        }
        df_analysis['departure_label'] = df_analysis['departure_time'].map(time_labels)
        st.markdown("### 🕒 Departure Time vs Price")
        fig = px.box(df_analysis, x="departure_label", y="price",
             labels={"departure_label": "Time of Day", "price": "Price"},
             title="Pricing by Departure Time")

        st.plotly_chart(fig)

        # Class Comparison
        st.markdown("### 🎫 Economy vs Business Pricing")
        class_avg = df_analysis.groupby("class")["price"].mean().reset_index()
        class_avg["Class"] = class_avg["class"].map({0: "Economy", 1: "Business"})
        fig = px.bar(class_avg, x="Class", y="price", color="Class",
                     title="Average Price per Travel Class")
        st.plotly_chart(fig)

        # Price vs Days Left
        st.markdown("### ⏳ Price Trend by Days Left")
        fig = px.scatter(df_analysis, x="days_left", y="price", trendline="lowess",
                         title="Price vs Booking Lead Time")
        st.plotly_chart(fig)

        #  Flight Number of Stop
        # ✅ Clean and prepare stops
        df_analysis["stops"] = pd.to_numeric(df_analysis["stops"], errors="coerce")
        df_analysis["stops"] = df_analysis["stops"].round(0)
        df_analysis = df_analysis[df_analysis["stops"].isin([0, 1, 2])]
        df_analysis["stops"] = df_analysis["stops"].astype("Int64")
        # ✅ Count number of flights per stop count
        stop_counts = df_analysis["stops"].value_counts().sort_index().reset_index()
        stop_counts.columns = ["stops", "Number of Flights"]
        # 📊 Bar Chart
        st.markdown("### ✈️ Number of Flights by Stop Count")
        fig = px.bar(
            stop_counts,
            x="stops",
            y="Number of Flights",
            labels={"stops": "Number of Stops"},
            title="Number of Flights by Stop Count",
            color="stops",  # Optional: adds visual distinction
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(text=stop_counts["Number of Flights"], textposition="outside")
        fig.update_layout(
            xaxis_type="category",  # 👈 Keep x-axis clean
            showlegend=False
        )
        st.plotly_chart(fig)

        #Price Distribution by Airline
        st.markdown("### 💸 Price Distribution by Airline")
        fig = px.box(df_analysis, x="airline", y="price",
                    color="departure_label",
                    labels={"airline": "Airline", "price": "Ticket Price", "departure_label": "Time of Day"},
                    title="Price Distribution Across Airlines by Departure Time")
        st.plotly_chart(fig)

        # Popular Routes Heatmap
        # Create readable route column
        df_analysis['route'] = df_analysis['source_city'] + " → " + df_analysis['destination_city']
        # Count most frequent routes
        route_counts = df_analysis['route'].value_counts().reset_index()
        route_counts.columns = ['Route', 'Count']
        # Sort and select top 15
        top_routes = route_counts.head(15)
        # Plot bar chart with Plotly
        import plotly.express as px
        st.markdown("### 🧭 Top 15 Most Frequent Routes")
        fig = px.bar(top_routes, x='Route', y='Count',
                 title="Top 15 Most Frequent Flight Routes",
                 labels={'Route': 'Route', 'Count': 'Number of Flights'},
                 color='Count', color_continuous_scale='magma')
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig)

    except FileNotFoundError:
        st.warning("🚫 airline_analysis_dataset.csv not found. Please run the preprocessing script.")

# === Footer ===
st.markdown("---")
st.markdown("🛠 Built by Yunus · ✨ Powered by clusters and curiosity")

