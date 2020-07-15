import pandas as pd
import json
from mongodb  import getdbData

def get(Datafrom):
    return getdbData(colection=Datafrom)