#application
update_branch: str = "stable" # main (unstable), stable

#firewall
firewall_active: bool = True
firewall_allowedips: list = ["127.0.0.1"]

#server
auto_reload: bool = False
debugger: bool = False
evalex: bool = False

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
