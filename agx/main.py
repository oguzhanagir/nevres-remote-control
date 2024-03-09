from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS desteğini etkinleştir

speed = 0
turning_angle = 0

@app.route('/robot-control', methods=['POST'])
def robot_control():
    global speed, turning_angle 

    try:
        data = request.get_json()
        direction = data.get('direction')

        if direction is not None:
            print(f'Received command: {direction}')

            if direction == 'w':
                speed += 5
                turning_angle = 0  
            elif direction == 's':
                speed -= 5
            elif direction == 'a':
                turning_angle -= 5
            elif direction == 'd':
                turning_angle += 5

            print(f'Current speed: {speed}, Current turning angle: {turning_angle}')


            return {'status': 'success', 'message': f'Received command: {direction}, current speed: {speed}, current turning angle: {turning_angle}'}
        else:
            return {'status': 'error', 'message': 'Invalid request payload.'}, 400
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
