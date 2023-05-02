import cv2
import cv2 as cv  # запуск выделения фрагмента Alt + Shift + E
from cv2 import COLOR_BGR2GRAY

cap = cv.VideoCapture('cam_video.mp4')
# cap = cv.VideoCapture(0)
# variant = 10
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (21, 21), 0)

    ret, thresh = cv.threshold(gray, 105, 255, cv.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if len(contours):
        c = max(contours, key=cv.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        text = "Object coordinates: (" + str(x) + ' ' + str(y) + ')'
        print(text)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.putText(frame, text, (75, 75), cv.FONT_ITALIC, 1, (0, 255, 0))

    cv.imshow('frame', frame)
    if cv.waitKey(0) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
