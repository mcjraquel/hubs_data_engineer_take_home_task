import pandas as pd
import json


def calculate(df):
    latheability_df = setup_df(df)
    calculate_fields(latheability_df)
    fill_na(latheability_df)
    cast_to_types(latheability_df)
    latheability_df = latheability_df.drop("latheability", axis=1)

    return latheability_df


def setup_df(df):
    latheability_df = df[["uuid", "latheability"]]
    latheability_df = latheability_df.dropna(subset=["latheability"]).reset_index(
        drop=True
    )
    latheability_df["latheability"] = latheability_df.latheability.apply(
        lambda x: json.loads(x)
    )

    return latheability_df


def calculate_fields(df):
    df["axis_x"] = df.latheability.apply(
        lambda x: x["axis"]["x"] if "axis" in x else pd.NA
    )
    df["axis_y"] = df.latheability.apply(
        lambda x: x["axis"]["y"] if "axis" in x else pd.NA
    )
    df["axis_z"] = df.latheability.apply(
        lambda x: x["axis"]["z"] if "axis" in x else pd.NA
    )
    df["origin_x"] = df.latheability.apply(
        lambda x: x["origin"]["x"] if "origin" in x else pd.NA
    )
    df["origin_y"] = df.latheability.apply(
        lambda x: x["origin"]["y"] if "origin" in x else pd.NA
    )
    df["origin_z"] = df.latheability.apply(
        lambda x: x["origin"]["z"] if "origin" in x else pd.NA
    )
    df["fraction"] = df.latheability.apply(
        lambda x: x["fraction"] if "fraction" in x else pd.NA
    )


def fill_na(df):
    df["fraction"] = df.fraction.fillna(0)


def cast_to_types(df):
    df = df.astype(
        {
            "uuid": str,
            "axis_x": int,
            "axis_y": int,
            "axis_z": int,
            "origin_x": float,
            "origin_y": float,
            "origin_z": float,
            "fraction": float,
        }
    )
