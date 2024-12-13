import streamlit as st
import base64
import streamlit as st
import requests
import pandas as pd
import time

# Encode the image in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load the logo image
logo_base64 = get_base64_image("logo.png")

# Sidebar styling for logo
st.sidebar.markdown(f"""
    <style>
        .sidebar-logo {{
            text-align: left;
            # padding: 10px 0;
        }}
        .sidebar-logo img {{
            width: 80px;
            # margin-left: 10px;
        }}
    </style>
    <div class="sidebar-logo">
        <img src="data:image/png;base64,{logo_base64}" alt="Cloud Solutions Logo">
    </div>
""", unsafe_allow_html=True)

# Main bar styling for text
st.markdown(f"""
    <style>
        .main-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Arial', sans-serif;
        }}
        h1 {{
            font-size: 40px;
            text-align: center;
            margin: 0;
        }}
        h2 {{
            font-size: 20px;
            margin: 0;
        }}
        h2 .cloud {{
            color: black;
        }}
        h2 .solutions {{
            color: #EF4444;
        }}
    </style>
    <div class="main-container">
        <h2>
            <span class="cloud">CLOUD</span> <span class="solutions">SOLUTIONS</span>
        </h2>
    </div>
""", unsafe_allow_html=True)

# App title with color
st.markdown(
    "<h1 style='color: #EF4444;'>Smart-EHR Chat Interface</h1>",
    unsafe_allow_html=True
)


# Sidebar for Patient ID
with st.sidebar:
    st.markdown(
        "<h2 style='color: #EF4444;'>Select Patient ID</h2>",
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

# Input form
with st.form("chat_form"):
    st.markdown('<p style="color: #EF4444; font-size: 20px;">Ask a question about the patient:</p>', unsafe_allow_html=True)
    user_query = st.text_input("Ask a question about the patient", key="user_query")
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
                        st.markdown("<p style='color: #EF4444; font-size: 20px; font-weight: bold '>Response</p>", unsafe_allow_html=True)
                        st.markdown(f"{data.get('response', 'No response provided.')}")

                    elif data.get("type") == 2:
                        st.markdown("<p style='color: #EF4444; font-size: 20px; font-weight: bold '>Response</p>", unsafe_allow_html=True)
                        tabular_data = data.get("response")

                        if tabular_data:  # Check if tabular_data exists
                            # Display vitals_string if available
                            vitals_string = data.get("vitals_string")
                            if vitals_string:
                                st.markdown(vitals_string)

                            # Convert response to DataFrame and display as a table
                            if isinstance(tabular_data, dict):
                                df = pd.DataFrame(
                                    tabular_data.items(),
                                    columns=["Parameter", "Value"]
                                )
                                st.markdown(df.to_html(), unsafe_allow_html=True)
                            else:
                                st.warning("Invalid format for type 2 response.")
                        else:
                            st.warning("Data not found.")

                    elif data.get("type") == 3:
                        st.markdown("<p style='color: #EF4444; font-size: 20px; font-weight: bold '>Response</p>", unsafe_allow_html=True)

                        response_data = data.get("response", [])

                        if not response_data:  # Check if response is empty
                            st.warning("Data not found.")
                        else:
                            for idx, item in enumerate(response_data):
                                with st.expander(f"Report {idx + 1}: {item.get('ResultType', 'Unknown')}"):
                                    # Display ReportData
                                    st.markdown(f"<strong>Report Data:</strong><br>{item.get('ReportData', 'No Report Data available.')}")

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
                                        st.markdown(df.to_html(), unsafe_allow_html=True)
                    else:
                        st.error("Unknown response type.")
                else:
                    st.error(f"Failed to fetch data. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")
