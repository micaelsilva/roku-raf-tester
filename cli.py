import sys
import json
import argparse
from enum import Enum

import requests

import ssdp


class Fmt(Enum):
    Auto = "Auto"
    DASH = "DASH"
    HLS = "HLS"


class Drm(Enum):
    Widevine = "Widevine"
    Playready = "Playready"


class RAF:
    def __init__(self, ip=None):
        if ip:
            self.ip = ip
        else:
            try:
                self.ip, _ = self.scan()
            except Exception as e:
                print(e)
                sys.exit(1)

        self.HTTP_PARAMS = {
            "live": "true",
            "autoCookie": "false",
            "debugVideoHud": "false",
            "url": "",
            "fmt": "DASH",
            "drmParams": {
                "drmParams": {
                    "name": "Widevine",
                    "licenseServerURL": "",
                    "serializationUrl": "",
                    "licenseRenewUrl": "",
                    "appData": ""
                }
            },
            "headers": '{}',
            "metadata": '{"isFullHD":false}',
            'cookies': "[]"
        }

    def scan(self):
        devices = ssdp.get_devices(
            st="roku:ecp",
            field='friendlyName',
            name="Roku")
        if len(devices) == 0:
            raise Exception("No devices found")
        elif len(devices) == 1:
            return devices[0]
        else:
            list_devices = {str(x): y for x, y in enumerate(devices)}
            for i in list_devices.items():
                print(f"{i[0]}: {i[1][1]} - {i[1][0]}")
            id_ = input("Select number of the device: ")
            return devices[int(id_)]

    def send(self):
        params = self.HTTP_PARAMS.copy()
        params["drmParams"] = json.dumps(params["drmParams"])
        try:
            r = requests.post(
                f"http://{self.ip}:8060/launch/63218",
                params=params,
                timeout=5)
        except Exception as e:
            print(e)
        else:
            print(r.text)


def main():
    parser = argparse.ArgumentParser(
        prog='rokuraftester',
        description='Send commands to a Roku device to test streams')
    parser.add_argument(
        '--ip',
        default=False,
        help='IP of the device')
    parser.add_argument(
        '--url',
        default=None,
        help='URL of the stream')
    parser.add_argument(
        '--format',
        default=None,
        help='Stream format')
    parser.add_argument(
        '--lic',
        default=False,
        help='License server')
    parser.add_argument(
        '--drm',
        default=False,
        help='DRM format (Widevine or Playready)')
    parser.add_argument(
        '--hud',
        action='store_true',
        default=False,
        help='Show HUD')
    parser.add_argument(
        '--mediaplayer',
        action='store_true',
        default=False,
        help='Get media player info')

    args = parser.parse_args()

    raf = RAF(ip=args.ip if args.ip else None)

    if args.url:
        raf.HTTP_PARAMS["url"] = args.url

    if args.format:
        try:
            raf.HTTP_PARAMS["fmt"] = Fmt(args.format).name
        except Exception:
            print("Invalid format option")

    if args.lic:
        raf.HTTP_PARAMS["drmParams"]["drmParams"]["licenseServerURL"] = args.lic

    if args.drm:
        raf.HTTP_PARAMS["drmParams"]["drmParams"]["name"] = args.drm

    if args.hud:
        raf.HTTP_PARAMS["debugVideoHud"] = "true"

    if args.mediaplayer:
        try:
            r = requests.get(
                f"http://{raf.ip}:8060/query/media-player",
                timeout=5)
        except Exception as e:
            print(e)
        else:
            print(r.text)
    else:
        params = raf.HTTP_PARAMS.copy()
        params["drmParams"] = json.dumps(params["drmParams"])
        try:
            r = requests.post(
                f"http://{raf.ip}:8060/launch/63218",
                params=params,
                timeout=5)
        except Exception as e:
            print(e)
        else:
            print(r.text)


if __name__ == "__main__":
    main()
