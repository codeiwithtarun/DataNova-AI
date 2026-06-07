from fastapi import FastAPI
import pandas as pd

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Backend is working"}


@app.post("/clean")
def clean_data(data: dict):

    df = pd.DataFrame(data)

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill numeric columns with mean
    numeric_cols = df.select_dtypes(include=['number']).columns

    for col in numeric_cols:

        mean_value = df[col].mean()

        df[col] = df[col].fillna(mean_value)

    # Fill text columns with mode
    categorical_cols = df.select_dtypes(include=['object']).columns

    for col in categorical_cols:

        if not df[col].mode().empty:

            mode_value = df[col].mode()[0]

            df[col] = df[col].fillna(mode_value)

    return df.to_dict(orient="list")
