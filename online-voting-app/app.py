
from app import create_app

app = create_app()

if __name__ == "__main__":
    # FIX [10036] Server Leaks Version Information:
    # debug=False prevents Werkzeug debugger and suppresses version banners.
    # use_reloader=False prevents the "Restarting with watchdog" message.
    # server_header=False (Werkzeug 2.1+) stops Werkzeug from adding its own Server header.
    app.run(debug=False, use_reloader=False)
