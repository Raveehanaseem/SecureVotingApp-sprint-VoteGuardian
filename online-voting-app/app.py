from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=False se faltu lines khatam ho jayengi
    # use_reloader=False se "Restarting with watchdog" khatam ho jayega
    app.run(debug=False, use_reloader=False)