import pandas as pd
from io import BytesIO

def process_files(vat_file, sap_file, pin_file):

    vat_gl = pd.read_excel(vat_file, usecols=["DocumentNo", "Doc. Date", "Amount in DC"])
    sap_tax = pd.read_excel(sap_file, usecols=["BP Name", "DocumentNo"])
    supplier_pin = pd.read_excel(pin_file, usecols=["SUPPLIER", "PIN"])


    merged_df = pd.merge(vat_gl, sap_tax, on="DocumentNo", how="left")

    merged_df = pd.merge(
        merged_df, supplier_pin, left_on="BP Name", right_on="SUPPLIER", how="left"
    )

    matched_df = merged_df[merged_df["BP Name"].notna() & merged_df["PIN"].notna()]
    unmatched_df = merged_df[merged_df["BP Name"].isna() | merged_df["PIN"].isna()]

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        matched_df.to_excel(writer, index=False, sheet_name="Matched")
        unmatched_df.to_excel(writer, index=False, sheet_name="Unmatched")

    output.seek(0)
    return output
