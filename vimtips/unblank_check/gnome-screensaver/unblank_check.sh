#!/bin/bash

DESKTOP_ENVIRONMENT="gnome"  # can be `xfce` or `gnome`

while read -r line; do
    case "${line}" in
        *"boolean false"*)
            echo "unblank"
            ;;
    esac
done < <(dbus-monitor --session "type='signal',interface='org.${DESKTOP_ENVIRONMENT}.ScreenSaver'")
