import json
import argparse
import requests
import ssdp


class RAF:
    def __init__(self, ip=None):
        if ip:
            self.ip = ip
        else:
            self.ip, self.device_name = self.scan()

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
        if len(devices) == 1:
            return devices[0]

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

    raf = RAF(ip=args.ip if args.ip else None)

    if args.name:
        print(raf)

    if args.mediaplayer:
        try:
            r = requests.get(
                f"http://{raf.ip}:8060/query/media-player",
                timeout=5)
        except Exception as e:
            print(e)
        else:
            print(r.text)


if __name__ == "__main__":
    main()
