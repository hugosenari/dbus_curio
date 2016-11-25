#include <stdio.h>
#include <gio/gio.h>
#define MIN_ARRAY_SIZE  128



int main()
{
    GDBusMessage *message;
    gsize size;
    guchar* mbuf;
    GError* error;
    // https://github.com/GNOME/glib/blob/f924d0b1f7d2b019f1abb56685dcfda74266c608/gio/tests/gdbus-serialization.c
    GVariant *body = g_variant_new ("(tsogybnqiuxd)",
    //    value 0:   uint64:       18446744073709551615\n
                          G_GUINT64_CONSTANT(0xffffffffffffffff),
    //    value 1:    string:      `this is a string'\n
                          "this is a string",
    //    value 2:    object_path: `/this/is/a/path'\n
                          "/this/is/a/path",
    //    value 3:    signature:   `sad'\n
                          "sad",
    //    value 4:    byte:         0x2a\n
                          42,
    //    value 5:    bool:         true\n
                          TRUE,
    //    value 6:    int16:        -42\n
                          -42,
    //    value 7:    uint16:       60000\n
                          60000,
    //    value 8:    int32:        -44\n
                          -44,
    //    value 9:    uint32:       100000\n
                          100000,
    //    value 10:    int64:        -34359738368\n
                          -G_GINT64_CONSTANT(2)<<34,
    //    value 11:   double:       42.500000\n";
                          42.5
    );
    error = NULL;
    message = g_dbus_message_new_signal(
                                        "/aaaaaaa/aaaaaaa",
                                        "bbbbbbbbb.bbbbbbb",
                                        "cccccccccccccccccc");
    g_dbus_message_set_serial (message, 0x40);
    g_dbus_message_set_byte_order (message, G_DBUS_MESSAGE_BYTE_ORDER_LITTLE_ENDIAN);
    g_dbus_message_set_header (message, G_DBUS_MESSAGE_HEADER_FIELD_SIGNATURE, g_variant_new_signature ("(sogybnqiuxtd)"));
    g_dbus_message_set_body(message, body);
    mbuf = g_dbus_message_to_blob(message,
                         &size,
                         G_DBUS_CAPABILITY_FLAGS_NONE,
                         &error);
    g_print("Message size %u\n", size);
    for (int i = 0; i < size; i++) {
        g_print("\\x%02x", mbuf[i]);
    }
    g_print("\n");
    return 0;
}