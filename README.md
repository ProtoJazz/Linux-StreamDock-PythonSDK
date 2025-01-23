```
# Linux-x86_64 platform
### It is recommended to use Python 3 or above. Test environment: Ubuntu 20.04, Python 3.8.10

You need to install `pillow`, `pyudev`, `threading`, `ctypes`, `time`, `abc`

```bash
pip install pillow
```

Alternatively, the following libraries may already be included in your Python version and do not need to be installed:

```bash
pip install pyudev
```
```bash
pip install threading
```
```bash
pip install ctypes
```
```bash
pip install time
```
```bash
pip install abc
```

### Install Linux Software

If you want to install them one by one, please pay attention to the installation order: libusb-1.0-0-dev needs to be installed before libhidapi-libusb0.
If you encounter the error "undefined reference to `get_input_report()`", you can replace the `/usr/local/lib/libhidapi-libusb.so.0`file with the`libhidapi-libusb.so.0` file we provided in the Transport folder.

```
sudo apt install -y libudev-dev libusb-1.0-0-dev libhidapi-libusb0
```

When using it, you need to first define a `DeviceManager` class object (device manager class), and then call its `enumerate()` function to traverse the devices and obtain a list of device objects.

```py
manner = DeviceManager();
streamdocks = manner.enumerate();
```

After obtaining the list of device objects, you need to call the `open()` method to open the device before calling other methods to operate on the device.

**~~Note! When using `set_touchscreen_image()` and `set_key_image()`, the image format must be JPEG.~~ **However**, in the new version, you don't need to worry about the image size details. The SDK will handle them for you internally.**
**~~Additionally, the `set_touchscreen_image()` function requires a fixed image size. For example, the size for the 293V3 is 800x480. The `set_key_image()` function also accepts a fixed size, such as 112x112 for the 293V3. For specific sizes, please refer to the~~**[documentation](https://creator.key123.vip/en/windows/websocket/events-sent.html#setkeyimg)and[documentation](https://creator.key123.vip/en/windows/websocket/events-sent.html#setbackgroundimg)

```py
for device in streamdocks:
        # 打开设备
        device.open()
        device.wakeScreen()
        # 开线程获取设备反馈
        t = threading.Thread(target=device.whileread)
        t.daemon = True # detach
        t.start()
        # 设置设备亮度0-100
        device.set_brightness(50)
        # # 设置背景图片（传图片的地址）
        # device.clearAllIcon()
        for i in range(1000):
            res = device.set_touchscreen_image("../img/YiFei320.png")
            device.refresh()
            time.sleep(2)
            device.clearAllIcon()
            for i in range(10):
                device.set_key_image(i + 1, "../img/tiga64.png")
            device.refresh()
            time.sleep(2)
        # 清空某个按键的图标
        device.cleaerIcon(3)
        time.sleep(1)
        # 清空所有按键的图标
        # device.clearAllIcon()
        device.refresh()
        # time.sleep(1)
        # 关闭设备
        # device.close()
    time.sleep(10000)
```
