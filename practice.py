import datetime
from dateutil.relativedelta import relativedelta


start_date=datetime.date(2023,11,2)
next_month=start_date+relativedelta(month=1)
print(next_month)