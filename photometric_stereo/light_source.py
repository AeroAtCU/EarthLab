# get normal vectors of sun direction

from pysolar.solar import  *
import datetime

# date = datetime.datetime(2019, 8, 8, 10, 18, 1, 130320, tzinfo=datetime.timezone.utc)
# date = datetime.datetime(tzinfo=datetime.timezone.utc)
date = datetime.datetime(2019, 8, 8, tzinfo=datetime.timezone.utc)
date = datetime.datetime.now()

print(get_azimuth(40.206, -105.382, date))

