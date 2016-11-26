while inotifywait -e close_write serialize.c; do
    g++ -g serialize.c -o serialize \
        `pkg-config --cflags glib-2.0` \
        -Wall -Wextra -lglib-2.0 -lgio-2.0 -lgobject-2.0 -lgthread-2.0  -fpermissive;
#    export GLIB_PATH=/home/hugosenari/codes/glib;
#    g++ -g serialize.c -o serialize_dbg \
#        -I$GLIB_PATH -I$GLIB_PATH/glib -I$GLIB_PATH/gio -I$GLIB_PATH/gmodule -I$GLIB_PATH/gobject -I$GLIB_PATH/gthread \
#        -Wall -Wextra -lglib-2.0 -lgio-2.0 -lgobject-2.0 -lgthread-2.0  -fpermissive;
done

#sh -c "
#while inotifywait -e close_write gio/gdbusmessage.c; do
#make;
#g++ -g $PWD/../dbus_curio/sandbox/serialize.c -o $PWD/../dbus_curio/sandbox/serialize_dbg \
#    -I$PWD -I$PWD/gio -I$PWD/gio/libs/ -I$PWD/glib -I$PWD/gmodule -I$PWD/gobject -I$PWD/gthread \
#    -Wall -Wextra -lglib-2.0 -lgio-2.0 -lgobject-2.0 -lgthread-2.0  -fpermissive;
#done"