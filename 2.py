import cv2
import numpy as np

# 1. 打开摄像头
cap = cv2.VideoCapture(0)

# 循环读取每一帧画面
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("无法读取摄像头画面")
        break

    # 任务1：灰度图 + Canny边缘检测
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny_img = cv2.Canny(gray, threshold1=10, threshold2=60)

    # 任务2：Sobel边缘 + 反向二值化
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, dx=1, dy=0)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, dx=0, dy=1)
    sobel_x_abs = cv2.convertScaleAbs(sobel_x)
    sobel_y_abs = cv2.convertScaleAbs(sobel_y)
    sobel_full = cv2.addWeighted(sobel_x_abs, 0.5, sobel_y_abs, 0.5, 0)

    # 反向二值化
    _, sobel_bin_inv = cv2.threshold(sobel_full, thresh=40, maxval=255, type=cv2.THRESH_BINARY_INV)

    # 窗口名称全部改为英文，彻底解决乱码
    cv2.imshow("Canny Edge", canny_img)
    cv2.imshow("Sobel Original", sobel_full)
    cv2.imshow("Sobel Binary Inv", sobel_bin_inv)

    # ESC退出
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()