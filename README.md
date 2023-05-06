# poop-meter

Source code and design for the ultrasnoic septic tank monitor and main water shutoff.

* Doc: Documentation and technical notes.
* Deprecated Arduino and Perl code for the previous incarnation.
* Poop-Valve: Schematic for the water main shutoff valve.
* etc: Support files (Raspberry Pi startup script, crontab).
* src: Python source code.

## TL;DR

Tracks the depth of the effluent in the septic holding tank. Notifies a human (SMS text)
at intervals, more frequently as the tank gets more full.  Shuts off the main water valve
if the tank gets to a panic level.

## Notable Notes

Softwasre dependencies are spelled out in `poopWatcher.py`, but we also need a confguration file
that tells us how to authenticat with Twilio to send text messages.  This file can reside `twilio.conf`
tin any of the curerent directory, in './etc/twilio.conf', or in '/usr/local/etc/twilio.conf'.  For
security reasons this file is not in the repository.  Create the file and fill out at least the
`[twilio]` section and add users to the `recippint` section.

```
[twilio]
account_sid = **********************************
auth_token  = ********************************
from_phone = +1xxxyyyzzzz

[recipient]
dave = +1xxxyyyzzzz
```

A more detailed explanation is forthcoming.

## Detailed Design

Super high level: we are multi-threaded and are a mix between polled and GPIO event driven threads.
A side effect of this is that software bugs do not generally cause fatal errors.  Polling is handled
by `poop.Poop.perSecond` which, first thing, schedules itself to run again in one second.  It then,
as prescribed by the `interval` dictionary, dispatches an ADC sample of the poop tank, flashes the
heartbeat LED, prints a status report to the log, does housekeeping, and decides if we need to page
or open/close the mains valve. Simple, no?

![Poop meter schematic](Doc/Schematic.jpg)

![Poop meter internals](Doc/Poop-meter-internals.jpg)
