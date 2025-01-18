import ui
import dialogs
import ssdp
import requests
import json
from enum import Enum
from console import hud_alert

import urllib.parse
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

def find_device(ctx, indicator=None):
  if indicator:
    indicator.start()
  global CASTIP
  devices = ssdp.get_devices(st="roku:ecp", field='friendlyName', name="Roku")
  if not devices:
    #ctx["devices_btn"].enabled = False
    ctx["devices_btn"].title = "No device found"
  elif len(devices) == 1:
    ctx["devices_btn"].title = f"{devices[0][1]}: {devices[0][0]}"
    CASTIP = devices[0][0]
  else:
    selector = dialogs.list_dialog(title='Devices found:', items=[f"{i[1]}: {i[0]}"
                 for i in devices])
    if selector:
      items = selector.split(": ")
      ctx["devices_btn"].title = f"{items[1]}: {items[0]}"
      CASTIP = items[1]
  if indicator:
    indicator.stop()

class Fmt(Enum):
  Auto = 0
  DASH = 1
  HLS = 2
  
def select_fmt(ctx):
  global HTTP_PARAMS
  if Fmt(ctx.selected_index) == Fmt.Auto:
    HTTP_PARAMS["fmt"] = "Auto"
  elif Fmt(ctx.selected_index) == Fmt.DASH:
    HTTP_PARAMS["fmt"] = "DASH"
  elif Fmt(ctx.selected_index) == Fmt.HLS:
    HTTP_PARAMS["fmt"] = "HLS"

def select_tab(ctx, new_tab):
  global SUBVIEW
  ctx.superview.remove_subview(SUBVIEW)
  SUBVIEW = ui.load_view(f'tab_{new_tab}')
  SUBVIEW.frame = ctx.superview["subviews"].frame
  ctx.superview.add_subview(SUBVIEW)

def segmented_control(ctx):
  select_tab(ctx, ctx.selected_index)

def button_press(sender):
  global HTTP_PARAMS
  global INDICATOR
  if sender.name == "devices_btn":
    find_device(sender.superview, INDICATOR)
  elif sender.name == "textfield_url":
    HTTP_PARAMS["url"] = sender.text
  elif sender.name == "islive_switch":
    HTTP_PARAMS["live"] = str(sender.value).lower()
  elif sender.name == "hashud_switch":
    HTTP_PARAMS["debugVideoHud"] = str(sender.value).lower()
  elif sender.name == "license_url":
    HTTP_PARAMS["drmPrams"]["drmParams"]["licenseServerURL"] = sender.text
  elif sender.name == "serialization_url":
    HTTP_PARAMS["drmPrams"]["drmParams"]["serializationUrl"] = sender.text
  elif sender.name == "renew_url":
    HTTP_PARAMS["drmPrams"]["drmParams"]["licenseRenewUrl"] = sender.text
  elif sender.name == "app_data":
    HTTP_PARAMS["drmPrams"]["drmParams"]["appData"] = sender.text

def play(ctx):
  if not CASTIP:
    hud_alert('No device found')
    return None
  params = HTTP_PARAMS.copy()
  params["drmParams"] = json.dumps(params["drmParams"])
  try:
    r = requests.post(f"http://{CASTIP}:8060/launch/63218", params=params, timeout=5)
  except Exception as e:
    print(e)
  else:
    print(r.text)

def main():
  v = ui.load_view('main')
  global SUBVIEW
  SUBVIEW = ui.load_view('tab_0')
  SUBVIEW.frame = v["subviews"].frame 
  v.add_subview(SUBVIEW)
  v.present()
  
  global INDICATOR
  INDICATOR = ui.ActivityIndicator()
  INDICATOR.x, INDICATOR.y = (12, 12)
  v.add_subview(INDICATOR)
  find_device(v, INDICATOR)
 
if __name__ == '__main__':
  main()

