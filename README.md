# OwnTracks Backfill from Home Assistant

This is a utility that I made to take location data from a device_tracker entity, the Home Assistant mobile app on iOS in my case, and use it as additional data points for OwnTracks.

To use this, you will need to create a `.env` file with the following entries (adjusted for your setup, naturally):

```bash
HA_URL="http://homeassistant.local:8123"
HA_PERIOD_START="2022-01-01T00:00:00+05:00"
HA_PERIOD_END="2023-11-27T00:00:00+05:00"
HA_ENTITIES="device_tracker.mobile_app"
HA_TOKEN="some long lived token created under your profile"
OT_USER="gene"
OT_DEVICE_ID="phone"
OT_TID="XX"
OT_URL="https://ot.example.com/pub"
OT_AUTH_USER="gene"
OT_AUTH_PASS="your basic auth password"
```

These steps can be used to setup dependencies:

```bash
python3 -m venv .venv                      
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```
