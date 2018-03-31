#ifdef __unix__

#include <stdio.h>
#include <unistd.h>

#include <X11/Xlib.h>
#include <X11/extensions/dpms.h>

#define QUERY_INTERVAL 5


static const char *check_display_state(void) {
    Display *dpy = XOpenDisplay(NULL);
    int dummy;
    BOOL onoff;
    CARD16 state;

    if (!DPMSQueryExtension(dpy, &dummy, &dummy)) {
        return NULL;
    }
    if (!DPMSCapable(dpy)) {
        return NULL;
    }
    DPMSInfo(dpy, &state, &onoff);
    if (!onoff) {
        return NULL;
    }
    switch (state) {
    case DPMSModeOn:
        return "on";
    case DPMSModeStandby:
        return "standby";
    case DPMSModeSuspend:
        return "suspend";
    case DPMSModeOff:
        return "off";
    default:
        return NULL;
    }
}


int main(void) {
    const char *current_display_state, *previous_display_state;

    current_display_state = previous_display_state = check_display_state();
    do {
        if (current_display_state != previous_display_state) {
            printf("%s\n", current_display_state);
            fflush(stdout);
            previous_display_state = current_display_state;
        }
        sleep(QUERY_INTERVAL);
    } while ((current_display_state = check_display_state()) != NULL);

    return 1;
}

#else
#error This program can only be used on macos.
#endif
