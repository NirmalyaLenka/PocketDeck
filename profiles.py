# profiles.py
# PocketDeck - Button profiles and action mappings
#
# This is the main file you will edit to customize what each button does.
#
# HOW TO READ THIS FILE
# ─────────────────────
# PROFILES is a dictionary.
# Each key is a profile name (any string you like).
# Each value is another dictionary mapping button numbers to actions.
#
# Button numbers go from 1 to 16.
# Button 16 is reserved as the profile-switching button and will be ignored here.
#
# An action is a tuple with two parts:
#   (action_type, action_value)
#
# Supported action types:
#
#   "key"    Send a keyboard shortcut.
#            Examples:
#              ("key", "ctrl+c")         Copy
#              ("key", "ctrl+shift+t")   Reopen closed tab
#              ("key", "F5")             Refresh / build (depends on app)
#              ("key", "escape")         Escape key
#              ("key", "space")          Spacebar
#
#   "media"  Send a media control key.
#            Examples:
#              ("media", "play")         Play or pause
#              ("media", "next")         Next track
#              ("media", "prev")         Previous track
#              ("media", "volume_up")    Volume up
#              ("media", "volume_down")  Volume down
#              ("media", "mute")         Mute toggle
#
#   "text"   Type a string as if you typed it on a keyboard.
#            Useful for inserting boilerplate text, email signatures, etc.
#            Examples:
#              ("text", "Hello, world!")
#              ("text", "your.email@example.com")
#
# HOW TO ADD A NEW PROFILE
# ─────────────────────────
# Add a new entry to PROFILES with a unique name.
# Add that name to PROFILE_ORDER so the device knows when to show it.
#
# Example:
#   "Streaming": {
#       1: ("media", "play"),
#       2: ("key", "ctrl+shift+m"),   # Mute mic in OBS
#       ...
#   }
#   Then add "Streaming" to PROFILE_ORDER.


PROFILES = {

    "Gaming": {
        1:  ("key",   "F1"),             # Help / info overlay
        2:  ("key",   "F5"),             # Quicksave (many games)
        3:  ("key",   "F9"),             # Quickload (many games)
        4:  ("key",   "escape"),         # Pause menu
        5:  ("key",   "tab"),            # Inventory / map
        6:  ("key",   "m"),              # Map (common keybind)
        7:  ("key",   "i"),              # Inventory
        8:  ("key",   "ctrl+shift+i"),   # Dev console in some games
        9:  ("media", "volume_up"),      # Volume up
        10: ("media", "volume_down"),    # Volume down
        11: ("media", "mute"),           # Mute
        12: ("key",   "printscreen"),    # Screenshot
        13: ("key",   "alt+F4"),         # Force quit (use carefully)
        14: ("key",   "ctrl+z"),         # Undo
        15: ("key",   "space"),          # Jump / confirm
        # Button 16 is the profile switcher - do not assign it here
    },

    "Coding": {
        1:  ("key",   "ctrl+shift+p"),   # Command palette (VS Code / Cursor)
        2:  ("key",   "ctrl+/"),         # Toggle line comment
        3:  ("key",   "ctrl+shift+k"),   # Delete line
        4:  ("key",   "alt+up"),         # Move line up
        5:  ("key",   "alt+down"),       # Move line down
        6:  ("key",   "ctrl+d"),         # Select next occurrence
        7:  ("key",   "ctrl+shift+l"),   # Select all occurrences
        8:  ("key",   "F12"),            # Go to definition
        9:  ("key",   "ctrl+shift+f"),   # Find in files
        10: ("key",   "ctrl+grave"),     # Toggle terminal (VS Code)
        11: ("key",   "ctrl+b"),         # Toggle sidebar
        12: ("key",   "ctrl+shift+e"),   # Explorer panel
        13: ("key",   "ctrl+z"),         # Undo
        14: ("key",   "ctrl+shift+z"),   # Redo
        15: ("key",   "ctrl+s"),         # Save
        # Button 16 is the profile switcher
    },

    "Media": {
        1:  ("media", "play"),           # Play / Pause
        2:  ("media", "next"),           # Next track
        3:  ("media", "prev"),           # Previous track
        4:  ("media", "mute"),           # Mute toggle
        5:  ("media", "volume_up"),      # Volume up
        6:  ("media", "volume_down"),    # Volume down
        7:  ("key",   "ctrl+l"),         # Focus address bar (browser)
        8:  ("key",   "ctrl+t"),         # New browser tab
        9:  ("key",   "ctrl+w"),         # Close tab
        10: ("key",   "ctrl+shift+t"),   # Reopen closed tab
        11: ("key",   "ctrl+r"),         # Refresh page
        12: ("key",   "alt+left"),       # Browser back
        13: ("key",   "alt+right"),      # Browser forward
        14: ("key",   "F11"),            # Fullscreen toggle
        15: ("key",   "ctrl+p"),         # Print / save as PDF
        # Button 16 is the profile switcher
    },

    "Browser": {
        1:  ("key",   "ctrl+t"),         # New tab
        2:  ("key",   "ctrl+w"),         # Close tab
        3:  ("key",   "ctrl+shift+t"),   # Restore closed tab
        4:  ("key",   "ctrl+l"),         # Focus address bar
        5:  ("key",   "ctrl+f"),         # Find on page
        6:  ("key",   "ctrl+shift+j"),   # Developer console
        7:  ("key",   "F5"),             # Refresh
        8:  ("key",   "ctrl+shift+r"),   # Hard refresh (clear cache)
        9:  ("key",   "alt+left"),       # Go back
        10: ("key",   "alt+right"),      # Go forward
        11: ("key",   "ctrl+plus"),      # Zoom in
        12: ("key",   "ctrl+minus"),     # Zoom out
        13: ("key",   "ctrl+0"),         # Reset zoom
        14: ("key",   "ctrl+d"),         # Bookmark page
        15: ("key",   "ctrl+shift+b"),   # Toggle bookmarks bar
        # Button 16 is the profile switcher
    },

}


# PROFILE_ORDER determines the order profiles cycle through when you
# press the profile button. Add your custom profile names here.
PROFILE_ORDER = ["Gaming", "Coding", "Media", "Browser"]
