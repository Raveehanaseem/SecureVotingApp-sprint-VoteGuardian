from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # FIX [10036]: Conditionally suppress Werkzeug Server header
    if os.environ.get('FLASK_ENV') != 'production':
        from werkzeug.serving import WSGIRequestHandler
        WSGIRequestHandler.server_version = ""
        WSGIRequestHandler.sys_version = ""
    
    app.run(debug=False, use_reloader=False)
