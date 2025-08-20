import streamlit as st
from backend import process_files

st.set_page_config(page_title="VAT GL VLOOKUP Tool", layout="centered")

# --- Custom CSS for Button ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        font-weight: bold;
        background-color: #2E86C1;
        color: white;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #1B4F72;
        transform: scale(1.05);
        background-image: url('https://cdn-icons-png.flaticon.com/512/992/992700.png'); /* hover icon */
        background-repeat: no-repeat;
        background-position: 95% center;
        background-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.title("📊 TAX ANALYSIS TOOL")
st.write("Upload VAT GL, SAP Tax Report, and Supplier PIN list to match the records.")

# --- File Uploads ---
vat_file = st.file_uploader("Upload VAT GL file", type=["xls", "xlsx"])
sap_file = st.file_uploader("Upload SAP Tax Report", type=["xls", "xlsx"])
pin_file = st.file_uploader("Upload Supplier PIN list", type=["xls", "xlsx"])

# --- Execute Button ---
if st.button("EXCCUTE"):
    if vat_file and sap_file and pin_file:
        with st.spinner("Processing... Please wait"):
            result = process_files(vat_file, sap_file, pin_file)
        st.success("✅ Processing complete!")

        st.download_button(
            label="📥 Download Result Excel",
            data=result,
            file_name="Matched.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Please upload all three files before running.")
