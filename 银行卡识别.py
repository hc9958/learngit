'''任务书: 要为某家银行设计一套智能卡号识别的系统。
要求: 传入一张图片, 就自动输出信用卡图片中的数字
'''
import numpy as np
import argparse  # python内置库
import cv2
import myutils

'''
-i card1.png
-t kahao.png
'''
# 设置参数
ap = argparse.ArgumentParser()  # 创建ArgumentParser对象,这个对象将用于定义和解析命令行参数
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
ap.add_argument("-t", "--template", required=True,
                help="path to template OCR-A image")
args = vars(ap.parse_args())  # vars()是Python中的一个内置函数,用于返回对象的属性和值的字典。

# 指定信用卡类型
FIRST_NUMBER = {
    "3": "American Express",
    "4": "Visa",
    "5": "MasterCard",
    "6": "Discover Card"
}


def cv_show(name, img):  # 绘图展示
    cv2.imshow(name, img)
    cv2.waitKey(0)


'''----------模板图像中数字的定位处理----------'''
img = cv2.imread(args["template"])
cv_show('img', img)
ref = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图
cv_show('ref', ref)
ref = cv2.threshold(ref, thresh=10, maxval=255, type=cv2.THRESH_BINARY_INV)[1]  # 二值图像 黑底白字,方便找轮廓
cv_show('ref', ref)

# 计算轮廓: cv2.findContours()函数接受的参数为二值图,即黑白的(不是灰度图)
# cv2.RETR_EXTERNAL 只检测外轮廓, cv2.CHAIN_APPROX_SIMPLE只保留终点坐标
refCnts = cv2.findContours(ref, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
cv2.drawContours(img, refCnts, -1, color=(0, 0, 255), thickness=3)
cv_show('refCnts', img)
refCnts = myutils.sort_contours(refCnts, method="left-to-right")[0]  # 排序,从左到右,从上到下
digits = {}  # 保存模板中每个数字对应的像素值

for (i, c) in enumerate(refCnts):  # 遍历每一个轮廓
    (x, y, w, h) = cv2.boundingRect(c)  # 计算外接矩形并且resize成合适大小
    roi = ref[y:y + h, x:x + w]
    roi = cv2.resize(roi, dsize=(57, 88))  # 缩放到指定的大小
    cv_show('roi', roi)
    digits[i] = roi  # 每一个数字对应每一个模板

print(digits)




'''----------信用卡的图像处理----------'''
# 读取输入图像，预处理
image = cv2.imread(args["image"])
cv_show('image', image)
image = myutils.resize(image, width=300)  # 设置图像的大小
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv_show('gray', gray)
# 顶帽操作，突出图像中的细节节，清除背景图，原因是背景颜色变化小，不被腐蚀掉。
rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(9, 3))  # 初始化卷积核
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(5, 5))
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)  # 顶帽 = 原始图像 - 开运算结果(先腐蚀后膨胀)
# open = cv2.morphologyEx(gray, cv2.MORPH_OPEN, rectKernel)  # 开运算结果(先腐蚀后膨胀)
# cv_show('open', open)
cv_show('tophat', tophat)
# --------找到数字边框-----------
# 1、通过闭操作（先膨胀，再腐蚀）将数字连在一起
closeX = cv2.morphologyEx(tophat, cv2.MORPH_CLOSE, rectKernel)
cv_show('closeX', closeX)

# THRESH_OTSU会自动寻找合适的阈值，适合双峰，需把阈值参数设置为0
thresh = cv2.threshold(closeX,0,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
cv_show('thresh', thresh)

# 再来一个闭操作
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)  # 再来一个闭操作
cv_show('close2', thresh)

# 计算轮廓
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
cnts_img = image.copy()
cv2.drawContours(cnts_img, cnts, -1, color=(0, 0, 255), thickness=3)
cv_show('cnts_img', cnts_img)

# 遍历轮廓，找到数字部分像素区域
locs = []
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)  # 计算外接矩形
    ar = w / float(h)
    # 选择合适的区域，根据实际任务来。
    if 2.5 < ar < 4.0:
        if (40 < w < 55) and (10 < h < 20):  # 符合的留下来
            locs.append((x, y, w, h))
# 将符合的轮廓从左到右排序
locs = sorted(locs, key=lambda x: x[0])
print(locs)
# 新增调试
print(f"一共检测到 {len(locs)} 组卡号，准备进入数字匹配循环！")
# 将符合的轮廓从左到右排序
locs = sorted(locs, key=lambda x: x[0])
print("已完成卡号分组排序，即将开始遍历每组数字")



####################
output = []
# 遍历每一个轮廓中的数字
for (gX, gY, gW, gH) in locs:
    groupOutput = []
    group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]  # 适当加一点边界
    cv_show('group', group)
    # 预处理
    group = cv2.threshold(group,0,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv_show('group', group)
    # 计算每一组的轮廓
    digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    digitCnts = myutils.sort_contours(digitCnts, method="left-to-right")[0]
    # 计算每一组中的每一个数值
    for c in digitCnts:
        # 找到当前数值的轮廓，resize成合适的大小
        (x, y, w, h) = cv2.boundingRect(c)
        roi = group[y:y + h, x:x + w]
        roi = cv2.resize(roi, dsize=(57, 88))
        cv_show('roi', roi)
        '''------使用模板匹配，计算匹配得分----------'''
        scores = []
        # 在模板中计算每一个得分
        for (digit, digitROI) in digits.items():
            # 模板匹配
            result = cv2.matchTemplate(roi, digitROI, cv2.TM_CCOEFF)
            (_, score, _, _) = cv2.minMaxLoc(result)
            scores.append(score)
        # 得到最合适的数字
        groupOutput.append(str(np.argmax(scores)))
    # 画出来
    cv2.rectangle(image, pt1=(gX - 5, gY - 5), pt2=(gX + gW + 5, gY + gH + 5), color=(0, 0, 255), thickness=1)
    # cv2.putText()是OpenCV库中的一个函数，用于在图像上添加文本。
    cv2.putText(image, "".join(groupOutput),(gX, gY - 15), cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.65, color=(0, 0, 255), thickness=2)
    output.extend(groupOutput)  # 得到结果 将一个列表的元素添加到另一个列表的末尾。
# 打印结果
print("Credit Card Type: {}".format(FIRST_NUMBER[output[0]]))
print("Credit Card #: {}".format("".join(output)))
cv2.imshow("Image", image)
cv2.waitKey(0)