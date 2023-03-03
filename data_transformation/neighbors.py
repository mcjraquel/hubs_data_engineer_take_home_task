import pandas as pd
import json
import sys
import os

from dotenv import find_dotenv

sys.path.append(os.path.dirname(find_dotenv()))

from data_transformation.utils import convert_volume_fields


def calculate(df):
    neighbors_df = setup_df(df)
    neighbors_df = calculate_fields(neighbors_df)
    neighbors_df = cast_to_types(neighbors_df)
    neighbors_df = neighbors_df.drop("neighbors", axis=1)

    return neighbors_df


def setup_df(df):
    neighbors_df = df[["uuid", "neighbors"]]
    neighbors_df = neighbors_df.dropna(subset=["neighbors"]).reset_index(drop=True)
    neighbors_df["neighbors"] = neighbors_df.neighbors.apply(lambda x: json.loads(x))

    return neighbors_df


def calculate_fields(df):
    df["neighbor"] = df.neighbors.apply(lambda x: x["value"])
    df["unit"] = df.neighbors.apply(lambda x: x["unit"])
    df = df.explode("neighbor")
    df["neighbor"] = df.apply(
        lambda x: convert_volume_fields({"unit": x["unit"], "value": x["neighbor"]}),
        axis=1,
    )
    df = df.drop("unit", axis=1)

    return df


def cast_to_types(df):
    df = df.astype(
        {
            "neighbor": int,
        }
    )

    return df
