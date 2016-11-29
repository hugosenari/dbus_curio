#include <stdio.h>
#include <gio/gio.h>
#define MIN_ARRAY_SIZE  128



int main()
{
    GDBusMessage *message;
    gsize size = G_GINT64_CONSTANT(0);
    guchar* mbuf;
    GError* error;
    GVariantBuilder params;
    g_variant_builder_init(&params, G_VARIANT_TYPE_ARRAY);
    g_variant_builder_add_value(&params, g_variant_new("s", "World!"));
    g_variant_builder_add_value(&params, g_variant_new("s", "Hello"));
    GVariant *body = g_variant_new ("(tas)",
                          G_GUINT64_CONSTANT(0xffffffffffffffff),
                          &params
    );
    error = NULL;
    message = g_dbus_message_new_signal(
                                        "/aaaaaaa/aaaaaaa",
                                        "bbbbbbbbb.bbbbbbb",
                                        "cccccccccccccccccc");
    g_dbus_message_set_serial (message, 0x40);
    g_dbus_message_set_byte_order (message, G_DBUS_MESSAGE_BYTE_ORDER_LITTLE_ENDIAN);
    g_dbus_message_set_header (message, G_DBUS_MESSAGE_HEADER_FIELD_SIGNATURE, g_variant_new_signature ("(tas)"));
    g_dbus_message_set_body(message, body);
    mbuf = g_dbus_message_to_blob(message,
                         &size,
                         G_DBUS_CAPABILITY_FLAGS_NONE,
                         &error);
    if (error == NULL) {
        g_print("error code NULL\n");
    }
    g_print("Message size %lu\n", size);
    for (guint i = 0; i < size; i++) {
        g_print("\\x%02x", mbuf[i]);
    }
    g_print("\n");
    return 0;
}