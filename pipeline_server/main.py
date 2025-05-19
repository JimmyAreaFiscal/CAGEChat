"""

This module is responsible for running a pipeline server for uploading documents to the database. 
This is a simple server that, given a command, will execute the croresponding pipeline and upload the documents in the "arquivos" folder. 

"""

import os 
import requests 


files = os.listdir("arquivos")


