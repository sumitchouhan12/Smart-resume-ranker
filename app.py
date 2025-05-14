from flask import Flask, render_template, request, jsonify
import os
from model import rank_resume
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'resumes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return jsonify({'score': 0})
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'score': 0})
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            score = rank_resume(filepath)
            return jsonify({'score': score})
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
