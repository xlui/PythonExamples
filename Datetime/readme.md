# datetime

> datetime  
> datetime.now  
> datetime.timestamp  
> datetime.fromtimestamp  
> datetime.utcfromtimestamp  
> datetime.strptime  
> strftime.strftime

```py
>>> import datetime
>>> datetime.datetime(2017, 11, 25, 18, 35)
datetime.datetime(2017, 11, 25, 18, 35)
>>> now = datetime.datetime.now()
>>> now
datetime.datetime(2017, 11, 25, 18, 36, 9, 950934)
>>> timestamp = now.timestamp()
>>> timestamp
1511606169.950934
>>> datetime.datetime.fromtimestamp(timestamp)
datetime.datetime(2017, 11, 25, 18, 36, 9, 950934)
>>> datetime.datetime.utcfromtimestamp(timestamp)
datetime.datetime(2017, 11, 25, 10, 36, 9, 950934)
>>> datetime.datetime.strptime('2017-11-25 18:37:00', '%Y-%m-%d %H:%M:%S')
datetime.datetime(2017, 11, 25, 18, 37)
>>> now.strftime('%a, %b %d %H:%M')
'Sat, Nov 25 18:36'
```