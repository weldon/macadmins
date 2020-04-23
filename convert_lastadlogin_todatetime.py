from datetime import datetime

string = "adDateLastConnected: Thursday, August 23, 2018 at 12:00:07 AM"
timestamp = datetime.strptime(string, "adDateLastConnected: %A, %B %d, %Y at %I:%M:%S %p")
print(timestamp.tzinfo)
dt = timestamp.replace(tzinfo=timezone.utc)
print(dt)