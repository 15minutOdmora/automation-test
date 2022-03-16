# Test automation homework

**Test Environment:**

- Language: Python (3.8)
- Platform: Windows
- Browsers: Chrome, Firefox

I only used the Selenium library (and others that come with it). It might seem like a lot of code for one test case, but I 
tried to make it extendable so in case more tests would be added some functionality would be reusable.

I recycled some code from older unfinished projects.

Before running the code please install needed drivers (chrome and gecko). The executables should be placed into their 
own folder in the `drivers/` directory.

#### A) Making script browser independent

Module `usefull/driver.py` contains driver class implementations. The BaseDriver class holds methods 
that are useful or just used a lot. Then there are two classes ChromeDriver and FirefoxDriver which inherit from the
above mentioned BaseDriver and from their own Selenium Webdriver classes (Chrome and Firefox). Both classes have the same
attributes and extend the parent drivers functionality making their usage more dynamic and user friendly. 

#### B) Parallel execution

Implemented using MultiProcessing (ProcessPoolExecutor seen in the `main.py` file). The script takes all available 
drivers and executes the test script on each one. 

I could also use some third party library that simplifies (or improves) parallel execution. 
Selenium Grid or just executing the file multiple times from a Bash script would also work.

#### C) Reporting

Normally I'd use logging functionality to save execution output into log files and some sort of file storage system to save
previous execution data (database, server-side files, ...). 
On top of that I'd use a testing library such as the standard Python Unittest or an open source one such as Pytest.

In this example I implemented my own saving functionality into a csv file. If the test fails it saves some data about the error.
The data saved (from me testing the script) can be found in the csv file located in `test_history/`. It contains some
failed tests, which were forcefully failed by me to see the output. 

For example:
The two rows located at lines `24` and `25` in the csv file occurred when I removed line `36` in the `test_expandable.py` file.
That failed the test as the modal didn't open in time.
