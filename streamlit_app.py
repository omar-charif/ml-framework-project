import streamlit as st

from ml_framework_project.main import (
    diamonds_classification_pipeline_df,
    diamonds_regression_pipeline_df,
)

st.title("Diamonds Pipeline Analysis")

# Text input for file path
file_path = st.text_input(
    "Enter file path",
    placeholder="e.g., /path/to/diamonds.csv",
)

# Radio button to choose between regression and classification
pipeline_type = st.radio(
    "Select pipeline type:",
    ["Regression", "Classification"],
    horizontal=True,
)

# Button to run the pipeline
if st.button("Run Pipeline"):
    if not file_path:
        st.error("Please enter a file path")
    else:
        try:
            with st.spinner("Processing data..."):
                if pipeline_type == "Regression":
                    df = diamonds_regression_pipeline_df(file_path)
                    st.success("Regression pipeline completed!")
                else:
                    df = diamonds_classification_pipeline_df(file_path)
                    st.success("Classification pipeline completed!")

            # Display the dataframe as a table
            st.subheader("Processed Data")
            st.dataframe(df, use_container_width=True)

            # Display summary statistics
            st.subheader("Summary Statistics")
            st.write(f"Number of rows: {df.shape[0]}")
            st.write(f"Number of columns: {df.shape[1]}")

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
