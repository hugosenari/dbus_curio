while inotifywait -e close_write serialize.c; do echo `g++ -g serialize.c -o serialize -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -Wall -Wextra -lglib-2.0 -lgio-2.0 -lgobject-2.0 -lgthread-2.0  -fpermissive`; done