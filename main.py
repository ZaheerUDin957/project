import streamlit as st
import requests
import pandas as pd
import time

import streamlit as st
import base64

# Encode the image in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load the logo image
logo_base64 = get_base64_image("logo.png")


# CSS styling
st.markdown(f"""
    <style>
        .container {{
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: flex-start;
            padding: 20px;
        }}
        .column-left {{
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .column-right {{
            flex: 3;
            display: flex;
            justify-content: flex-start;
            align-items: center;
        }}
        .logo {{
            width: 100px;
        }}
        h1 {{
            font-family: 'Arial', sans-serif;
            font-size: 30px;
            margin-top: 0;
            padding-left: 20px;
        }}
        h1 .cloud {{
            color: black;
        }}
        h1 .solutions {{
            color: #EF4444;
        }}
    </style>
    <div class="container">
        <div class="column-left">
            <img src="data:image/png;base64,{logo_base64}" alt="Cloud Solutions Logo" class="logo">
        </div>
        <div class="column-right">
            <h1>
                <span class="cloud">CLOUD</span> <span class="solutions">SOLUTIONS</span>
            </h1>
        </div>
    </div>
""", unsafe_allow_html=True)

# App title with color
st.markdown(
    "<h1 style='color: #3d5a80;'>Smart-ehr</h1>",
    unsafe_allow_html=True
)

# Sidebar for Patient ID
with st.sidebar:
    st.markdown(
        "<h2 style='color: #293241;'>Select Patient ID</h2>",
        unsafe_allow_html=True
    )
    patient_id = st.selectbox(
        "Patient ID:",
        options=[
            430725, 3365563, 4096834, 1224272, 2279340, 2416237, 2870262, 953132,
            872210, 2009411, 3053583, 2519226, 1141505, 1958758, 898099, 4604718,
            5021273, 2820191, 4937867, 5004093, 876079
        ],
        index=17  # Default to patient_id 2820191
    )

# Main content
st.markdown(
    "<h2 style='color: #3d5a80;'>Chat Interface</h2>",
    unsafe_allow_html=True
)

# Input form
with st.form("chat_form"):
    user_query = st.text_input("Ask a question about the patient:", "")
    submit_button = st.form_submit_button("Submit")

# Process the query with a loader
if submit_button:
    if user_query:
        # Show the loader
        with st.spinner("Fetching data... Please wait"):
            # Simulate delay for better UX
            time.sleep(1)  # Remove this in production

            # Construct the URL with the selected patient_id
            url = f"https://smart-ehr-03-542808340038.us-central1.run.app/api/chatbot?query={user_query}&patient_id={patient_id}"

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()

                    # Check the response type
                    if data.get("type") == 1:
                        st.subheader("Response:")
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #e0fbfc;
                                padding: 15px;
                                border-radius: 10px;
                                border: 1px solid #3d5a80;
                                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                                font-family: Arial, sans-serif;
                                font-size: 16px;
                                color: #3d5a80;
                                line-height: 1.6;
                            ">
                            {data.get("response", "No response provided.")}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    elif data.get("type") == 2:
                        st.subheader("Response:")
                        tabular_data = data.get("response")

                        if tabular_data:  # Check if tabular_data exists
                            # Display vitals_string if available
                            vitals_string = data.get("vitals_string")
                            if vitals_string:
                                st.markdown(
                                    f"""
                                    <div style="
                                        background-color: #e0fbfc;
                                        padding: 15px;
                                        border-radius: 10px;
                                        border: 1px solid #3d5a80;
                                        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                                        font-family: Arial, sans-serif;
                                        font-size: 16px;
                                        color: #3d5a80;
                                        line-height: 1.6;
                                    ">
                                    {vitals_string}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                            # Convert response to DataFrame and display as a styled table
                            if isinstance(tabular_data, dict):
                                df = pd.DataFrame(
                                    tabular_data.items(),
                                    columns=["Parameter", "Value"]
                                )
                                st.markdown(
                                    df.style.set_table_styles(
                                        [
                                            {
                                                "selector": "thead th",
                                                "props": [
                                                    ("background-color", "#3d5a80"),
                                                    ("color", "white"),
                                                    ("font-size", "16px"),
                                                    ("text-align", "center"),
                                                ],
                                            },
                                            {
                                                "selector": "tbody td",
                                                "props": [
                                                    ("background-color", "#f0f8ff"),
                                                    ("color", "#293241"),
                                                    ("text-align", "center"),
                                                    ("padding", "10px"),
                                                ],
                                            },
                                            {
                                                "selector": "tbody tr:nth-child(even) td",
                                                "props": [("background-color", "#eaf4fc")],
                                            },
                                        ]
                                    ).hide(axis="index").to_html(),
                                    unsafe_allow_html=True
                                )
                            else:
                                st.warning("Invalid format for type 2 response.")
                        else:
                            st.warning("Data not found.")

                    elif data.get("type") == 3:
                        st.subheader("Response:")

                        response_data = data.get("response", [])

                        if not response_data:  # Check if response is empty
                            st.warning("Data not found.")
                        else:
                            for idx, item in enumerate(response_data):
                                with st.expander(f"Report {idx + 1}: {item.get('ResultType', 'Unknown')}"):
                                    # Display ReportData in a blue box
                                    st.markdown(
                                        f"""
                                        <div style="
                                            background-color: #3d5a80;
                                            color: white;
                                            padding: 15px;
                                            border-radius: 10px;
                                            font-size: 16px;
                                        ">
                                        <strong>Report Data:</strong><br>
                                        {item.get("ReportData", "No Report Data available.")}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )

                                    # Create a table for other keys
                                    table_data = {
                                        key: value
                                        for key, value in item.items()
                                        if key != "ReportData"
                                    }

                                    if table_data:
                                        df = pd.DataFrame(
                                            table_data.items(),
                                            columns=["Parameter", "Value"]
                                        )
                                        st.markdown(
                                            df.style.set_table_styles(
                                                [
                                                    {
                                                        "selector": "thead th",
                                                        "props": [
                                                            ("background-color", "#3d5a80"),
                                                            ("color", "white"),
                                                            ("font-size", "16px"),
                                                            ("text-align", "center"),
                                                        ],
                                                    },
                                                    {
                                                        "selector": "tbody td",
                                                        "props": [
                                                            ("background-color", "#f0f8ff"),
                                                            ("color", "#293241"),
                                                            ("text-align", "center"),
                                                            ("padding", "10px"),
                                                        ],
                                                    },
                                                    {
                                                        "selector": "tbody tr:nth-child(even) td",
                                                        "props": [("background-color", "#eaf4fc")],
                                                    },
                                                ]
                                            ).hide(axis="index").to_html(),
                                            unsafe_allow_html=True
                                        )
                    else:
                        st.error("Unknown response type.")
                else:
                    st.error(f"Failed to fetch data. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")
