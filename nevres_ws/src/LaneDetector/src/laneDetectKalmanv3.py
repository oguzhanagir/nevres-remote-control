import cv2
from keras.models import load_model
import numpy as np

model = load_model("/home/oguzhan/nevres_ws/src/LaneDetector/src/nevres-best.hdf5", compile=False)

# Kalman Filtresi Değişkenleri
kf = cv2.KalmanFilter(4, 2)
kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32) 
kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
kf.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.003
last_measurement = None
last_prediction = None

cap = cv2.VideoCapture(2) #Harici Zed 2i kamerasını alır.

while True:
    retval, frame = cap.read()
    frame2 = cv2.resize(frame,(256,256))
    gray_image = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    frames = [gray_image]
    image_dataset = np.array(frames)
    image_dataset = np.expand_dims(image_dataset, axis=3)

    image_dataset = image_dataset / 255.

    pred = (model.predict(image_dataset)[0,:,:,0] > 0.5).astype(np.uint8)

    pred = pred.reshape(256, 256, 1)
    pred = pred.astype(np.uint8)

    h, w, d = pred.shape
    image = frame.copy()

    mask0 = pred.copy()
    mask6 = pred.copy()
    right_lane = pred.copy()
    left_lane = pred.copy()

    search_top0 = h // 2
    search_bot0 = h // 2 + 100
    mask0[0:search_top0, 0:w] = 0
    mask0[search_bot0:h, 0:w] = 0
    mask_left_against = mask0.copy()
    mask_right_against = mask0.copy()

    left_roi_x = 3 * w // 5
    left_roi_y = 3 * h // 4

    right_roi_x = 3 * w // 5
    right_roi_y = 3 * h // 4


    mask_left_against[:, left_roi_x:] = 0
    mask_right_against[:, :right_roi_x] = 0

    search = h // 2 + 150
    mask6[0:search, 0:w] = 0

    right_lane[:right_roi_y, :] = 0
    right_lane[right_roi_y:, :right_roi_x] = 0

    left_lane[:left_roi_y, :] = 0
    left_lane[left_roi_y:, left_roi_x:] = 0

    M = cv2.moments(left_lane)
    N = cv2.moments(right_lane)

    SagM = cv2.moments(mask_right_against)
    SolM = cv2.moments(mask_left_against)
    S = cv2.moments(mask0)
    if S["m00"] != 0:
        cX = int(S["m10"] / S["m00"])
        cY = int(S["m01"] / S["m00"])
    else:
        cX, cY = 0, 0

    sagX = -1
    solX = -1

    if SagM["m00"] != 0:
        sagX = int(SagM["m10"] / SagM["m00"])
    if SolM["m00"] != 0:
        solX = int(SolM["m10"] / SolM["m00"])

    prediction = np.array([cX, cY, 0, 0], dtype=np.float32)

    if last_measurement is None:
        last_measurement = prediction
    if last_prediction is None:
        last_prediction = prediction.reshape(4, 1)

    measurement = np.array([cX, cY], dtype=np.float32)

    prediction = np.matmul(kf.transitionMatrix, last_prediction)
    prediction = prediction.reshape(-1,1)
    kf.predict()

    if np.sum(measurement) != 0:
        kf.correct(measurement)

    last_prediction = prediction
    last_measurement = measurement

    # Görselleştirme
    cv2.circle(image, (cX, cY), 5, (0, 255, 0), -1)

    if sagX != -1:
       cv2.line(image, (sagX, 0), (sagX, h), (0, 255, 0), 2)

    if solX != -1:
        cv2.line(image, (solX, 0), (solX, h), (255, 0, 0), 2)

    if sagX != -1 and solX != -1:
        diff = (sagX + solX) // 2
        cv2.line(image, (diff, 0), (diff, h), (0, 0, 255), 2)


        if diff > 0:
            # Aracı sağa döndür
            angle = diff / 10
            print("Sağ")
        elif diff < 0:
            # Aracı sola döndür
            angle = diff / 10
            print("Sol")
        else:
            print("Düz")
    else:  
      angle = 0
      print("Düz")

    print(angle)
    
    
    cv2.imshow("output", image)
    #cv2.imwrite("output.jpg",image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()