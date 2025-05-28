import streamlit as st
import requests
import json

# --- Page Setup ---
st.set_page_config(page_title="📊 MCP JSON Analyzer", layout="wide")
st.title("📊 MCP JSON Analyzer")

# --- Sidebar Config ---
st.sidebar.header("🔧 Server Configuration")
SERVER_URL = st.sidebar.text_input("MCP Tool URL", "http://localhost:8000/tool/analyze-data")
st.sidebar.markdown("---")
st.sidebar.info("Your JSON should be a list or a dict of lists of numbers.")

# --- Upload Section ---
st.markdown("### 📁 Upload a JSON File")
uploaded_file = st.file_uploader("Choose a .json file", type="json")

# --- Operation Selection in Main Area ---
st.markdown("### 🧮 Choose Operations to Perform")
operation_choices = st.multiselect(
    "Select one or more operations:",
    ["sum", "mean", "average", "median", "min", "max"],
    default=["mean", "max"]
)

if uploaded_file:
    try:
        file_content = uploaded_file.read().decode("utf-8")
        data = json.loads(file_content)
        st.success("✅ JSON loaded!")
        with st.expander("📄 Preview Uploaded JSON", expanded=False):
            st.json(data)

        if st.button("🚀 Run Analysis", use_container_width=True):
            with st.spinner("Analyzing data..."):
                response = requests.post(SERVER_URL, json={"data": data})
                if response.ok:
                    result = response.json()
                    if result.get("status") == "success":
                        raw_result = result["result"]
                        st.success("✅ Analysis complete!")

                        st.markdown("### 📈 Filtered Results")
                        if isinstance(raw_result, dict) and all(isinstance(v, dict) for v in raw_result.values()):
                            for key, stats in raw_result.items():
                                filtered = {k: v for k, v in stats.items() if k in operation_choices}
                                with st.expander(f"🔹 {key}"):
                                    st.json(filtered)
                        else:
                            filtered = {k: v for k, v in raw_result.items() if k in operation_choices}
                            st.json(filtered)
                    else:
                        st.error(f"❌ Error: {result.get('error')}")
                else:
                    st.error(f"🚨 Server error: HTTP {response.status_code}")
    except json.JSONDecodeError:
        st.error("⚠️ Invalid JSON format.")
    except Exception as e:
        st.error(f"🚨 Unexpected error: {e}")
else:
    st.info("📥 Please upload a JSON file to start.")
