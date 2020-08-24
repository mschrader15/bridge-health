#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='db_migrate', url='mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC+Driver+17+for+SQL+Server%7D%3BSERVER%3Dtcp%3Ahanson-bridge-monitor.database.windows.net%3BDATABASE%3DHanson-Bridge-Monitor%3BUID%3Dmcschrader%3BPWD%3Dbr1dge-health', debug='False')
