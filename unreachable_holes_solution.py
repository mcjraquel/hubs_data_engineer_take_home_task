import pandas as pd
import json


def main():
    data = pd.read_parquet("2023 DE_case_dataset.gz.parquet")

    data["has_unreachable_hole_warning"] = data.apply(
        lambda row: any(
            [hole["length"] > hole["radius"] * 20 for hole in json.loads(row["holes"])]
        )
        if not pd.isna(row["holes"])
        else False,
        axis=1,
    )
    data["has_unreachable_hole_error"] = data.apply(
        lambda row: any(
            [hole["length"] > hole["radius"] * 80 for hole in json.loads(row["holes"])]
        )
        if not pd.isna(row["holes"])
        else False,
        axis=1,
    )

    export = input("Would you like to export the table to a CSV file? [y/n]: ")
    while export not in ["y", "n"]:
        export = input(
            "Would you like to export the tables to CSV files to your current directory? [y/n]: "
        )

    if export == "y":
        data.to_csv("unreachable_holes_solution.csv")


if __name__ == "__main__":
    main()
