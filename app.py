# import cv2
# import os
# from flask import Flask, render_template, Response, request,redirect, url_for

# app = Flask(__name__)

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# def detect_color(frame):
#     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     height, width, _ = frame.shape

#     cx = int(width / 2)
#     cy = int(height / 2)

#     # Pick pixel value
#     pixel_center = hsv_frame[cy, cx]
#     hue_value = pixel_center[0]

#     color = "Undefined"
#     if hue_value < 5:
#         color = "RED"
#     elif hue_value < 22:
#         color = "ORANGE"
#     elif hue_value < 33:
#         color = "YELLOW"
#     elif hue_value < 78:
#         color = "GREEN"
#     elif hue_value < 131:
#         color = "BLUE"
#     elif hue_value < 170:
#         color = "VIOLET"
#     else:
#         color = "RED"

#     pixel_center_bgr = frame[cy, cx]
#     b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

#     cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
#     cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
#     cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

#     ret, jpeg = cv2.imencode('.jpg', frame)
#     return jpeg.tobytes(), color

# def gen():
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         frame_bytes, color = detect_color(frame)

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/', methods=['POST'])
# def detect():
#     success, frame = cap.read()
#     if not success:
#         return "Error: Failed to capture frame from camera"
    
#     # Detect the color of the object in the frame
#     color = detect_color(frame)
#     filename = os.path.join(app.root_path, 'img', color[1]+'.jpg')
#     cv2.imwrite(filename, frame)
#     # Return the color as a string
#     # print(color[0])
#     # cap.release()
    
#     return color
    
# @app.route('/home')
# def home():
#     return "Hello, World!"

# if __name__ == '__main__':
#     app.run()


from flask import Flask, render_template, Response, redirect, url_for
import cv2
import os

app = Flask(__name__)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Flag variable to keep track of whether the camera preview is running or not
camera_running = True
camera_capture = None
def detect_color(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    height, width, _ = frame.shape

    cx = int(width / 2)
    cy = int(height / 2)

    # Pick pixel value
    pixel_center = hsv_frame[cy, cx]
    hue_value = pixel_center[0]

    color = "Undefined"
    if hue_value < 5:
        color = "RED"
    elif hue_value < 22:
        color = "ORANGE"
    elif hue_value < 33:
        color = "YELLOW"
    elif hue_value < 78:
        color = "GREEN"
    elif hue_value < 131:
        color = "BLUE"
    elif hue_value < 170:
        color = "VIOLET"
    else:
        color = "RED"

    pixel_center_bgr = frame[cy, cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])

    cv2.rectangle(frame, (cx - 220, 10), (cx + 200, 120), (255, 255, 255), -1)
    cv2.putText(frame, color, (cx - 200, 100), 0, 3, (b, g, r), 5)
    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)

    ret, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes(), color

def gen():
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_bytes, color = detect_color(frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def gen():
    while True:
        if camera_running:
            success, frame = cap.read()
            if not success:
                break

            frame_bytes, color = detect_color(frame)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=['POST'])
def detect():
    # global camera_running  # Use the global keyword to modify the flag variable
    # if camera_running is False:
        # return "Please click the continue"
    success, frame = cap.read()
    if not success:
        return "Error: Failed to capture frame from camera"
    
    # Detect the color of the object in the frame
    color = detect_color(frame)
    filename = os.path.join(app.root_path, 'img', color[1]+'.jpg')
    cv2.imwrite(filename, frame)

    # Release the VideoCapture object to stop the camera preview
    # cap.release()
    # camera_running = False  # Set the sflag variable to False to stop the camera preview
    
    # Return the color as a string
    return color

# @app.route('/continue')
# def continue_preview():
#     global cap, camera_running  # Use the global keyword to modify the flag variables

#     if not camera_running:
#         # Create a new VideoCapture object to start the camera preview again
#         # if cap is not None:
#         #     cap.release()
#         cap = cv2.VideoCapture(0)
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#         camera_running = True  # Set the flag variable to True to resume the camera preview

#     return render_template('index.html')

# if __name__ == '__main__':

#     app.run()

