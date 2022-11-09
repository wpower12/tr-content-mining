"""
Script to process a labeled_data.csv file and insert its raw data into the DB.

INPUTS
    Filename   - Name of the csv file to process
    Labeler_ID - The ID of the human labeler
    Questions  - Ignore for now, assume they have all the questions, and that we can read their ids from the csv file.
    DB Name    - Name of the DB to actually use.
    DB Credentials - Should just stay in a .env file, like usual
OUTPUTS
    None

SIDE EFFECTS
    Modifies the state of the DB
"""