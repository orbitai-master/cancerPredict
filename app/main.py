#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --------------------
# 1. DATA CLEANING
# --------------------


def get_clean_data():
    """Reads and cleans the breast cancer data."""
    # Assuming the data is in a 'data' subfolder relative to the script
    data = pd.read_csv("data/data.csv")

    # Drop unnecessary columns
    data = data.drop(["Unnamed: 32", "id"], axis=1)

    # Map diagnosis to numerical values: Malignant (M) = 1, Benign (B) = 0
    data["diagnosis"] = data["diagnosis"].map({"M": 1, "B": 0})

    return data


# --------------------
# 2. SIDEBAR INPUTS
# --------------------


def add_sidebar():
    """Creates the Streamlit sidebar with input sliders."""
    st.sidebar.markdown(
        "<h1 style='text-align: left; font-size: 50px;'>M E D I C A</h1>",
        unsafe_allow_html=True,
    )
    st.sidebar.header("Cell Nuclei Measurements")

    data = get_clean_data()

    # Define the labels for the sliders and their corresponding column names
    slider_labels = [
        ("Radius (mean)", "radius_mean"),
        ("Texture (mean)", "texture_mean"),
        ("Perimeter (mean)", "perimeter_mean"),
        ("Area (mean)", "area_mean"),
        ("Smoothness (mean)", "smoothness_mean"),
        ("Compactness (mean)", "compactness_mean"),
        ("Concavity (mean)", "concavity_mean"),
        ("Concave points (mean)", "concave points_mean"),
        ("Symmetry (mean)", "symmetry_mean"),
        ("Fractal dimension (mean)", "fractal_dimension_mean"),
        ("Radius (se)", "radius_se"),
        ("Texture (se)", "texture_se"),
        ("Perimeter (se)", "perimeter_se"),
        ("Area (se)", "area_se"),
        ("Smoothness (se)", "smoothness_se"),
        ("Compactness (se)", "compactness_se"),
        ("Concavity (se)", "concavity_se"),
        ("Concave points (se)", "concave points_se"),
        ("Symmetry (se)", "symmetry_se"),
        ("Fractal dimension (se)", "fractal_dimension_se"),
        ("Radius (worst)", "radius_worst"),
        ("Texture (worst)", "texture_worst"),
        ("Perimeter (worst)", "perimeter_worst"),
        ("Area (worst)", "area_worst"),
        ("Smoothness (worst)", "smoothness_worst"),
        ("Compactness (worst)", "compactness_worst"),
        ("Concavity (worst)", "concavity_worst"),
        ("Concave points (worst)", "concave points_worst"),
        ("Symmetry (worst)", "symmetry_worst"),
        ("Fractal dimension (worst)", "fractal_dimension_worst"),
    ]

    input_dict = {}

    for label, key in slider_labels:
        input_dict[key] = st.sidebar.slider(
            label,
            min_value=float(0),
            max_value=float(data[key].max()),
            value=float(data[key].mean()),
        )

    return input_dict


# --------------------
# 3. VISUALIZATION & SCALING
# --------------------


def get_scaled_values(input_dict):
    """Scales user input values (MinMaxScaler style, based on original data) for the radar chart."""
    data = get_clean_data()

    X = data.drop(["diagnosis"], axis=1)

    scaled_dict = {}

    for key, value in input_dict.items():
        # Simple Min-Max scaling based on the original data's range
        max_val = X[key].max()
        min_val = X[key].min()
        scaled_value = (value - min_val) / (max_val - min_val)
        scaled_dict[key] = scaled_value

    return scaled_dict


