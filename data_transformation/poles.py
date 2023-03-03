import pandas as pd
import json


def calculate(df):
    poles_df = setup_df(df)
    calculate_fields(poles_df)
    fill_na(poles_df)
    poles_df = poles_df.drop("poles", axis=1)

    return poles_df


def setup_df(df):
    poles_df = df[["uuid", "poles"]]
    poles_df = poles_df.dropna(subset=["poles"]).reset_index(drop=True)
    poles_df["poles"] = poles_df.poles.apply(lambda x: json.loads(x))
    poles_df = poles_df.explode("poles")

    return poles_df


def calculate_fields(df):
    df["center_x"] = df.poles.apply(
        lambda x: x["center"]["x"] if "center" in x else pd.NA
    )
    df["center_y"] = df.poles.apply(
        lambda x: x["center"]["y"] if "center" in x else pd.NA
    )
    df["center_z"] = df.poles.apply(
        lambda x: x["center"]["z"] if "center" in x else pd.NA
    )
    df["direction_x"] = df.poles.apply(
        lambda x: x["direction"]["x"] if "direction" in x else pd.NA
    )
    df["direction_y"] = df.poles.apply(
        lambda x: x["direction"]["y"] if "direction" in x else pd.NA
    )
    df["direction_z"] = df.poles.apply(
        lambda x: x["direction"]["z"] if "direction" in x else pd.NA
    )
    df["end_closed"] = df.poles.apply(
        lambda x: x["end"]["closed"] if "end" in x else pd.NA
    )
    df["end_reachable"] = df.poles.apply(
        lambda x: x["end"]["reachable"] if "end" in x else pd.NA
    )
    df["facet_count"] = df.poles.apply(
        lambda x: x["facet_count"] if "facet_count" in x else pd.NA
    )
    df["length"] = df.poles.apply(lambda x: x["length"] if "length" in x else pd.NA)
    df["radius"] = df.poles.apply(lambda x: x["radius"] if "radius" in x else pd.NA)


def fill_na(df):
    df["facet_count"] = df.facet_count.fillna(0)
    df["length"] = df.length.fillna(0)
    df["radius"] = df.radius.fillna(0)


def cast_to_types(df):
    df = df.astype(
        {
            "center_x": float,
            "center_y": float,
            "center_z": float,
            "direction_x": float,
            "direction_y": float,
            "direction_z": float,
            "end_closed": bool,
            "end_reachable": bool,
            "facet_count": int,
            "length": float,
            "radius": float,
        }
    )
