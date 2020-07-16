# importing tick data using duka

import duka.app.app as import_ticks_method
from duka.core.utils import TimeFrame
import datetime
import pandas as pd

#elements to import data from duka
start_date =  datetime.date (20110,1,1)
end_date =  datetime.date (2020,5,30)
Assets = ["AUDUSD"]
import_ticks_method (Assets, start_date, end_date, 1, TimeFrame.H1, ".", True)
