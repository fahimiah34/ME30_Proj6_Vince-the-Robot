from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Render the HTML page
    return render_template("index.html")

@app.route("/start", methods=['POST'])
def start_process():
    ip_address = request.form.get('ip_address', '')
    delay_start = request.form.get('delay_start', '')
    speed = request.form.get('speed', '')
    print("Starting process with IP: {}, Delay: {}, Speed: {}".format(ip_address, delay_start, speed))
    # Include your logic to start the process with these parameters
    return jsonify(status="Process started")

@app.route("/stop", methods=['POST'])
def stop_process():
    print("Stopping process")
    # Include your logic to stop the process
    return jsonify(status="Process stopped")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')