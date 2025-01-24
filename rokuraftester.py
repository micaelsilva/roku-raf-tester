import ssdp
import requests
import json
import argparse

CASTIP = ""
HTTP_PARAMS = {
  "live": "true",
  "autoCookie": "false",
  "debugVideoHud": "false",
  "url": "",
  "fmt": "DASH",
  "drmParams": {"drmParams":{"name":"Widevine","licenseServerURL":"","serializationUrl":"","licenseRenewUrl":"","appData":""}},
  "headers": '{}',
  "metadata": '{"isFullHD":false}',
  'cookies': "[]"
}

def scan():
  devices = ssdp.get_devices(st="roku:ecp", field='friendlyName', name="Roku")
  return devices

def main():
    parser = argparse.ArgumentParser(
        prog='rokuraftester',
        description='Send commands to a Roku device to test streams')
    parser.add_argument(
        '--ip',
        default=False,
        help='IP of the device')
    parser.add_argument(
        '--connect',
        action='store_true',
        default=None,
        help='Connect to a new network')
    parser.add_argument(
        '--name',
        default=None,
        help='Change the Chromecast device name')
    parser.add_argument(
        '--list',
        action='store_true',
        default=False,
        help='List configured networks')
    parser.add_argument(
        '--forget',
        action='store_true',
        default=False,
        help='Forget configured network')
    parser.add_argument(
        '--mediaplayer',
        action='store_true',
        default=False,
        help='Get media player info')

    args = parser.parse_args()

    if args.name:
        print(a.set_name(args.name))

    if args.mediaplayer:
        # query/media-player


if __name__ == "__main__":
    main()
