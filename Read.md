# Project Title
Generates a report with a map of all the answers to surveys by user, having the question in columns.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisites
1- SQL Server database with the following structure:
    - dbo.Answer
    
    - dbo.Question
    
    - dbo.Survey
    
    - dbo.SurveyStructure
    
    - dbo.User   

2- Python interpreter to run the script
3- Folder with write permission to save reports
4- Folder with write permission to save configurations

## Installing
- Put the generateSurveyReport.py and Config.ini at the same folder
- Configure the ini file to set the database location, and the folders to store configuration and reports files

## Running the Tests
Running the generateSurveyReport.py and check if it ran successfully, if not check the error messages

```
Remark: the access to the database is made using Windows authentication, so make sure the user running the code 
has privilleges to log in the SQL Server and access the database and its content.
```

# Authors
Erika Fonseca - Initial work - Data Wrangling Assignment
