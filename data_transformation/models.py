import pandas as pd
import json
import sys
import os

from dotenv import find_dotenv

sys.path.append(os.path.dirname(find_dotenv()))


from pint import UnitRegistry
from datetime import datetime
from data_transformation.utils import convert_time_fields, convert_length_fields

ureg = UnitRegistry()


def calculate(df):
    calculate_time_fields(df)
    df = calculate_multipart_fields(df)
    df = calculate_sheet_like_shape_fields(df)
    df = calculate_unmachinable_edges_fields(df)
    df = remove_old_fields(df)
    df = df.astype(
        {
            "uuid": str,
        }
    )

    return df


def calculate_time_fields(df):
    df["geometric_heuristics"] = df.geometric_heuristics.apply(convert_time_fields)
    df["job_run_time"] = df.job_run_time.apply(convert_time_fields)
    df["created"] = df.created.apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    )
    df["updated"] = df.updated.apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    )
    df["queued"] = df.queued.apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    df["time"] = df.time.apply(lambda x: int(float(x)))


def calculate_multipart_fields(df):
    df["multipart"] = df.multipart.apply(
        lambda x: json.loads(x if not pd.isna(x) else "{}")
    )
    df["multipart_multibody"] = df.multipart.apply(
        lambda x: bool(x["multibody"]) if "multibody" in x else pd.NA
    )
    df["multipart_patches_count"] = df.multipart.apply(
        lambda x: int(x["patches"]["count"] or 0)
        if "patches" in x and "count" in x["patches"]
        else pd.NA
    )
    df["multipart_patches_not_tiny_count"] = df.multipart.apply(
        lambda x: int(x["patches"]["not_tiny_count"] or 0)
        if "patches" in x and "not_tiny_count" in x["patches"]
        else pd.NA
    )
    df = df.drop("multipart", axis=1)

    return df


def calculate_sheet_like_shape_fields(df):
    df["sheet_like_shape"] = df.sheet_like_shape.apply(
        lambda x: json.loads(x if not pd.isna(x) else "{}")
    )
    df["sheet_like_shape_detected"] = df.sheet_like_shape.apply(
        lambda x: bool(x["detected"]) if "detected" in x else False
    )
    df["sheet_like_shape_positive_fraction_of_samples"] = df.sheet_like_shape.apply(
        lambda x: float(x["positive_fraction_of_samples"])
        if "positive_fraction_of_samples" in x
        else 0
    )
    df["sheet_like_shape_thickness"] = df.sheet_like_shape.apply(
        lambda x: float(extract_thickness(x["thickness"])) if "thickness" in x else 0
    )
    df = df.drop("sheet_like_shape", axis=1)

    return df


def calculate_unmachinable_edges_fields(df):
    df["unmachinable_edges"] = df.unmachinable_edges.apply(
        lambda x: json.loads(x if not pd.isna(x) else "{}")
    )
    df["unmachinable_edges_count"] = df.unmachinable_edges.apply(
        lambda x: int(x["count"]) if "count" in x else False
    )
    df["unmachinable_edges_list_url"] = df.unmachinable_edges.apply(
        lambda x: str(x["edge_list_url"]) if "edge_list_url" in x else False
    )
    df["unmachinable_edges_length"] = df.unmachinable_edges.apply(
        lambda x: float(x["length"]) if "length" in x else False
    )
    df = df.drop("unmachinable_edges", axis=1)

    return df


def calculate_extrusion_height_field(df):
    df["extrusion_height"] = df.apply(
        lambda x: float(
            (x["extrusion_height"]) * ureg(x["units"]).to("mm").magnitude
            if not pd.isna(x["extrusion_height"])
            else 0
        ),
        axis=1,
    )
    df = df.drop("units", axis=1)

    return df


def remove_old_fields(df):
    df = df.drop("holes", axis=1)
    df = df.drop("latheability", axis=1)
    df = df.drop("machining_directions", axis=1)
    df = df.drop("neighbors", axis=1)
    df = df.drop("poles", axis=1)
    df = df.drop("units", axis=1)

    return df


def extract_thickness(val):
    if isinstance(val, float):
        return val

    if isinstance(val, str):
        val = json.loads(val)

    try:
        val = convert_length_fields(val)
    except TypeError:
        return val

    return val
