# love-frame

A digital picture frame and video message recording device

## Configuring the network wifi

Configuring the wifi can be done without keyboard, mouse or current network (vnc & ssh).

1.  swipe the touch screen from the bottom to the top to exit the love-frame application
2.  Double tap on the Onboard shortcut icon on the raspian desktop. This should launch an onscreen keyboard.
3.  Tap on the Wifi icon in the top header (raspian desktop)
4.  Find your network in the drop down and select it
5.  Use the onscreen keyboard to enter your wifi password when prompted
6.  Close the onscreen keyboard app
7.  Double tap the start.sh shortcut on the raspian desktop to start the love-frame app

## Accessing media files

Pictures are stored on the Pi's filesystem at:

```
/home/pi/love-frame/data/gallery
```

Raw video and audio files are also stored on the Pi's filesystem at:

```
/home/pi/love-frame/data/messages
```

You can add to the pictures shown in the gallery by uploading files to the data/gallery directory. For example, using scp from the ssh utils:

```
scp ~/Documents/my_pics/* pi@loveframe.local:/home/pi/love-frame/data/gallery
```

And you can copy raw video and audio files locally using scp like this:

```
scp pi@loveframe.local:/home/pi/love-frame/data/messages/* ~/Documents/loveframe_messages/*
```

Note that you will need a program like iMovie to stitch the audio and video together. It takes too long on the Pi to do that using ffmpeg to do it at record time.
