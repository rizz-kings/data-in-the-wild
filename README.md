# data-in-the-wild / rizz-kings
This is the GitHub repo associated with group rizz-kings' final exam project for course:<br> **KSDWWVD1KU**/*Data In The Wild: Wrangling And Visualising Data*. <br>
<br>
**This repo contains all code- and data used to produce the final report.**

#### Data
The data used for this project is collected from two types of sources: 
- Movie Review Sites
- Movie Metadata Databases
<br>
All movie reviews across different sites are stored in: <br> https://github.com/rizz-kings/data-in-the-wild/blob/main/data/processed/all_reviews.csv <br>
Movie metadata is stored in: <br> https://github.com/rizz-kings/data-in-the-wild/tree/main/data/processed/movie_stats <br>

#### Notebooks

The notebooks folder contains notebooks used in every step of the project. <br> imdb_reviews.ipynb is the main notebook used to gather all reviews from imdb.com. <br>
<br>
Most Notebooks within this folder should have self-explanatory names. <br>

#### Scripts
The scripts folder contains .py files mainly used in the data collection process. <br>

#### Versions
All notebooks were tested to run with Python version 3.10.13 and the package versions in requirements.txt. When testing the installation of all requirements.txt files on another device we ran into issues, so we suggest when wanting to run a given notebook installing any missing imports on the go and specifying the package versions found in the requirements.txt file. <br>

Note that due to Selenium funkiness, the relevant Selenium drivers may need to be installed, and Selenium python package pip installed.
