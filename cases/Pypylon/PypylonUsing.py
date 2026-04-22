# nuitka-project: --mode=app-dist

import os

os.environ["PYLON_CAMEMU"] = "3"

from pypylon import pylon


def main():
    tl_factory = pylon.TlFactory.GetInstance()

    device_info = pylon.DeviceInfo()
    device_info.SetDeviceClass("BaslerCamEmu")

    transport_layers = tl_factory.EnumerateTls()
    devices = tl_factory.EnumerateDevices([device_info])

    print("TLS", len(transport_layers))
    print("DEVICES", len(devices))

    if not devices:
        raise RuntimeError("Expected at least one emulated pypylon device.")

    camera = pylon.InstantCamera(tl_factory.CreateFirstDevice(device_info))
    camera.Open()

    try:
        device_info = camera.GetDeviceInfo()
        print("MODEL", device_info.GetModelName())
        print("VENDOR", device_info.GetVendorName())
    finally:
        camera.Close()


if __name__ == "__main__":
    main()
