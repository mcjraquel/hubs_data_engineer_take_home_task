import pandas as pd
import json
import time
import sys
import os

from dotenv import find_dotenv

sys.path.append(os.path.dirname(find_dotenv()))

from data_transformation import models
from data_transformation import holes
from data_transformation import latheability
from data_transformation import machining_directions
from data_transformation import neighbors
from data_transformation import poles


def main():
    print("Transforming data...")
    start = time.time()

    data = pd.read_parquet("2023 DE_case_dataset.gz.parquet")
    calculate_unreachable_holes_fields(data)
    holes_df = holes.calculate(data)
    latheability_df = latheability.calculate(data)
    machining_directions_df = machining_directions.calculate(data)
    neighbors_df = neighbors.calculate(data)
    poles_df = poles.calculate(data)
    models_df = models.calculate(data)

    end = time.time()
    print("Done! Elapsed time: {}".format(end - start))

    export = input("Would you like to export the tables to CSV files? [y/n]: ")
    while export not in ["y", "n"]:
        export = input(
            "Would you like to export the tables to CSV files to your current directory? [y/n]: "
        )

    if export == "y":
        holes_df.to_csv("holes.csv")
        latheability_df.to_csv("latheability.csv")
        machining_directions_df.to_csv("machining_directions.csv")
        neighbors_df.to_csv("neighbors.csv")
        poles_df.to_csv("poles.csv")
        models_df.to_csv("models.csv")

    return {
        "holes": holes_df,
        "latheability": latheability_df,
        "machining_directions": machining_directions_df,
        "neighbors": neighbors_df,
        "poles": poles_df,
        "models": models_df,
    }


def calculate_unreachable_holes_fields(df):
    df["has_unreachable_hole_warning"] = df.apply(
        lambda row: any(
            [hole["length"] > hole["radius"] * 20 for hole in json.loads(row["holes"])]
        )
        if not pd.isna(row["holes"])
        else False,
        axis=1,
    )
    df["has_unreachable_hole_error"] = df.apply(
        lambda row: any(
            [hole["length"] > hole["radius"] * 80 for hole in json.loads(row["holes"])]
        )
        if not pd.isna(row["holes"])
        else False,
        axis=1,
    )


if __name__ == "__main__":
    main()
