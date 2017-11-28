#!/usr/bin/env python3

import datetime
import sys
import notify2

# Only notify during work hours
now = datetime.datetime.now()
hour = now.hour
if hour < 9 or hour > 19:
    sys.exit(0)

notify2.init("rest-eyes")
n = notify2.Notification("Rest your eyes", "Try to look away for 20s")
n.show()
