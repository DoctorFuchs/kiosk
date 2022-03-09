# -*- coding: utf-8 -*-

#application
update_branch: str = "stable" # main (unstable), stable

#firewall
firewall_active: bool = True
firewall_allowedips: list = ["127.0.0.1"]

#server
auto_reload: bool = False
debugger: bool = False
evalex: bool = False

port: int = 1024

#mimetypes
mimetypes = {
    # text MIME types
    "html": "text/html",
    "css": "text/css",
    "js": "text/js",
    "json": "application/json",

    # image MIME types
    "gif": "image/gif",
    "jpg":"image/jpeg",
    "jpeg":"image/jpeg",
    "png": "image/png",
    "svg": "image/svg+xml",

    # other MIME types
    "pdf": "application/pdf"
}
mimetypes_default = "text/plain"

default_language = "de"

# Ü, ü     \u00dc, \u00fc
# Ä, ä     \u00c4, \u00e4
# Ö, ö     \u00d6, \u00f6
# ß        \u00df

contact = {
        "admin_name": "Test Test",
        "contact_ways": [
            {   
                "name":"Email",
                "link":"mailto:test@test.test",
                "icon":"mail.svg"
            },
            {
                "name":"Telegram",
                "link":"https://telegram.me/username",
                "icon":"telegram.svg"
            },
            {
                "name":"WhatsApp",
                "link":"https://wa.me/491525557912/",
                "icon":"whatsapp.svg"
            }
        ],
    }