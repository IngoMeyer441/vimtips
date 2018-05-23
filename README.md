# Vim Tips

## Introduction

![screenshot](https://raw.githubusercontent.com/IngoHeimbach/vimtips/master/screenshot.png)

*Vim Tips* is a project to aggregate and show vim tips from different sources. A small daemon waits for screen unlocks
and automatically starts the vim tips gui if it is the first unlock of the day.

## Installation

*Vim Tips* can be installed with `pip` on Linux and macos:

```bash
python3 -m pip install vimtips
```

*Vim tips* contains components that must be compiled on installation, so ensure you have XCode installed on macos or
build tools on any Linux distribution. For Linux, you also need X11 headers. On Ubuntu / Debian-based distributions you
can install these dependencies with:

```bash
apt install build-essential libx11-dev nx-x11proto-xext-dev
```

## Usage

After installation, you get the new commands `vimtips-gui` and `vimtips-daemon` to start the graphical application or
the daemon process. On the first gui start, the cache of vim tips is refreshed so the first startup can take several
seconds. Future runs renew the cache in the background. You can add `vimtips-daemon` to your startup / login items to
automatically get new tips on computer startup or when you unlock the screen for the first time of the day.

### Login item creation on macos

It is indeed possible to add terminal commands to the user's login items but this will cause the startup of a terminal
window every time you login to your Mac. A better solution is to start the preinstalled *Automator* application, create
a new app and add a bash script which starts `vimtips-daemon`. The created app can then be added to hidden login items.

## Tip sources

Currently, only twitter is supported as a tip source (the [vimtips account](https://twitter.com/vimtips?lang=en) is
read) but new sources can be added by creating a new Python module in `vimtips/sources`. Look at
[vimtips/sources/twitter.py](https://raw.githubusercontent.com/IngoHeimbach/vimtips/master/vimtips/sources/twitter.py)
for an example. You only need to implement a global function `tips` which returns a list of strings.

## Screen unlock detection

This package has different backends to detect a screen unlock:

- Linux:
  - `xscreensaver`: If `xscreensaver` is running, it will be asked for unlock events.
  - `X11 dpms`: As a fallback dpms events are watched which should work on every Linux desktop. However, this backend
    does not really check for a screen unlock, it checks the screen power state instead (however, in most configurations
    the screen is sent to sleep when the screen is locked, so this should be fine on most systems). This backend could
    fail if screensavers are used.
- macos:
  - On macos, the screen power state is watched similiar to the Linux X11 backend. If anyone knows how to check for a
    screen lock, please send a pull request! :)
