import pandas as pd


class Csv2Json:

    def __init__(self, input_file_csv, delimiter=","):
        self.input_file_csv = input_file_csv
        self.delimiter = delimiter

    def make_json(self):
        # create a dictionary

        df = pd.read_csv(filepath_or_buffer=self.input_file_csv, delimiter=self.delimiter)
        # Open a csv reader called DictReader
        return df.to_json(orient='records', lines=True).splitlines()
