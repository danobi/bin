#!/usr/bin/env python3

import notify2

notify2.init("rest-eyes")
n = notify2.Notification("Rest your eyes", "Try to look away for 20s")
n.show()
