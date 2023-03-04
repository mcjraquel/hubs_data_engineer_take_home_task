# Hubs Data Engineer Take-home Task

Hello! In this project, I am given sample data on the DFM of 3D models submitted on the Hubs online platform.

I attempt to do the following things:

1. Create two additional fields called `has_unreachable_hole_warning` and `has_unreachable_hole_error`. A warning is given if the hole has a poor ratio (`length > radius * 2 * 10`), while an error is given if the hole has a critical ratio (`length > radius * 2 * 40`).
2. Design a transformation pipeline to flatten the data in the given Parquet fie.
3. Visualize the tables and relationships in the proposed schema using an ERD.
4. Give some observations and insights on the size, structure, and volume of the data.
5. Give some insights on the data on the models' holes.

There are three very important files in this repo:

1. `unreachable_holes_solution.py`
   This accepts no argument (automatically takes the given Parquet file) and this will ask if the user would like to export the raw data with the two additional columns to a CSV file. This has already been executed and the resulting CSV file can be found in the same directory.
2. `data_transformation\main.py`
   This also accepts no argument (automatically takes the given Parquet file) and this will also ask if the user would like to export the transformed tables to CSV files. This has already been executed and the resulting CSV files can be found in the same directory as well. The specifics of how I transformed the `holes` column of the raw data can be found in the `data_transformation\holes.py` file.

    Additionally, the `main` function of this file returns a dictionary of table names and corresponding DataFrames. This can be imported and called within the repo so that the user can access the transformed data (as demonstrated in file #3).

3. `insights.ipynb`
   This is where I put down my observations and insights on the raw data, transform the data using the `main` function from file #2, and try to gain insights on the holes data. I also solve the unreachable holes problem here using SQL queries on the transformed `holes` table.

Assumptions while solving the problem:

1. Time and length are in `ms` and `mm`, respectively. Consequently, volume is in `mm**3`. All values not in these units are converted.
2. Timestamps are in `%Y-%m-%d %H:%M:%S` format.
3. All holes have center (x, y, z), direction (x, y, z), two ends (with `closed` and `reachable` values), length and radius.
4. All poles have center (x, y, z), direction (x, y, z), an end (with `closed` and `reachable` values), length and radius.
5. The `units` field is for the `extrusion_height` field, and since I converted values to `mm`, the `units` field can be decommissioned.

About the assessment:

-   How long did it take you to complete the task?
    I worked on the whole task a few hours a day for a few days. For the two additional fields, I was able to solve this in Python in a few minutes. The transformation is what took most of my time, as well as gaining insights from the data.

-   What part did you find the most challenging? Was something unclear?
    The transformation was definitely the most challenging, because almost all the fields were in string data type, and within these were actually deeply nested dictionaries, with values that were also differing in data type.

-   Do you think the assignment has an appropriate level of difficulty?
    I think this is appropriate for the few days given to me.

-   Does the assignment evaluate what you expected?
    Yes, I would say that the task was something that I would expect from a tahe-home task for the Data Engineer position. While the data transformation part was the most challenging for me, it was also very fun and I learned a lot from the experience.

Thanks for going through my work!
