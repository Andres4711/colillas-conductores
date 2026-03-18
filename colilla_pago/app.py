from flask import Flask
from routes.main import main

app = Flask(__name__)
app.register_blueprint(main)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
