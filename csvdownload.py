#!/usr/bin/python
# -*- coding: utf-8 -*-

from clevertap import CleverTap
import argparse
import datetime
import json
import csv

MAX_BATCH_SIZE = 5000



def main(account_id, passcode, region, path_json, path_csv, type_of_download):

    clevertap = CleverTap(account_id, passcode, region=region)
    result = []

    if type_of_download not in ["event", "profile"]:
        raise Exception("unknown record type %s" % type)
        return

    start_time = datetime.datetime.now()
    print("Downloading...")
    try:
        with open(path_json) as data_file:
            data = json.load(data_file)
        if type_of_download == "profile":
            clevertap.profiles(data, MAX_BATCH_SIZE)
        elif type_of_download == "event":
            clevertap.events(data, MAX_BATCH_SIZE)

    except Exception as e:
        print(e)

    finally:
        end_time = datetime.datetime.now()
        processing_time = end_time - start_time
        print(("Processing Time: %s" % processing_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CleverTap CSV downloader')
    parser.add_argument('-a', '--id', help='CleverTap Account ID', required=True)
    parser.add_argument('-c', '--passcode', help='CleverTap Account Passcode', required=True)
    parser.add_argument('-r','--region', help='Your dedicated CleverTap Region', required=False)
    parser.add_argument('-pjson', '--pathjson', help='Absolute path to the json file', required=True)
    parser.add_argument('-pcsv', '--pathcsv', help='Absolute path to the csv file', required=True)
    parser.add_argument('-t', '--type', help='The type of data, either profile or event, defaults to profile',
                        default="profile")

    args = parser.parse_args()

    main(args.id, args.passcode, args.region, args.pathjson, args.pathcsv, args.type)
