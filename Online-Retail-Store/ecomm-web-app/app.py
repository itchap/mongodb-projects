from flask import Flask, render_template, jsonify
from products import products_bp
from user import user_bp
import logging_setup
import structlog
import logging

# Initialize structured logging
logging.basicConfig(level=logging.DEBUG)
logger = structlog.get_logger()

# Create Flask app
app = Flask(__name__)

# Register blueprints
app.register_blueprint(products_bp)
app.register_blueprint(user_bp)

# Define the home route
@app.route('/')
def index():
    return render_template('index.html')

# Define the admin route
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Enhanced error handling
@app.errorhandler(Exception)
def handle_error(e):
    logger.error("General error occurred", error=str(e))
    response = {
        "error": str(e),
        "message": "An error occurred while processing your request.",
        "status_code": 500
    }
    return jsonify(response), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)