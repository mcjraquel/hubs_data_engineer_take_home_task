import pandas as pd
import json
from pint import UnitRegistry

ureg = UnitRegistry()


def convert_time_fields(value, to="milliseconds"):
    if pd.isna(value):
        return 0

    val_dict = json.loads(value)
    time = float(val_dict["value"])
    unit = ureg(val_dict["unit"])
    time_in_milliseconds = (time * unit).to(to).magnitude

    return time_in_milliseconds


def convert_volume_fields(val_dict, to="mm**3"):
    volume = float(val_dict["value"])
    unit = val_dict["unit"]
    formatted_unit = ureg("{0}**{1}".format(unit[:-1], unit[-1]))
    volume_in_cubic_mm = (volume * formatted_unit).to(to).magnitude

    return volume_in_cubic_mm


def convert_length_fields(val_dict, to="mm"):
    if pd.isna(val_dict):
        return 0

    length = float(val_dict["value"])
    unit = ureg(val_dict["unit"])
    length_in_mm = (length * unit).to(to).magnitude

    return length_in_mm
