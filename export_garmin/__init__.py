#!/usr/bin/env python3
"""
export EMAIL=<your garmin email>
export PASSWORD=<your garmin password>

"""
from datetime import datetime
import logging
import os
import re
from getpass import getpass

import requests
from garth.exc import GarthHTTPError

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

# Load environment variables if defined
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
exportpath = os.getenv("GARMIN_EXPORT_PATH") or "./export"

# Configure debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = None


def get_credentials():
    """Get user credentials."""

    email = input("Login e-mail: ")
    password = getpass("Enter password: ")

    return email, password


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    try:
        # Using Oauth1 and OAuth2 token files from directory
        print(
            f"Trying to login to Garmin Connect using token data from directory '{tokenstore}'...\n"
        )

        garmin = Garmin()
        garmin.login(tokenstore)

    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        print(
            "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        )
        try:
            # Ask for credentials if not set as environment variables
            if not email or not password:
                email, password = get_credentials()

            garmin = Garmin(email, password)
            garmin.login()
            # Save Oauth1 and Oauth2 token files to directory for next login
            garmin.garth.dump(tokenstore)
            print(
                f"Oauth tokens stored in '{tokenstore}' directory for future use.\n"
            )
        except (
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectAuthenticationError,
            requests.exceptions.HTTPError,
        ) as err:
            logger.error(err)
            return None

    return garmin


def main():
    # Initialize everything
    api = init_api(email, password)
    latest = datetime.min.strftime("%Y-%m-%d")
    if os.path.exists(exportpath):
        exports = sorted(
            [d for d in os.listdir(exportpath) if re.match(r"\d{4}-\d{2}-\d{2}", d)]
        )
        if exports:
            latest = exports[-1]
    
    # Get last exported activity day. Worst case, we overwrite a couple of activities.
    startdate = latest + "T00:00:00.000000"
    enddate = datetime.now().isoformat()
    print(f"Fetching activities from {latest}...")
    activities = api.get_activities_by_date(startdate, enddate)
    for activity in activities:
        outdir = os.path.join(exportpath, activity["startTimeGMT"][:10])
        print(f"Downloading {activity['startTimeGMT'][:10]}...")
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        outfile = os.path.join(outdir, str(activity["activityId"])) + ".tsx"
        raw = api.download_activity(activity["activityId"])
        with open(outfile, "wb") as out:
            out.write(raw)
