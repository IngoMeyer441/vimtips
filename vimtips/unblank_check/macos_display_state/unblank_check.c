#ifdef __APPLE__

#include <CoreServices/CoreServices.h>
#include <IOKit/IOMessage.h>
#include <stdio.h>


#define UNUSED(param) ((void)(param))


static void display_callback(void *context, io_service_t y, natural_t msg_type, void *msg_argument) {
    static enum { display_on, display_dimmed, display_off } state = display_on;
    UNUSED(context);
    UNUSED(y);
    UNUSED(msg_argument);

    switch (msg_type) {
    case kIOMessageDeviceWillPowerOff:
        ++state;
        if (state == display_dimmed) {
            printf("dim\n");
            fflush(stdout);
        } else if (state == display_off) {
            printf("sleep\n");
            fflush(stdout);
        }
        break;
    case kIOMessageDeviceHasPoweredOn:
        if (state == display_dimmed) {
            printf("undim\n");
            fflush(stdout);
        } else {
            printf("wakeup\n");
            fflush(stdout);
        }
        state = display_on;
        break;
    }
}

static void initialize_display_notifications(void) {
    io_service_t display_wrangler;
    IONotificationPortRef notification_port;
    io_object_t notifier;

    display_wrangler = IOServiceGetMatchingService(kIOMasterPortDefault, IOServiceNameMatching("IODisplayWrangler"));
    if (!display_wrangler) {
        fprintf(stderr, "IOServiceGetMatchingService failed\n");
        exit(1);
    }
    notification_port = IONotificationPortCreate(kIOMasterPortDefault);
    if (!notification_port) {
        fprintf(stderr, "IONotificationPortCreate failed\n");
        exit(1);
    }
    if (IOServiceAddInterestNotification(notification_port, display_wrangler, kIOGeneralInterest, display_callback,
                                         NULL, &notifier) != kIOReturnSuccess) {
        fprintf(stderr, "IOServiceAddInterestNotification failed\n");
        exit(1);
    }
    CFRunLoopAddSource(CFRunLoopGetCurrent(), IONotificationPortGetRunLoopSource(notification_port),
                       kCFRunLoopDefaultMode);
    IOObjectRelease(display_wrangler);
}

int main(void) {
    initialize_display_notifications();
    CFRunLoopRun();
    return 0;
}

#else
#error This program can only be used on macos.
#endif
