from flask import Flask
import pipeline

app = Flask(__name__)

@app.route("/api/process/start", methods=['POST'])
def start_processing_routine():
    try:
        pipeline.run()
    except Exception as e:
        print(e)
    return "Done"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5002)
