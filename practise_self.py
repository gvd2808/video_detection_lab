import cv2
import cv2 as cv
from cv2 import COLOR_BGR2GRAY

# variant = 10
cap = cv.VideoCapture('cam_video.mp4')    # получаем видеопоток
cap_width, cap_heght = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FRAME_WIDTH)

while True:     # loop цикл - читаем кадры до сигнала остановки
    ret, frame = cap.read()
    if not ret:
        break   # в случае остановки потока видео - break
    gray = cv.cvtColor(frame, COLOR_BGR2GRAY)   # в полутоновый (чёрно-белый) формат
    gray = cv.GaussianBlur(gray, (21, 21), 0)   # фильтр Гаусса
    # будем разбивать по пороговому значению на пиксели минимальной и максимальной интенсивности
    ret, thresh = cv.threshold(gray, 105, 255, cv.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    if len(contours):   # маркируем обнаруженную область
        c = max(contours, key=cv.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        # calculating the space object takes
        object_space_percentage = w * h / cap_width / cap_heght * 100
        text = "Object coordinates: (" + str(x) + ' ' + str(y) + ')'
        print(text, "taking", round(object_space_percentage, 2), "% of the frame")
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.putText(frame, text, (75, 75), cv.FONT_ITALIC, 1, (0, 255, 0))
        cv.putText(frame, (str(round(object_space_percentage, 2)) + '%'), (x, y - 10), cv.FONT_ITALIC, 0.5, (255, 0, 0))

    cv.imshow('frame', frame)
    if cv.waitKey(0) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
