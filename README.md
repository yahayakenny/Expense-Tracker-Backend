# Expense-Tracker-Backend

Simple expense tracker built with django rest framework, redux and react to help me track and manage my expenses.
Please ensure you have python installed. I used python 3.9 for this project

1. Please note that all installations were done using 'pipenv install <package-name>' instead of 'pip install'
2. Hence ensure you have pipenv installed,
3. To do this, ensure you have python installed already, then run 'pip install pipenv'
4. confirm pipenv has been installed by running 'pipenv --version'
5. If you get the following error, 'pipenv shell 'pipenv' is not recognized as an internal or external command, operable program or batch file.', this means you need to set up pipenv in your global environmental variables on your windows laptop,
6. Follow the instructions in this link 'https://stackoverflow.com/questions/61742227/pipenv-is-not-recognized-on-powershell';
7. Close and Reopen the CMD, and type 'pipenv --version' again, you should now get the version 'pipenv, version 2020.11.15'
8. Now cd into the folder, the virtual environment is set up here, enclosing the backend folder
9. Run 'pipenv shell' to activate the virtual environment
10. Run 'pipenv install --dev' to install all the backend project dependencies as defined in the 'Pipfile.lock' file
11. Launch the project using 'python manage.py runserver'
