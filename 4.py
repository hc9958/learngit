import cv2

# 1. 读取图像
img_bgr = cv2.imread('hua.png')
if img_bgr is None:
    print("错误：未找到 'hua.png' 文件，请检查路径。")
    exit()

# ==========================================
# 任务 A: 灰度图像处理
# ==========================================
gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

# ==========================================
# 任务 B: 图像二值化
# ==========================================
# 反向二值化：背景变黑，花束变白
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# ==========================================
# 任务 C: 轮廓提取与绘制
# ==========================================
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

result_img = img_bgr.copy()

if contours:
    cnt = contours[0]

    # 1. 红色画出外部轮廓 (BGR: 0,0,255)
    cv2.drawContours(result_img, [cnt], -1, (0, 0, 255), 2)

    # 2. 绿色画出近似轮廓 (BGR: 0,255,0)
    perimeter = cv2.arcLength(cnt, True)
    epsilon = 0.005 * perimeter
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    cv2.drawContours(result_img, [approx], -1, (0, 255, 0), 2)

# ==========================================
# 任务 D: 分别弹出独立窗口（使用纯英文标题）
# ==========================================
cv2.imshow('1. Original Image', img_bgr)
cv2.imshow('2. Grayscale Image', gray)
cv2.imshow('3. Binarized Image', thresh)
cv2.imshow('4. Final Result (Red & Green)', result_img)

cv2.waitKey(0)
cv2.destroyAllWindows()