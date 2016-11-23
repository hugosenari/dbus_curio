#include <stdio.h>
#include <gio/gio.h>
#define MIN_ARRAY_SIZE  128

typedef struct _GMemoryBuffer GMemoryBuffer;
struct _GMemoryBuffer
{
  gsize len;
  gsize valid_len;
  gsize pos;
  gchar *data;
  GDataStreamByteOrder byte_order;
};

int main()
{
    GDBusMessage *message;
    gsize * size;
    guchar * mbuf = 0;
    GError * error;
    GVariant *var = g_variant_new_boolean (TRUE);;
    message = g_dbus_message_new_signal(
                                        "/org/gtk/GDBus/TestObject",
                                        "org.gtk.GDBus.TestInterface",
                                        "GimmeStdout");
    //g_dbus_message_set_signature(message, "b");
    //g_dbus_message_set_body(message, var);
    mbuf = g_dbus_message_to_blob(message,
                         size,
                         G_DBUS_CAPABILITY_FLAGS_NONE,
                         &error);
    g_print("Hello World\n %s", size);
    return 0;
}