# Setup
# There is an api that produces all stations in map bound
# We must make n api calls over x min to gather all samples
import os
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv("TOKEN")

latitude_1 = 39.379436
longitude_1 = 116.091230
latitude_2 = 40.235643
longitude_2 = 116.784382
