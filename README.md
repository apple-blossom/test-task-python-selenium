####How to install project requirements:
1. Create and activate virtualenv:
	- Open command line and enter `pip install virtualenv`
	- Create virtual environment by `virtualenv venv-name`
	- Activate virtual environment by: 
		- Windows `venv-name\Scripts\activate.bat`;
		- MacOS, Linux `source venv-name/bin/activate`
2. Run `pip install -r requirements.txt`

####To run UI tests:
`pytest --tb=short ./ui_suite_test.py`

####Remarks:
1. All tests are run in headless mode by default
2. I've chosen the approach to store locators as class fields not in a separate class as it seems more logical to me
3. I've split first test in two - first is user creation flow, second is purchasing a product flow as is reduces test flakiness