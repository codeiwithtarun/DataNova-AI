import streamlit as st
import pandas as pd


from src.components.sidebar import render_sidebar
# from src.components.navbar import render_navbar
from src.components.uploader import upload_dataset
from src.components.data_preview import show_dataset_preview
from src.utils.file_handler import load_dataset
from src.cleaning.missing_values import (
    remove_missing_values,
    fill_missing_values,
    missing_values_summary
)

from src.cleaning.duplicates import (
    remove_duplicates,
    count_duplicates
)

from src.components.download_center import download_dataset
from src.visualization.histogram import show_histogram

from src.visualization.boxplot import show_boxplot

from src.visualization.heatmaps import show_heatmap

from src.visualization.scatterplots import show_scatter_plot

from src.visualization.correlation import (
    show_correlation_matrix
)
from src.ai_engine.smart_suggestions import smart_suggestions
from src.reports.analytics_report import generate_report
from src.cleaning.auto_cleaner import auto_clean_dataset
from src.auth.auth import *
if "logged_in" not in st.session_state:
    st.session_state.username = ""

    st.session_state.logged_in = False
from src.auth.database import (create_user,
                               login_user,
                               save_history,
                               get_history,
                               save_cleaned_dataset,
                               get_cleaned_datasets
                               )
# from src.ai_engine.chatbot import ask_ai
import matplotlib.pyplot as plt
import seaborn as sns
from src.eda.eda_analysis import show_eda_analysis


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(

    page_title="DataNova AI",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
<style>  

/* MOBILE RESPONSIVE */

@media (max-width: 768px) {

    section[data-testid="stSidebar"] {

        width: 220px !important;

        min-width: 220px !important;

        max-width: 220px !important;
    }

    section[data-testid="stSidebar"] > div {

        width: 220px !important;
    }

    .main .block-container {

        padding-left: 1rem !important;

        padding-right: 1rem !important;

        max-width: 100% !important;
    }

    .main-title {

        font-size: 34px !important;
    }

    .sub-title {

        font-size: 16px !important;
    }

    .feature-card {

        padding: 18px !important;

        border-radius: 16px !important;
    }

    .stButton button {

        font-size: 14px !important;

        padding: 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================
# CUSTOM UI DESIGN + ANIMATIONS
# =========================================

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background: linear-gradient(
        135deg,
        #f8fbff,
        #eef4ff,
        #f5f7ff
    );
}

/* Premium Sidebar */
section[data-testid="stSidebar"] > div:first-child {

    background: linear-gradient(
        180deg,
        #1e3a8a,
        #2563eb,
        #60a5fa
    );

    border-radius: 0px 20px 20px 0px;

    box-shadow: 0 0 25px rgba(0,0,0,0.15);
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: 500;
}

/* Main Title Animation */
.main-title {
    font-size: 55px;
    font-weight: bold;
    text-align: center;
   
    background: linear-gradient(90deg,#2563eb,#9333ea,#06b6d4);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;

   
}

/* Subtitle */
.sub-title {
    text-align: center;
    font-size: 22px;
    color: #475569;
    margin-bottom: 50px;
}

/* Feature Cards */
.feature-card {

    background: rgba(255,255,255,0.75);

    backdrop-filter: blur(12px);

    border-radius: 24px;

    padding: 30px;

    margin-bottom: 25px;

    box-shadow:
        0 8px 32px rgba(31,38,135,0.12);

    transition: 0.4s ease;
}

/* Hover Effect */
.feature-card:hover {

    transform: translateY(-8px);

    box-shadow:
        0 15px 40px rgba(37,99,235,0.25);
}

/* Hover Effect */
.feature-card:hover {
    transform: scale(1.03);
    box-shadow: 0px 8px 30px rgba(0,0,0,0.2);
}

/* Buttons */
.stButton > button {

    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );

    color: white;

    border: none;

    border-radius: 14px;

    padding: 12px 28px;

    font-size: 16px;

    font-weight: 600;

    transition: 0.3s ease;
}

/* Button Hover */
.stButton > button:hover {

    transform: scale(1.05);

    box-shadow:
        0 10px 25px rgba(37,99,235,0.35);
}

/* Button Hover */
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(
        to right,
        #43e97b,
        #38f9d7
    );
}

/* Upload Box */
[data-testid="stFileUploader"] {
    border: 3px dashed #4facfe;
    border-radius: 20px;
    padding: 20px;
    background: white;
}

/* Fade Animation */
@keyframes fadeUp {

    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

.feature-card {
    animation: fadeUp 0.7s ease;
}
/* Status Box */
[data-testid="stSidebar"] .stMarkdown:nth-of-type(2) {

    background: rgba(15, 23, 42, 0.75);

    padding: 18px;

    border-radius: 18px;

    margin-top: 25px;

    box-shadow: 0 8px 20px rgba(0,0,0,0.25);

    backdrop-filter: blur(10px);
}

/* Authentication Box */

[data-testid="stSidebar"] details {

    background: rgba(15, 23, 42, 0.75);

    padding: 12px;

    border-radius: 18px;

    margin-top: 20px;

    box-shadow: 0 8px 20px rgba(0,0,0,0.25);

    backdrop-filter: blur(10px);
}

/* ONE BIG NAVIGATION BOX */
[data-testid="stSidebar"] .stRadio {

    background: rgba(15, 23, 42, 0.45);

    padding: 18px;

    border-radius: 20px;

    margin-top: 10px;

    margin-bottom: 20px;

    backdrop-filter: blur(10px);

    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}
/* Navigation Hover */
[data-testid="stSidebar"] .stRadio label:hover {

    transform: translateX(5px);

    transition: 0.3s ease;
}


   
/* Sidebar Info Box */
.sidebar-info-box {
    background: rgba(10, 15, 40, 0.75);
    padding: 20px;
    border-radius: 22px;
    margin-top: 25px;
    color: white;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    }


</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# NAVBAR
# ---------------------------------------------------

# render_navbar()


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

selected_option = render_sidebar()


# ---------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------

# ---------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------

with st.sidebar.expander("🔐 Authentication"):

    auth_option = st.selectbox(
        "Choose Option",
        ["Login", "Signup"]
    )

    # -----------------------------------------
    # SIGNUP
    # -----------------------------------------

    if auth_option == "Signup":

        new_username = st.text_input(
            "Username"
        )

        new_password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Create Account"):

            success = create_user(
                new_username,
                new_password
            )

            if success:

                st.success(
                    "Account Created Successfully"
                )

            else:

                st.error(
                    "Username Already Exists"
                )

    # -----------------------------------------
    # LOGIN
    # -----------------------------------------

    if auth_option == "Login":

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            success = login_user(
                username,
                password
            )

            if success:

                st.session_state.logged_in = True
                st.session_state.username = username

                save_history(
                    username,
                    "User Logged In"
                )

                st.success(
                    "Login Successful"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid Username or Password"
                )

            # =========================================
# USER DASHBOARD
# =========================================

# =========================================
# USER DASHBOARD
# =========================================

# =========================================
# USER DASHBOARD
# =========================================

if st.session_state.logged_in:

    st.sidebar.markdown("---")

    with st.sidebar.expander("👤 User Dashboard"):

        st.success(
            f"Logged in as:\n\n{st.session_state.username}"
        )

        # ---------------------------------
        # LOGIN HISTORY
        # ---------------------------------

        history = get_history(
            st.session_state.username
        )

        login_count = len(history)

        st.subheader("📜 User History")

        st.write(
            f"User Logged In {login_count} Times"
        )

        # ---------------------------------
        # RECENT CLEANED DATASETS
        # ---------------------------------

        datasets = get_cleaned_datasets(
            st.session_state.username
        )

        st.subheader(
            "📂 Recent Cleaned Datasets"
        )

        if len(datasets) > 0:

            for dataset in datasets:

                st.write(
                    "•",
                    dataset[0]
                )

        else:

            st.info(
                "No Dataset Cleaned Yet"
            )

        # ---------------------------------
        # LOGOUT
        # ---------------------------------

        if st.button("Logout"):

            st.session_state.logged_in = False

            st.rerun()
# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

if selected_option == "Home":

    st.markdown(
        """
        <div class="main-title">
            🚀 DataNova AI
        </div>

        <div class="sub-title">
            Professional AI-Powered Data Cleaning Platform
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
        <div class="feature-card">
        <div class="feature-title">📤 Upload Dataset</div>
        <div class="feature-desc">
        Upload CSV and Excel datasets easily with drag & drop support.
         </div>
        </div>

        <div class="feature-card">
         <div class="feature-title">🧹 Data Cleaning</div>
         <div class="feature-desc">
            Clean missing values, duplicates and outliers automatically.
         </div>
            </div>

        <div class="feature-card">
             <div class="feature-title">📊 Visualization</div>
        <div class="feature-desc">
        Create professional charts and beautiful visual analytics instantly.
        </div>
         </div>

        <div class="feature-card">
        <div class="feature-title">📈 EDA Analysis</div>
        <div class="feature-desc">
        Perform detailed exploratory data analysis with smart insights.
        </div>
         </div>

        <div class="feature-card">
        <div class="feature-title">🤖 AI Suggestions</div>
            <div class="feature-desc">
        Get AI-powered recommendations and automated preprocessing ideas.
        </div>
        </div>

        <div class="feature-card">
        <div class="feature-title">📑 Reports</div>
        <div class="feature-desc">
        Generate professional downloadable reports and summaries.
         </div>
        </div>
        """, unsafe_allow_html=True)
# ---------------------------------------------------
# UPLOAD DATASET
# ---------------------------------------------------


elif selected_option == "Upload Dataset":

    st.header("Upload Your Dataset")

    uploaded_file = upload_dataset()

    if uploaded_file is not None:

        dataframe = load_dataset(uploaded_file)

        if dataframe is not None:

            show_dataset_preview(dataframe)
            st.session_state["df"] = dataframe
# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

elif selected_option == "Data Cleaning":

    st.header("🧹 Data Cleaning Module")

    uploaded_file = upload_dataset()

    if uploaded_file is not None:

        dataframe = pd.read_csv(uploaded_file)

        st.subheader("📄 Original Dataset")

        st.dataframe(dataframe.head())

        st.write("Original Shape:", dataframe.shape)

        st.write(
            "Total Missing Values:",
            dataframe.isnull().sum().sum()
        )

        st.write(
            "Duplicate Rows:",
            dataframe.duplicated().sum()
        )

        # =========================================
        # CLEANING MODE
        # =========================================

        cleaning_mode = st.selectbox(
            "Select Cleaning Mode",
            [
                "Automatic Cleaning",
                "Manual Cleaning"
            ]
        )

        # =========================================
        # AUTOMATIC CLEANING
        # =========================================

        if cleaning_mode == "Automatic Cleaning":

            st.subheader("🤖 Automatic AI Cleaning")

            remove_outliers = st.checkbox(
                "Remove Outliers"
            )

            drop_high_missing_cols = st.checkbox(
                "Drop Columns with Too Many Missing Values"
            )

            if st.button("Start Auto Cleaning"):

                cleaned_dataframe = dataframe.copy()

                cleaned_dataframe.drop_duplicates(
                    inplace=True
                )

                if drop_high_missing_cols:

                    missing_percent = (
                        cleaned_dataframe.isnull().mean()
                    ) * 100

                    cols_to_drop = missing_percent[
                        missing_percent > 50
                    ].index.tolist()

                    if len(cols_to_drop) > 0:

                        cleaned_dataframe.drop(
                            columns=cols_to_drop,
                            inplace=True
                        )

                numeric_cols = cleaned_dataframe.select_dtypes(
                    include=['number']
                ).columns

                for col in numeric_cols:

                    cleaned_dataframe[col].fillna(
                        cleaned_dataframe[col].mean(),
                        inplace=True
                    )

                categorical_cols = cleaned_dataframe.select_dtypes(
                    include=['object']
                ).columns

                for col in categorical_cols:

                    if not cleaned_dataframe[col].mode().empty:

                        cleaned_dataframe[col].fillna(
                            cleaned_dataframe[col].mode()[0],
                            inplace=True
                        )

                if remove_outliers:

                    for col in numeric_cols:

                        if cleaned_dataframe[col].nunique() < 10:
                            continue

                        Q1 = cleaned_dataframe[col].quantile(0.25)

                        Q3 = cleaned_dataframe[col].quantile(0.75)

                        IQR = Q3 - Q1

                        lower = Q1 - 1.5 * IQR

                        upper = Q3 + 1.5 * IQR

                        cleaned_dataframe = cleaned_dataframe[
                            (
                                cleaned_dataframe[col] >= lower
                            ) &
                            (
                                cleaned_dataframe[col] <= upper
                            )
                        ]

                st.session_state[
                    "cleaned_df"
                ] = cleaned_dataframe

                st.success(
                    "✅ Dataset Cleaned Successfully"
                )

                st.subheader("🧼 Cleaned Dataset")

                st.dataframe(
                    cleaned_dataframe.head()
                )

                st.write(
                    "Cleaned Shape:",
                    cleaned_dataframe.shape
                )

        # =========================================
        # MANUAL CLEANING
        # =========================================

        elif cleaning_mode == "Manual Cleaning":

            st.subheader(
                "🛠 Advanced Manual Cleaning Operations"
            )

            # =====================================
            # USE CLEANED DATA
            # =====================================

            if "cleaned_df" not in st.session_state:

                st.session_state[
                    "cleaned_df"
                ] = dataframe.copy()

            cleaned_dataframe = st.session_state[
                "cleaned_df"
            ]

            # =====================================
            # DATASET INFO
            # =====================================

            st.write(
                "Dataset Shape:",
                cleaned_dataframe.shape
            )

            st.write(
                "Missing Values:",
                cleaned_dataframe.isnull().sum().sum()
            )

            st.write(
                "Duplicate Rows:",
                cleaned_dataframe.duplicated().sum()
            )

            # =====================================
            # OPERATION SELECT
            # =====================================

            operation = st.selectbox(
                "Select Cleaning Operation",
                [
                    "Fill Missing Values",
                    "Remove Missing Values",
                    "Remove Duplicates",
                    "Drop Columns",
                    "Rename Columns",
                    "Remove Outliers",
                    "Convert Data Type",
                    "Replace Values",
                    "Text Cleaning",
                    "Encode Categorical Data",
                    "Normalize Data",
                    "Sort Dataset",
                    "Filter Rows",
                    "Remove Negative Values",
                    "Remove Constant Columns",
                    "Column Statistics",
                    "Null Value Summary",
                    "Undo Changes"
                ]
            )

            # =====================================
            # FILL MISSING VALUES
            # =====================================

            if operation == "Fill Missing Values":

                selected_col = st.selectbox(
                    "Select Column",
                    cleaned_dataframe.columns
                )

                method = st.selectbox(
                    "Select Method",
                    [
                        "Mean",
                        "Median",
                        "Mode",
                        "Custom Value"
                    ]
                )

                custom_value = ""

                if method == "Custom Value":

                    custom_value = st.text_input(
                        "Enter Custom Value"
                    )

                if st.button("Apply Fill Missing"):

                    if method == "Mean":

                        cleaned_dataframe[selected_col].fillna(
                            cleaned_dataframe[selected_col].mean(),
                            inplace=True
                        )

                    elif method == "Median":

                        cleaned_dataframe[selected_col].fillna(
                            cleaned_dataframe[selected_col].median(),
                            inplace=True
                        )

                    elif method == "Mode":

                        cleaned_dataframe[selected_col].fillna(
                            cleaned_dataframe[selected_col].mode()[0],
                            inplace=True
                        )

                    else:

                        cleaned_dataframe[selected_col].fillna(
                            custom_value,
                            inplace=True
                        )

                    st.success(
                        "✅ Missing Values Filled Successfully"
                    )

            # =====================================
            # REMOVE MISSING VALUES
            # =====================================

            elif operation == "Remove Missing Values":

                if st.button("Remove Missing Values"):

                    cleaned_dataframe.dropna(
                        inplace=True
                    )

                    st.success(
                        "✅ Missing Values Removed"
                    )

            # =====================================
            # REMOVE DUPLICATES
            # =====================================

            elif operation == "Remove Duplicates":

                if st.button("Remove Duplicates"):

                    cleaned_dataframe.drop_duplicates(
                        inplace=True
                    )

                    st.success(
                        "✅ Duplicate Rows Removed"
                    )

            # =====================================
            # DROP COLUMNS
            # =====================================

            elif operation == "Drop Columns":

                columns_to_drop = st.multiselect(
                    "Select Columns",
                    cleaned_dataframe.columns
                )

                if st.button("Drop Selected Columns"):

                    cleaned_dataframe.drop(
                        columns=columns_to_drop,
                        inplace=True
                    )

                    st.success(
                        "✅ Columns Dropped Successfully"
                    )

            # =====================================
            # RENAME COLUMNS
            # =====================================

            elif operation == "Rename Columns":

                selected_column = st.selectbox(
                    "Select Column",
                    cleaned_dataframe.columns
                )

                new_name = st.text_input(
                    "Enter New Column Name"
                )

                if st.button("Rename Column"):

                    cleaned_dataframe.rename(
                        columns={
                            selected_column: new_name
                        },
                        inplace=True
                    )

                    st.success(
                        "✅ Column Renamed Successfully"
                    )

            # =====================================
            # REMOVE OUTLIERS
            # =====================================

            elif operation == "Remove Outliers":

                numeric_cols = cleaned_dataframe.select_dtypes(
                    include=['number']
                ).columns

                selected_col = st.selectbox(
                    "Select Numeric Column",
                    numeric_cols
                )

                if st.button("Remove Outliers"):

                    Q1 = cleaned_dataframe[
                        selected_col
                    ].quantile(0.25)

                    Q3 = cleaned_dataframe[
                        selected_col
                    ].quantile(0.75)

                    IQR = Q3 - Q1

                    lower = Q1 - 1.5 * IQR

                    upper = Q3 + 1.5 * IQR

                    cleaned_dataframe = cleaned_dataframe[
                        (
                            cleaned_dataframe[selected_col]
                            >= lower
                        ) &
                        (
                            cleaned_dataframe[selected_col]
                            <= upper
                        )
                    ]

                    st.success(
                        "✅ Outliers Removed Successfully"
                    )

            # =====================================
            # FILTER ROWS
            # =====================================

            elif operation == "Filter Rows":

                filter_col = st.selectbox(
                    "Select Column",
                    cleaned_dataframe.columns
                )

                filter_value = st.text_input(
                    "Enter Filter Value"
                )

                if st.button("Filter Dataset"):

                    cleaned_dataframe = cleaned_dataframe[
                        cleaned_dataframe[
                            filter_col
                        ].astype(str).str.contains(
                            filter_value,
                            case=False,
                            na=False
                        )
                    ]

                    st.success(
                        "✅ Dataset Filtered Successfully"
                    )

            # =====================================
            # TEXT CLEANING
            # =====================================

            elif operation == "Text Cleaning":

                text_col = st.selectbox(
                    "Select Text Column",
                    cleaned_dataframe.select_dtypes(
                        include=['object', 'string']
                    ).columns
                )

                text_operation = st.selectbox(
                    "Select Text Operation",
                    [
                        "Lowercase",
                        "Uppercase",
                        "Title Case",
                        "Remove Spaces"
                    ]
                )

                if st.button("Apply Text Cleaning"):

                    if text_operation == "Lowercase":

                        cleaned_dataframe[text_col] = (
                            cleaned_dataframe[text_col]
                            .astype(str)
                            .str.lower()
                        )

                    elif text_operation == "Uppercase":

                        cleaned_dataframe[text_col] = (
                            cleaned_dataframe[text_col]
                            .astype(str)
                            .str.upper()
                        )

                    elif text_operation == "Title Case":

                        cleaned_dataframe[text_col] = (
                            cleaned_dataframe[text_col]
                            .astype(str)
                            .str.title()
                        )

                    elif text_operation == "Remove Spaces":

                        cleaned_dataframe[text_col] = (
                            cleaned_dataframe[text_col]
                            .astype(str)
                            .str.strip()
                        )

                    st.success(
                        "✅ Text Cleaned Successfully"
                    )

            # =====================================
            # SAVE SESSION STATE
            # =====================================

            st.session_state[
                "cleaned_df"
            ] = cleaned_dataframe

            # =====================================
            # FINAL PREVIEW
            # =====================================

            st.subheader(
                "🧼 Cleaned Dataset Preview"
            )

            st.dataframe(
                cleaned_dataframe.head()
            )

            st.write(
                "Dataset Shape:",
                cleaned_dataframe.shape
            )

            # =====================================
            # DOWNLOAD BUTTON
            # =====================================

            csv = cleaned_dataframe.to_csv(
                index=False
            ).encode("utf-8")

            logged_in = st.session_state.get(
                "logged_in",
                False
            )

            if logged_in:

                st.download_button(
                    label="⬇ Download Cleaned Dataset",
                    data=csv,
                    file_name="manual_cleaned_dataset.csv",
                    mime="text/csv"
                )

            else:

                st.warning(
                    "Please Login to Download Dataset"
                )
          # -------------------------------------
# DOWNLOAD BUTTON
# -------------------------------------


# ---------------------------------------------------
# VISUALIZATION MODULE
# ---------------------------------------------------

elif selected_option == "Visualization":

    st.header("📊 Visualization Module")

    uploaded_file = upload_dataset()

    if uploaded_file is not None:

        # ---------------------------------------
        # USE CLEANED DATA IF AVAILABLE
        # ---------------------------------------

        if "cleaned_df" in st.session_state:

            dataframe = st.session_state["cleaned_df"]

            st.success(
                "✅ Using Cleaned Dataset For Visualization"
            )

        else:

            dataframe = pd.read_csv(uploaded_file)

            st.warning(
                "⚠ Using Original Dataset"
            )

        if dataframe is not None:

            # ---------------------------------------
            # DATASET PREVIEW
            # ---------------------------------------

            st.subheader("📄 Dataset Preview")

            st.dataframe(dataframe.head())

            st.write(
                "Dataset Shape:",
                dataframe.shape
            )

            # ---------------------------------------
            # VISUALIZATION SELECTION
            # ---------------------------------------

            visualization_option = st.selectbox(
                "Select Visualization",
                [
                    "Histogram",
                    "Box Plot",
                    "Heatmap",
                    "Scatter Plot",
                    "Correlation Matrix",
                    "Line Chart",
                    "Bar Chart",
                    "Pie Chart",
                    "Count Plot",
                    "Pair Plot",
                    "Missing Values Chart",
                    "Outlier Visualization"
                ]
            )

            # ---------------------------------------
            # NUMERIC & CATEGORICAL COLUMNS
            # ---------------------------------------

            numeric_cols = dataframe.select_dtypes(
                include=['number']
            ).columns

            categorical_cols = dataframe.select_dtypes(
                include=['object']
            ).columns

            # =======================================
            # HISTOGRAM
            # =======================================

            if visualization_option == "Histogram":

                st.subheader("📈 Histogram")

                selected_col = st.selectbox(
                    "Select Numeric Column",
                    numeric_cols
                )

                fig, ax = plt.subplots()

                sns.histplot(
                    dataframe[selected_col],
                    kde=True,
                    ax=ax
                )

                st.pyplot(fig)

            # =======================================
            # BOX PLOT
            # =======================================

            elif visualization_option == "Box Plot":

                st.subheader("📦 Box Plot")

                selected_col = st.selectbox(
                    "Select Numeric Column",
                    numeric_cols
                )

                fig, ax = plt.subplots()

                sns.boxplot(
                    y=dataframe[selected_col],
                    ax=ax
                )

                st.pyplot(fig)

            # =======================================
            # HEATMAP
            # =======================================

            elif visualization_option == "Heatmap":

                st.subheader("🔥 Heatmap")

                fig, ax = plt.subplots(
                    figsize=(10, 6)
                )

                sns.heatmap(
                    dataframe.corr(numeric_only=True),
                    annot=True,
                    cmap="coolwarm",
                    ax=ax
                )

                st.pyplot(fig)

            # =======================================
            # SCATTER PLOT
            # =======================================

            elif visualization_option == "Scatter Plot":

                st.subheader("🎯 Scatter Plot")

                x_col = st.selectbox(
                    "Select X Column",
                    numeric_cols
                )

                y_col = st.selectbox(
                    "Select Y Column",
                    numeric_cols
                )

                fig, ax = plt.subplots()

                sns.scatterplot(
                    x=dataframe[x_col],
                    y=dataframe[y_col],
                    ax=ax
                )

                st.pyplot(fig)

            # =======================================
            # CORRELATION MATRIX
            # =======================================

            elif visualization_option == "Correlation Matrix":

                st.subheader("🔗 Correlation Matrix")

                correlation = dataframe.corr(
                    numeric_only=True
                )

                st.dataframe(correlation)

            # =======================================
            # LINE CHART
            # =======================================

            elif visualization_option == "Line Chart":

                st.subheader("📉 Line Chart")

                x_col = st.selectbox(
                    "Select X Column",
                    dataframe.columns
                )

                y_col = st.selectbox(
                    "Select Y Column",
                    numeric_cols
                )

                fig, ax = plt.subplots()

                sns.lineplot(
                    x=dataframe[x_col],
                    y=dataframe[y_col],
                    ax=ax
                )

                plt.xticks(rotation=45)

                st.pyplot(fig)

            # =======================================
            # BAR CHART
            # =======================================

            elif visualization_option == "Bar Chart":

                st.subheader("📊 Bar Chart")

                x_col = st.selectbox(
                    "Select Categorical Column",
                    categorical_cols
                )

                y_col = st.selectbox(
                    "Select Numeric Column",
                    numeric_cols
                )

                fig, ax = plt.subplots()

                sns.barplot(
                    x=dataframe[x_col],
                    y=dataframe[y_col],
                    ax=ax
                )

                plt.xticks(rotation=45)

                st.pyplot(fig)

            # =======================================
            # PIE CHART
            # =======================================

            elif visualization_option == "Pie Chart":

                st.subheader("🥧 Pie Chart")

                selected_col = st.selectbox(
                    "Select Column",
                    categorical_cols
                )

                pie_data = dataframe[
                    selected_col
                ].value_counts()

                fig, ax = plt.subplots()

                ax.pie(
                    pie_data,
                    labels=pie_data.index,
                    autopct='%1.1f%%'
                )

                ax.axis('equal')

                st.pyplot(fig)

            # =======================================
            # COUNT PLOT
            # =======================================

            elif visualization_option == "Count Plot":

                st.subheader("🔢 Count Plot")

                selected_col = st.selectbox(
                    "Select Column",
                    categorical_cols
                )

                fig, ax = plt.subplots()

                sns.countplot(
                    x=dataframe[selected_col],
                    ax=ax
                )

                plt.xticks(rotation=45)

                st.pyplot(fig)

            # =======================================
            # PAIR PLOT
            # =======================================

            elif visualization_option == "Pair Plot":

                st.subheader("🔍 Pair Plot")

                pairplot_fig = sns.pairplot(
                    dataframe[numeric_cols]
                )

                st.pyplot(pairplot_fig)

            # =======================================
            # MISSING VALUES CHART
            # =======================================

            elif visualization_option == "Missing Values Chart":

                st.subheader(
                    "❓ Missing Values Chart"
                )

                missing_values = dataframe.isnull().sum()

                fig, ax = plt.subplots(
                    figsize=(10, 5)
                )

                missing_values.plot(
                    kind='bar',
                    ax=ax
                )

                plt.xticks(rotation=45)

                st.pyplot(fig)

            # =======================================
            # OUTLIER VISUALIZATION
            # =======================================

            elif visualization_option == "Outlier Visualization":

                st.subheader(
                    "🚨 Outlier Visualization"
                )

                selected_col = st.selectbox(
                    "Select Numeric Column",
                    numeric_cols
                )

                fig, ax = plt.subplots()

                sns.boxplot(
                    x=dataframe[selected_col],
                    ax=ax
                )

                st.pyplot(fig)

            # =======================================
            # DOWNLOAD DATASET
            # =======================================

            csv = dataframe.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇ Download Current Dataset",
                data=csv,
                file_name="visualized_dataset.csv",
                mime="text/csv"


            )

# ---------------------------------------------------
# EDA ANALYSIS
# ---------------------------------------------------

elif selected_option == "EDA Analysis":

    uploaded_file = upload_dataset()

    if uploaded_file is not None:

        if "cleaned_df" in st.session_state:

            dataframe = st.session_state[
                "cleaned_df"
            ]

        else:

            dataframe = load_dataset(
                uploaded_file
            )

        show_eda_analysis(
            dataframe
        )
        # ---------------------------------------------------
# AI SUGGESTIONS
# ---------------------------------------------------

elif selected_option == "AI Suggestions":

    st.header("🤖 AI Smart Suggestions")

    uploaded_file = upload_dataset()

    if uploaded_file is not None:

        if "cleaned_df" in st.session_state:

            dataframe = st.session_state[
                "cleaned_df"
            ]

        else:

            dataframe = pd.read_csv(
                uploaded_file
            )

        st.subheader("📄 Dataset Preview")

        st.dataframe(
            dataframe.head()
        )

        st.subheader(
            "🧠 AI Suggestions Report"
        )

        suggestions = []

        missing = dataframe.isnull().sum().sum()

        if missing > 0:

            suggestions.append(
                f"Dataset contains {missing} missing values."
            )

        else:

            suggestions.append(
                "No missing values found."
            )

        duplicates = dataframe.duplicated().sum()

        if duplicates > 0:

            suggestions.append(
                f"Dataset contains {duplicates} duplicate rows."
            )

        else:

            suggestions.append(
                "No duplicate rows found."
            )

        numeric_cols = dataframe.select_dtypes(
            include=['number']
        ).columns

        if len(numeric_cols) > 0:

            suggestions.append(
                "Numeric columns detected."
            )

        categorical_cols = dataframe.select_dtypes(
            include=['object', 'string']
        ).columns

        if len(categorical_cols) > 0:

            suggestions.append(
                "Categorical columns available."
            )

        suggestions.append(
            f"Dataset Shape: {dataframe.shape}"
        )

        for suggestion in suggestions:

            st.success(
                suggestion
            )


# ---------------------------------------------------
# REPORTS
# ---------------------------------------------------

elif selected_option == "Reports":

    st.header("📊 Dataset Reports")

    uploaded_file = upload_dataset()

    if uploaded_file is not None:

        if "cleaned_df" in st.session_state:

            dataframe = st.session_state[
                "cleaned_df"
            ]

        else:

            dataframe = pd.read_csv(
                uploaded_file
            )

        st.subheader(
            "📄 Dataset Preview"
        )

        st.dataframe(
            dataframe.head()
        )

        st.subheader(
            "📋 Dataset Report"
        )

        st.write(
            "Shape:",
            dataframe.shape
        )

        st.write(
            "Columns:"
        )

        st.write(
            list(dataframe.columns)
        )

        st.write(
            "Missing Values:"
        )

        st.dataframe(
            dataframe.isnull().sum()
        )

        st.write(
            "Data Types:"
        )

        st.dataframe(
            dataframe.dtypes.astype(str)
        )

        st.write(
            "Statistical Summary:"
        )

        st.dataframe(
            dataframe.describe()
        )


# ---------------------------------------------------
# AI CHATBOT
# ---------------------------------------------------
