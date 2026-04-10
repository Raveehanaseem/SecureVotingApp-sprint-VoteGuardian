# NOTE: All security headers are now consolidated in __init__.py (add_security_headers).
# This file is kept for reference but the duplicate after_request hook has been removed
# to avoid conflicts. Having two after_request hooks for security headers was redundant
# and the one in __init__.py is more complete (includes CSP nonce, Server override, etc.)
#
# If you need to add more headers in future, add them in __init__.py -> add_security_headers().
