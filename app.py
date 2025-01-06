from flask import render_template
from models import Trail, TrailSchema

import config

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    return render_template("home.html")

with app.app.app_context():
    try:
        trails = Trail.query.all()
        print(f"Retrieved {len(trails)} trails from the database.")
        print(trails)
    except Exception as e:
        print(f"Error while querying trails: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
