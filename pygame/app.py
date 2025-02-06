from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

DATA_FOLDER = 'data'

@app.route('/')
def home():
    return render_template('pygame/home.html')

@app.route('/course1')
def course1():
    return render_template('pygame/course1.html')

# コース2のページ
@app.route('/course2')
def course2():
    return render_template('pygame/course2.html')

# コース3のページ
@app.route('/course3')
def course3():
    return render_template('pygame/course3.html')

# コース4のページ
@app.route('/course4')
def course4():
    return render_template('pygame/course4.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    try:
        data = request.json
        quiz_file = data.get('quiz_file')

        if not quiz_file:
            return jsonify({'status': 'error', 'message': 'No quiz file specified'})

        json_file_path = os.path.join(DATA_FOLDER, quiz_file)

        if not os.path.exists(json_file_path):
            return jsonify({'status': 'error', 'message': f'File {quiz_file} does not exist'})

        subprocess.Popen(['python', 'game.py', json_file_path], shell=False)

        return jsonify({'status': 'success', 'message': f'Game started with {quiz_file}'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

