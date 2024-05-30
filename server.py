from app import app

from app.controllers import user_controller,chore_controller

if __name__ == "__main__":
    app.run(debug=True)