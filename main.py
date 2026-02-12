from flask import Flask, render_template
import os

from app.uploads.upload import upload_bp

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)



# Register your blueprint
app.register_blueprint(upload_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
