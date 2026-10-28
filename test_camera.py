import cv2

cap=cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
print("Camera opened successfully")

while True:
    ret,frame=cap.read()
    if not ret:
        print("can't get frame")
        break
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()