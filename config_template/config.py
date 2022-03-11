# -*- coding: utf-8 -*-

#application
update_branch: str = "stable" # main (unstable), stable

#firewall
firewall_active: bool = True
firewall_allowedips: list = ["127.0.0.1"]

#server
auto_reload: bool = True
debugger: bool = False
evalex: bool = False

port: int = 1025

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

# common german letters
# ü -> \u00FC
# Ü -> \u00DC
# ä -> \u00E4
# ö -> \u00F6
# ß -> \u00DF

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
