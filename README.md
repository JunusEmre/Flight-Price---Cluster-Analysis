# ✈️ Traveler Insights Dashboard

## 🔎 Overview  
An interactive Streamlit dashboard for visualizing flight booking data and uncovering travel patterns. This app clusters travelers based on behavior and offers insights into pricing, stop types, duration, and more.

## 👥 User Type Switch  
Inside the app, users can switch between **Traveler View** and **Airline View** for tailored analytics.  
To change the user type, use the dropdown menu located in the **top-left corner** of the sidebar.

- **Traveler View:** Focuses on individual booking patterns, pricing preferences, and travel characteristics.
- **Airline View:** Offers airline-centric insights including average pricing, route popularity, and segmentation behavior.

## 🚀 Launch the App  
Click below to open the dashboard directly in Streamlit:  
👉 [Open in Streamlit](https://flight-price---cluster-analysis-rbreuvhasnhimv2kyv2mtg.streamlit.app/)
⏳ **Note:** The Streamlit app may take a moment to load due to initial setup or data processing. If it seems slow, please be patient — it will launch shortly!

## ⚙️ Requirements  
To run the app locally using the Python file, make sure you have the following packages installed:

```bash
pip install streamlit pandas matplotlib seaborn plotly scikit-learn
```

Or simply use:

```bash
pip install -r requirements.txt
```
## 🔍 Clustering Traveler Behaviors

To better understand flight usage patterns, I applied clustering to group similar types of travelers based on their behavior — such as preferred routes, airlines, or travel frequency.

🧭 **Note:** Price, spending habits, and socioeconomic features were not prioritized in this analysis. Instead, the goal was to uncover travel clusters based on usage patterns — not consumer segmentation.

While the clustering may not produce sharply separated visual groups, it offers insights into which routes and airlines tend to attract similar usage behavior.

🔬 Think of it as a way to group travelers by **how they travel**, not **why they travel**.
