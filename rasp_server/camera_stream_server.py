from flask import Response, Flask
from camera_opencv import Camera

app = Flask(__name__)


def gen(): 
    """Video streaming generator function."""
    camera = Camera()
    yield b'--frame\r\n'
    while True:
        frame = camera.get_frame()
        yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'


@app.route('/video_feed') 
def video_feed(): 
   return Response(
       gen(), 
       mimetype='multipart/x-mixed-replace; boundary=frame'
    ) 


if __name__ == "__main__":
    app.listen('0.0.0.0', 5050)
