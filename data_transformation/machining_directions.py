import pandas as pd
import json
import sys
import os

from dotenv import find_dotenv

sys.path.append(os.path.dirname(find_dotenv()))

from data_transformation.utils import convert_volume_fields


def calculate(df):
    machining_directions_df = setup_df(df)
    calculate_fields(machining_directions_df)
    fill_na(machining_directions_df)
    cast_to_types(machining_directions_df)
    machining_directions_df = machining_directions_df.drop(
        "machining_directions", axis=1
    )

    return machining_directions_df


def setup_df(df):
    machining_directions_df = df[["uuid", "machining_directions"]]
    machining_directions_df = machining_directions_df.dropna(
        subset=["machining_directions"]
    ).reset_index(drop=True)
    machining_directions_df[
        "machining_directions"
    ] = machining_directions_df.machining_directions.apply(lambda x: json.loads(x))

    return machining_directions_df


def calculate_fields(df):
    df["box_volume"] = df.machining_directions.apply(
        lambda x: convert_volume_fields(x["box_volume"]) if "box_volume" in x else pd.NA
    )
    df["direction_removable_volume"] = df.machining_directions.apply(
        lambda x: json.dumps(x["direction_removable_volume"])
        if "direction_removable_volume" in x
        else pd.NA
    )
    df["is_machinable"] = df.machining_directions.apply(
        lambda x: x["is_machinable"] if "is_machinable" in x else pd.NA
    )
    df["selected_directions"] = df.machining_directions.apply(
        lambda x: json.dumps(x["selected_directions"])
        if "selected_directions" in x
        else pd.NA
    )
    df["unmachinable_volume"] = df.machining_directions.apply(
        lambda x: convert_volume_fields(x["unmachinable_volume"])
        if "unmachinable_volume" in x
        else pd.NA
    )
    df["unmachinable_volume_url"] = df.machining_directions.apply(
        lambda x: x["unmachinable_volume_url"]
        if "unmachinable_volume_url" in x
        else pd.NA
    )


def fill_na(df):
    df["box_volume"] = df.box_volume.fillna(0)
    df["unmachinable_volume"] = df.unmachinable_volume.fillna(0)


def cast_to_types(df):
    df = df.astype(
        {
            "box_volume": float,
            "direction_removable_volume": str,
            "is_machinable": bool,
            "selected_directions": str,
            "unmachinable_volume": float,
            "unmachinable_volume_url": str,
        }
    )
