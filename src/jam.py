from StreamDock.DeviceManager import DeviceManager
import threading
import time
import subprocess
import os

def press_media_key(key):
    """Simulate media key press"""
    subprocess.run(['xdotool', 'key', key])

def press_key_combo(keys):
    """Simulate complex key combination"""
    subprocess.run(['xdotool', 'key', '+'.join(keys)])

def setup_images(device):
    """Set up initial button images"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(script_dir, "media_images")
        
        device.clearAllIcon()
        
        device.set_key_image(1, os.path.join(image_dir, "icons8-rewind-100.png"))
        device.set_key_image(2, os.path.join(image_dir, "icons8-resume-button-100.png"))
        device.set_key_image(3, os.path.join(image_dir, "icons8-fast-forward-100.png"))
        device.set_key_image(4, os.path.join(image_dir, "icons8-audio-100.png"))
        device.set_key_image(5, os.path.join(image_dir, "icons8-headphones-100.png"))
        device.set_key_image(6, os.path.join(image_dir, "icons8-mute-100.png"))
        
        device.refresh()
        
        print("Images set successfully")
    except Exception as e:
        print(f"Error setting images: {e}")

def set_noba_mode(device):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(script_dir, "media_images")
        
        device.clearAllIcon()
        
        for i in range(1, 7):
            device.set_key_image(i, os.path.join(image_dir, "noba.jpeg"))
        
        
        device.refresh()
        
        print("Images set successfully")
    except Exception as e:
        print(f"Error setting images: {e}")

def brightness_controller(device, last_activity_time, dim_timeout=30):
    """Separate thread to handle screen brightness based on activity"""
    screen_dimmed = False
    
    while True:
        try:
            current_time = time.time()
            time_since_activity = current_time - last_activity_time[0]  # Get the shared value
            
            if not screen_dimmed and time_since_activity > dim_timeout:
                device.set_brightness(10)
                screen_dimmed = True
                device.refresh()
            elif screen_dimmed and time_since_activity < dim_timeout:
                device.set_brightness(50)
                screen_dimmed = False
                device.refresh()
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error in brightness controller: {e}")
            break

def custom_whileread(device, last_activity_time):
    noba_mode = False
    
    while True:
        try:
            result = device.read()
            
            if result and len(result) >= 5:
                data, ack, ok, key, status = result
                
                last_activity_time[0] = time.time()
                
                if key not in [80, 81]:
                    if key == 2:
                        press_media_key('XF86AudioPlay')
                        print("Play/Pause triggered")
                    elif key == 1:
                        press_media_key('XF86AudioPrev')
                        print("Previous track triggered")
                    elif key == 3:
                        press_media_key('XF86AudioNext')
                        print("Next track triggered")
                    elif key == 52:
                        if(noba_mode):
                            setup_images(device)
                            noba_mode = False
                        else:
                            set_noba_mode(device)
                            noba_mode = True
                        print("Noba mode triggered")
                    elif key == 4:
                        press_key_combo(['ctrl', 'alt', 'l'])
                        print("Ctrl+Shift+L triggered")
                    elif key == 5:
                        press_key_combo(['ctrl', 'alt', 'h'])
                        print("Ctrl+Shift+H triggered")
                    elif key == 6:
                        press_media_key('XF86AudioMute')
                        print("Mute triggered")
                elif key in [80, 81]:
                    if key == 81:
                        press_media_key('XF86AudioRaiseVolume')
                        print("Volume up")
                    else:
                        press_media_key('XF86AudioLowerVolume')
                        print("Volume down")

        except Exception as e:
            print(f"Error in whileread: {e}")
            break

if __name__ == "__main__":
    manner = DeviceManager()
    streamdocks = manner.enumerate()
    
    listener_thread = threading.Thread(target=manner.listen)
    listener_thread.start()
    
    print("Found {} Stream Dock(s).\n".format(len(streamdocks)))
    
    for device in streamdocks:
        device.open()
        device.wakeScreen()
        device.set_brightness(50)
        
        setup_images(device)
        
        last_activity_time = [time.time()]

        reader_thread = threading.Thread(target=lambda: custom_whileread(device, last_activity_time))
        reader_thread.daemon = True
        reader_thread.start()
        
        brightness_thread = threading.Thread(target=lambda: brightness_controller(device, last_activity_time, dim_timeout=30))
        brightness_thread.daemon = True
        brightness_thread.start()
        print("\nDevice ready for media control!")
        print("------------------------")
        print("Button 1: Previous Track")
        print("Button 2: Play/Pause")
        print("Button 3: Next Track")
        print("Button 4: Volume Up")
        print("Button 5: Volume Down")
        print("Button 6: Mute")
        print("Dial: Volume Control")
        print("------------------------")
        
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")
            break