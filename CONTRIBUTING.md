## Hacking on love-frame

### Making code changes

Just do it! Basically, my workflow while developing is,

1. make change in vsCode and wait a second. The python plugin or format on save is first writing a cache file before it saves the actual file. Your milage may vary.
1. alt+tab to an iTerm2 tab opened to my local love-frame working directory
1. up arrow or ctrl+r to the last upload command: `./upload.sh pi@loveframe.local`
1. alt+tab to an already open VNCViewer window and already open terminal window on the Pi, stop and restart love-frame app
1. alt+tab in the VNC Viewer to go back to the terminal you started src/love-frame.py to see debugging output
1. click out of VNC Viewer and then back to vsCode
1. rinse and repeat

See subsections below for more details.

### Upload changes to the pi

Make sure you are on the same wifi / network as the pi. Below replace "loveframe.local" with the hostname of your Pi.

```
./upload.sh pi@loveframe.local
```

The upload script uses rsync over ssh to sync the /home/pi/love-frame to whatever you have locally and is very fast.

SSH may prompt you for the pi user's password. Note that you can (maybe should) add your public ssh key to the /home/pi/.ssh/authorized_keys file on the Pi and ssh will not request your password.

To get the uploaded changes to take effect, you will need to stop and restart the love-frame application on the Raspberry Pi.

### Stop the love-frame application on the Pi

- Connect to love-frame pi using VNC Viewer from your desktop.
- Press 'q' to quit

### Starting the love-frame application on the Pi

Via VNC, open a terminal (in the raspian OS top tool bar). The terminal should also be visible on the Pi display. The terminal will open to the pi user's home directory; from there:

```
cd love-frame
sudo src/love_frame.py
```

The above command will start the love-frame app with log output to the Pi desktop terminal window. With the terminal window which you can get back to via VNC using alt+tab, you will be able to see any `print(...)` debugging statements you add to the python code.

If you want to restart in the background, the way it loads on boot, you can use `sudo ./start.sh`. On boot, the start.sh script is called via `/etc/xdg/lxsession/LXDE-pi/autostart` after the X desktop loads. See setup/files/lxe-autostart for more detail on changes made to Raspian desktop to support a kiosk style application.

## Building your own love frame

### Minimum prerequisites

- Raspberry Pi 4b (4GB)
- Touch screen display
- USB web cam
- Network and SSH access on the Raspberry Pi
- VNC configured for user pi

The setup.sh script was built for the Elecrow 7" for Raspberry Pi touch screen. This display requires some custom configuration to the boot config (see setup/files/boot-config.txt) that simply didn't work with Raspian Bullseye. I needed to use Raspian Buster to get the display to work as there was no workaround at the time.

### Setup the Pi

After cloning this repo from GitHub, you can use the upload script from the base love-frame directory. Below replace "loveframe.local" with the hostname of your Pi.

```
./upload.sh pi@loveframe.local
```

Enter your Pi user's password if prompted.

ssh into the Pi:

```
ssh pi@loveframe.local
```

cd into the love-frame directory and run setup script:

```
cd love-frame
./setup.sh
```

If everything works well (it won't), you should be up and running.
