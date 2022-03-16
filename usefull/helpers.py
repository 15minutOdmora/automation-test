"""
Various helper functions and classes.
"""

from typing import List, Union, Callable
import sys
import traceback
import csv
import os
from datetime import date, datetime, timedelta


def analyse_error(output: bool = False) -> List[Union[str, int]]:
    """
    Function analyses error info by reading the stack trace in execution info.

    Args:
        output (bool): If an output should be displayed in the console.

    Returns:
        List[Union[str, int]]: List containing error data -> [filename, line, function name, code that triggered error]
    """
    _, _, tb = sys.exc_info()
    filename, line, func, line_code = traceback.extract_tb(tb)[-1]

    if output:
        print(
            "Test failed at:\n"
            f"\tFunction {func} in:\n\t\t{filename} line {line}\n"
            f"\tError: {line_code}"
        )

    return [filename, line, func, line_code]


def create_csv_file(file_path: str, header: List[any]) -> None:
    """
    Creates new csv file on given file path (if it doesn't already exist), adds header to the first line.

    Args:
        file_path (str): Path to csv file.
        header (List[any]): Header with column titles to add.
    """
    if not os.path.isfile(file_path):
        with open(file_path, "w", encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # Write the header
            writer.writerow(header)


def append_to_csv_file(file_path: str, data: Union[List[List[any]], List[any]]) -> None:
    """
    Adds new row to given csv file.

    Args:
        file_path (str): Path to csv file.
        data (Union[List[List[any]], List[any]]): Either a single row of data, or a list containing multiple rows.
    """
    with open(file_path, "a", encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # Write data
        if type(data[0]) is list:
            writer.writerows(data)
        else:
            writer.writerow(data)


class TimeMeasure:
    """
    Class for measuring time.
    A logging function can be passed for saving start / end data.
    """
    def __init__(self, logging_function: Callable = lambda _: None):
        """
        Args:
            logging_function: A logging function used system wide to save to log files. Defaults to dummy lambda.
        """
        self.start_time = 0
        self.end_time = 0
        self._elapsed_seconds = 0

        self.logging_function = logging_function

    @property
    def elapsed_seconds(self) -> float:
        if self.end_time == 0:  # Has not yet been set
            self._elapsed_seconds = datetime.now().timestamp() - self.start_time
        else:
            self._elapsed_seconds = self.end_time - self.start_time
        return round(self._elapsed_seconds, 2)

    @elapsed_seconds.setter
    def elapsed_seconds(self, elapsed_sec):
        self._elapsed_seconds = elapsed_sec

    def start(self) -> float:
        """
        Methods starts the time measure while also logging it with the passed logging_function.

        Returns:
            float: Unix timestamp at start of measuring.
        """
        self.logging_function("Time measure: Started.")
        self.start_time = datetime.now().timestamp()
        return self.start_time

    def stop(self) -> int:
        """
        Method stops the time measure and outputs the elapsed time, also returning the elapsed seconds.

        Returns:
            int: Elapsed time in seconds.
        """
        self.end_time = datetime.now().timestamp()
        self.elapsed_seconds = int(self.end_time - self.start_time)
        self.logging_function(
            f"Time measure: Ended, total time: {TimeMeasure.seconds_to_time_string(self.elapsed_seconds)}."
        )
        return self.elapsed_seconds

    @staticmethod
    def seconds_to_time_string(seconds) -> str:
        """
        Method converts seconds into time in the format hh:mm:ss. Returns a string

        Returns:
            str: Time in the format hh:mm:ss
        """
        return str(timedelta(seconds=seconds)).split(".")[0]  # Chop off microseconds/milliseconds
