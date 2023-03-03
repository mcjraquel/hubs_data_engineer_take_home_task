import pandas as pd
import json


def calculate(df):
    holes_df = setup_df(df)
    calculate_fields(holes_df)
    fill_na(holes_df)
    cast_to_types(holes_df)
    holes_df = holes_df.drop("holes", axis=1)

    return holes_df


def setup_df(df):
    holes_df = df[
        ["uuid", "holes", "has_unreachable_hole_warning", "has_unreachable_hole_error"]
    ]
    holes_df = holes_df.dropna(subset=["holes"]).reset_index(drop=True)
    holes_df["holes"] = holes_df.holes.apply(lambda x: json.loads(x))
    holes_df = holes_df.explode("holes")

    return holes_df


def calculate_fields(df):
    df["center_x"] = df.holes.apply(
        lambda x: x["center"]["x"] if "center" in x else pd.NA
    )
    df["center_y"] = df.holes.apply(
        lambda x: x["center"]["y"] if "center" in x else pd.NA
    )
    df["center_z"] = df.holes.apply(
        lambda x: x["center"]["z"] if "center" in x else pd.NA
    )
    df["direction_x"] = df.holes.apply(
        lambda x: x["direction"]["x"] if "direction" in x else pd.NA
    )
    df["direction_y"] = df.holes.apply(
        lambda x: x["direction"]["y"] if "direction" in x else pd.NA
    )
    df["direction_z"] = df.holes.apply(
        lambda x: x["direction"]["z"] if "direction" in x else pd.NA
    )
    df["end1_closed"] = df.holes.apply(
        lambda x: x["end1"]["closed"] if "end1" in x else pd.NA
    )
    df["end1_reachable"] = df.holes.apply(
        lambda x: x["end1"]["reachable"] if "end1" in x else pd.NA
    )
    df["end2_closed"] = df.holes.apply(
        lambda x: x["end2"]["closed"] if "end2" in x else pd.NA
    )
    df["end2_reachable"] = df.holes.apply(
        lambda x: x["end2"]["reachable"] if "end2" in x else pd.NA
    )
    df["facet_count"] = df.holes.apply(
        lambda x: x["facet_count"] if "facet_count" in x else pd.NA
    )
    df["length"] = df.holes.apply(lambda x: x["length"] if "length" in x else pd.NA)
    df["radius"] = df.holes.apply(lambda x: x["radius"] if "radius" in x else pd.NA)


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
            "end1_closed": bool,
            "end1_reachable": bool,
            "end2_closed": bool,
            "end2_reachable": bool,
            "facet_count": int,
            "length": float,
            "radius": float,
        }
    )