def get_radar_chart(input_data):
    """Generates the radar chart using Plotly."""
    input_data = get_scaled_values(input_data)

    categories = [
        "Radius",
        "Texture",
        "Perimeter",
        "Area",
        "Smoothness",
        "Compactness",
        "Concavity",
        "Concave Points",
        "Symmetry",
        "Fractal Dimension",
    ]

    fig = go.Figure()

    # Trace for Mean values
    fig.add_trace(
        go.Scatterpolar(
            r=[
                input_data["radius_mean"],
                input_data["texture_mean"],
                input_data["perimeter_mean"],
                input_data["area_mean"],
                input_data["smoothness_mean"],
                input_data["compactness_mean"],
                input_data["concavity_mean"],
                input_data["concave points_mean"],
                input_data["symmetry_mean"],
                input_data["fractal_dimension_mean"],
            ],
            theta=categories,
            fill="toself",
            name="Mean Value",
            line=dict(color="rgba(255, 99, 132, 1)"),  # Custom color for mean
            fillcolor="rgba(255, 99, 132, 0.4)",
        )
    )
    # Trace for Standard Error values
    fig.add_trace(
        go.Scatterpolar(
            r=[
                input_data["radius_se"],
                input_data["texture_se"],
                input_data["perimeter_se"],
                input_data["area_se"],
                input_data["smoothness_se"],
                input_data["compactness_se"],
                input_data["concavity_se"],
                input_data["concave points_se"],
                input_data["symmetry_se"],
                input_data["fractal_dimension_se"],
            ],
            theta=categories,
            fill="toself",
            name="Standard Error",
            line=dict(color="rgba(54, 162, 235, 1)"),  # Custom color for SE
            fillcolor="rgba(54, 162, 235, 0.4)",
        )
    )
    # Trace for Worst values
    fig.add_trace(
        go.Scatterpolar(
            r=[
                input_data["radius_worst"],
                input_data["texture_worst"],
                input_data["perimeter_worst"],
                input_data["area_worst"],
                input_data["smoothness_worst"],
                input_data["compactness_worst"],
                input_data["concavity_worst"],
                input_data["concave points_worst"],
                input_data["symmetry_worst"],
                input_data["fractal_dimension_worst"],
            ],
            theta=categories,
            fill="toself",
            name="Worst Value",
            line=dict(color="rgba(75, 192, 192, 1)"),  # Custom color for worst
            fillcolor="rgba(75, 192, 192, 0.4)",
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Normalized Cell Feature Values (0-1 Scale)",
    )

    return fig


# --------------------
# 4. PREDICTIONS
# --------------------


def add_predictions(input_data):
    """Loads the model and scaler, makes a prediction, and displays the result."""
    # Assuming model and scaler are in a 'model' subfolder relative to the script
    model = pickle.load(open("model/model.pkl", "rb"))
    scaler = pickle.load(open("model/scaler.pkl", "rb"))

    # Convert the dictionary of inputs to a NumPy array for prediction
    input_array = np.array(list(input_data.values())).reshape(1, -1)

    # Scale the input array using the saved scaler
    input_array_scaled = scaler.transform(input_array)

    prediction = model.predict(input_array_scaled)

    st.subheader("Cell Cluster Prediction")
    st.write("The cell cluster is predicted to be:")

    if prediction[0] == 0:
        st.write(
            "<span class='diagnosis benign'>Benign (Non-Cancerous)</span>",
            unsafe_allow_html=True,
        )
    else:
        st.write(
            "<span class='diagnosis malicious'>Malicious (Cancerous)</span>",
            unsafe_allow_html=True,
        )

    # Display probabilities for full transparency
    st.write(
        "Probability of being benign: **{:.2f}%**".format(
            model.predict_proba(input_array_scaled)[0][0] * 100
        )
    )
    st.write(
        "Probability of being malicious: **{:.2f}%**".format(
            model.predict_proba(input_array_scaled)[0][1] * 100
        )
    )

    st.markdown("---")
    st.write(
        "**Disclaimer:** This app is created as part of TechSaksham to assist in predicting breast cancer diagnoses and is not a substitute for professional medical advice."
    )


# --------------------
# 5. NEW FEATURE: RESOURCES
# --------------------


def add_resources():
    """Adds a section for educational resources, blogs, and further reading."""
    st.markdown("---")
    st.header("Educational Resources & Further Reading")
    st.markdown(
        """
        <p style='font-size: 18px;'>
        To understand the **MEDICA** predictions, here are educational resources on breast cancer diagnosis, 
        the significance of cell nuclei measurements, and the role of machine learning in oncology.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Use tabs for clean organization
    resource_tab, technical_tab, blog_tab = st.tabs(
        ["Clinical Context", "Model Technical Details", "Streamlit Blogs & Deployment"]
    )

    with resource_tab:
        st.subheader("Understanding Breast Cancer Diagnosis")
        st.markdown(
            """
            The features measured—like **Radius**, **Perimeter**, and **Concavity**—are derived from a 
            Fine Needle Aspirate (FNA) biopsy. Pathologists use these characteristics of the cell 
            nuclei to determine the **grade** of a tumor. Generally:
            
            * **Malignant (Malicious) tumors** often show **larger** and **more irregular** nuclei, 
                resulting in higher mean values for size and irregularity features (e.g., Radius, Concavity).
            * **Benign tumors** typically have **smaller**, **more regular** cell nuclei.
            """
        )
        st.markdown(
            """
            * [**What's in a Breast Cancer Pathology Report?**](https://www.komen.org/breast-cancer/diagnosis/pathology-reports/contents/) - Understand the clinical terminology.
            * [**Breast Cancer Symptoms and Causes**](https://www.mayoclinic.org/diseases-conditions/breast-cancer/symptoms-causes/syc-20352470) - General information from Mayo Clinic.
            """
        )

    with technical_tab:
        st.subheader("Machine Learning and the Dataset")
        st.markdown(
            """
            This application is built upon the **Wisconsin Breast Cancer (Diagnostic) Dataset**, a key benchmark 
            for binary classification tasks in medical data. The model uses the 30 quantitative morphological features 
            of cell nuclei (like those you adjust in the sidebar) to classify the mass.
            """
        )
        st.markdown(
            """
            * [**UCI Breast Cancer Wisconsin (Diagnostic) Dataset**](https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic) - Official source of the underlying feature data.
            * [**Breast Cancer Diagnosis with Python & KNN**](https://www.youtube.com/watch?v=w5Ie1u4KW3o) - A coding tutorial on training a similar model.
            """
        )

    with blog_tab:
        st.subheader("Building Data Apps with Streamlit")
        st.markdown(
            """
            This predictive tool was built using **Streamlit**, an open-source Python library that transforms data scripts into shareable web applications with minimal effort.
            """
        )
        st.markdown(
            """
            * [**Streamlit Documentation**](https://docs.streamlit.io/) - The official getting started guide.
            * [**Towards Data Science**](https://towardsdatascience.com/) - Explore articles on deploying ML models and building data science apps.
            """
        )


# --------------------
# 6. MAIN FUNCTION
# --------------------


def main():
    """The main function that sets up the Streamlit page."""
    st.set_page_config(
        page_title="Breast Cancer Predictor",
        page_icon=":female-doctor:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Load custom CSS
    try:
        # Assuming the style.css file is in an 'assets' folder
        with open("assets/style.css") as f:
            st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Custom CSS file not found. Ensure 'assets/style.css' exists.")

    input_data = add_sidebar()

    # --- Header Section (Title and Logo) ---
    with st.container():
        col1, col2 = st.columns([4, 1])

        with col1:
            st.title("Breast Cancer Predictor")
            st.write(
                "Please connect this app to your cytology lab to help diagnose breast cancer from your tissue sample. "
                "This app predicts using a machine learning model whether a breast mass is benign or malignant "
                "based on the measurements it receives from your cytosis lab. You can also update the measurements "
                "by hand using the sliders in the sidebar."
            )

        with col2:
            # Assuming the logo image is in an 'assets' folder
            st.image("assets/logo.jpg", width=100)

    # --- Visualization and Prediction Section ---
    col1, col2 = st.columns([4, 1])

    with col1:
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart)
    with col2:
        add_predictions(input_data)

    # --- Resources Section ---
    add_resources()


if __name__ == "__main__":
    main()
