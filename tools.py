#============================================================================================================================================================
# Author:	   Erika Fonseca
# Create date: 31/03/2020
# Description:	Useful functions that are going to be used in the project
#============================================================================================================================================================

import sys
import datetime
import configparser
import subprocess

try:
    import pip
except:
    subprocess.call([sys.executable, "-m", "python", "ensurepip", "--default-pip"])

def install_package(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    import pyodbc
except ImportError as error_msg:
    package = str(error_msg).split("'")[-2]
    install_package(package)
    __import__(package)

try:
    import pandas as pd
except ImportError:
    install_package("pandas")
    import pandas as pd


def get_config():
    
    config = configparser.ConfigParser()

    try:
        config.read(r'Config.ini')
    except:
        print('Attention: error trying to open the Config.ini file!')
        sys.exit("Unable to find INI file")

    return config

       
def connect_SQL():
    
    config = get_config()

    Server = config['SQLSERVER']['Server']
    DB = config['SQLSERVER']['Database']

    connectionString = 'DRIVER={ODBC Driver 13 for SQL Server}; SERVER='+Server+';DATABASE='+DB+';Trusted_Connection=yes'
    try:
        sql_conn = pyodbc.connect(connectionString) 

    except:
        print('Attention: error trying to connect to database! Try to modify the "Config.ini" with the database location or check if the database is running.')
        sys.exit("Fail to connect to DB")

    return (sql_conn)

def read_structure():

    config = get_config()

    path = config['PATHS']['config']

    try:
        df_structure = pd.read_csv(path+'\structure.csv')  
    except:
        df_structure = None

    return df_structure

def save_report(df, type, name):

    config = get_config()

    if type == "report":
        path = config['PATHS']['report']
    else:
        path = config['PATHS']['config']

    try:
        df.to_csv(path + '\\' + name+ r'.csv')
    except:
        print('Attention: error trying to save file on ', path ,'! Try to modify the "Config.ini" with a different location or check if the location is read-only.')
        if type =='report':
            sys.exit("Unable to save report")