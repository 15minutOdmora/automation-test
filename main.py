"""
Main execution module, executes test case using MultiProcessing on every available driver.
"""

from concurrent import futures
from datetime import date

from test_expandable import test_expandable
from usefull.driver import AvailableBrowserDrivers
from usefull.helpers import create_csv_file, append_to_csv_file


# Get all available browser drivers, so the test can be executed on each one
drivers = list(AvailableBrowserDrivers.values())


def main(repeat: int = 1):
    """
    Executes the test_example_scenario 'repeat' times using multiprocessing. Saves test data to a csv file in the
    test_history directory.

    Args:
        repeat (int): Number of times to repeat the test.
    """
    date_formated = date.today().strftime("%d_%m_%Y")
    filename = f"test_history/{test_expandable.__name__}_{date_formated}.csv"
    header = ["Passed", "Browser", "Execution time", "Error", "Filename", "Line", "Function", "Error code"]
    # Create csv file, add header
    create_csv_file(filename, header)

    for _ in range(repeat):
        with futures.ProcessPoolExecutor() as executor:
            res = list(executor.map(test_expandable, drivers))
            append_to_csv_file(filename, res)


if __name__ == "__main__":  # Needed for ProcessPoolExecutor
    main(repeat=1)
