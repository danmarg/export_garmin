# Export Garmin

Export all your Garmin Connect activity as TSX. Tries to do so efficiently by
incrementally downloading since last sync.

Usage:
```
$ pip3 install git+https://github.com/danmarg/export_garmin.git
$ EMAIL=<your_email> \
  PASSWORD=<your password> \
  GARMIN_EXPORT_PATH=<garmin_sync_path> \
  python3 export_garmin.py
```

