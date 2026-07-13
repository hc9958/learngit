# # ----------------轮廓检测----------------
# # 查找轮廓的API: image, contours, hierarchy = cv2.findContours(img, mode, method)
# # 参数: img: 需要实现轮廓检测的原图
# # mode: 轮廓的检索模式，主要有四种方式：
# # cv2.RETR_EXTERNAL: 只检测外轮廓，所有子轮廓被忽略
# # cv2.RETR_LIST: 检测的轮廓不建立等级关系，所有轮廓属于同一等级
# # cv2.RETR_CCOMP: 返回所有的轮廓，只建立两个等级的轮廓。一个对象的外轮廓为第1级组织结构。
# #                而对象内部中空的轮廓为第2级组织结构，空洞中的任何对象的轮廓又是第 1 级组织结构。
# # -> cv2.RETR_TREE: 返回所有的轮廓，建立一个完整的组织结构的轮廓。
# # method: 轮廓的近似方法，主要有以下两种：
# # -> cv2.CHAIN_APPROX_NONE: 存储所有的轮廓点。
# # -> cv2.CHAIN_APPROX_SIMPLE: 压缩模式，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息。
# # 返回: image: 返回处理的原图
# # contours: 包含图像中所有轮廓的list对象。其中每一个独立的轮廓信息以边界点坐标 (x,y) 的形式储存在numpy数组中。

# import cv2

# phone = cv2.imread('phone.png')#读取原图
# phone_gray = cv2.cvtColor(phone,cv2.COLOR_BGR2GRAY)#灰度图的处理
# cv2.imshow('phone_b',phone_gray)
# cv2.waitKey(0)

# # phone_gray = cv2.imread('phone.png',0)  #读取灰度图

# ret, phone_binary = cv2.threshold(phone_gray, 120, 255, cv2.THRESH_BINARY)#阈值处理为二值
# cv2.imshow('phone_binary',phone_binary)
# cv2.waitKey(0)

# # _, contours , hierarchy = cv2.findContours(phone_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# contours = cv2.findContours(phone_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2]  # 通用
# # print(hierarchy)
# print(len(contours))

# # 轮廓的绘制
# # cv2.drawContours(image, contours, contourIdx, color, thickness=None,
# #                 lineType=None, hierarchy=None, maxLevel=None, offset=None)
# # 参数含义如下：
# # image:要在其上绘制轮廓的输入图像。
# # contours:轮廓列表，通常由cv2.findContours()函数返回。
# # contourIdx:要绘制的轮廓的索引，如果为负数，则绘制所有轮廓。 -1
# # color:轮廓的颜色，以BGR格式表示，例如，(0, 255, 0)表示绿色。
# # thickness:轮廓线的粗细，默认值为1。
# # lineType:轮廓线的类型，默认值为cv2.LINE_8.
# # hierarchy:轮廓层次结构，通常由cv2.findContours()函数返回。
# # maxLevel:绘制的最大轮廓层级，默认值为None，表示绘制所有层级。
# # offset:轮廓点的偏移量，默认值为None.

# image_copy = phone.copy()
# cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1,color=(0,255,0),thickness=2)
# cv2.imshow('Contours_show', image_copy)
# cv2.waitKey(0)

# # for i in range(len(contours)):
# #     image_copy = cv2.drawContours(image=image_copy, contours=contours, contourIdx=i,color=(0,255,0),thickness=3)
# #     cv2.imshow('Contours_show', image_copy)
# #     cv2.waitKey(0)

'''轮廓特征'''
# cv2.contourArea(contour[, oriented]) → retval      轮廓面积
# contour: 顶点构成的二维向量组（如轮廓列表contours中的一个轮廓）
# oriented: 定向区域标志，默认值为False，返回面积的绝对值，Ture 时则根据轮廓方向返回带符号的数值



# import cv2

# phone = cv2.imread('phone.png')#读取原图
# phone_gray = cv2.cvtColor(phone,cv2.COLOR_BGR2GRAY)#灰度图的处理
# ret, phone_binary = cv2.threshold(phone_gray, 120, 255, cv2.THRESH_BINARY)#阈值处理为二值
# contours = cv2.findContours(phone_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

# area_0 = cv2.contourArea(contours[0])    #轮廓面积
# print(area_0)
# area_1 = cv2.contourArea(contours[1])
# print(area_1)

# # arcLength(InputArray curve, bool closed)        轮廓周长
# # curve，输入的二维点集（轮廓顶点），可以是 vector 或 Mat 类型。
# # closed，用于指示曲线是否封闭。
# length = cv2.arcLength(contours[0],closed=True)
# print(length)

# # 根据面积显示特定轮廓
# a_list=[]
# for i in contours:
#     if cv2.contourArea(i)>10000:
#         a_list.append(i)

# image_copy = phone.copy()
# image_copy = cv2.drawContours(image=image_copy, contours=a_list, contourIdx=-1,color=(0,255,0),thickness=3)
# cv2.imshow('Contours_show_10000', image_copy)
# cv2.waitKey(0)

# # '''轮廓定位好方法  根据轮廓面积进行排序'''
# sortcnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]  # 选取最大面积的轮廓
# image_contours = cv2.drawContours(image_copy, contours= [sortcnt],contourIdx=-1,color=(0,0,255),thickness=3)#绘制轮廓
# cv2.imshow('image_contours',image_contours)
# cv2.waitKey(0)



# '''轮廓特征'''
# # cv2.contourArea(contour[, oriented]) → retval
# # 轮廓面积
# # contour: 顶点构成的二维向量组（如轮廓列表contours中的一个轮廓）
# # oriented: 定向区域标志，默认值为False，返回面积的绝对值，True时则根据轮廓方向返回带符号的数值
import cv2

# 1. 轮廓外接圆示例
phone = cv2.imread('phone.png')  # 读取原图
phone_gray = cv2.cvtColor(phone, cv2.COLOR_BGR2GRAY)  # 灰度图处理
ret, phone_binary = cv2.threshold(phone_gray,120,255, cv2.THRESH_BINARY)  # 阈值处理为二值
contours = cv2.findContours(phone_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

cnt = contours[0]
(x, y), r = cv2.minEnclosingCircle(cnt)  # 计算轮廓的外接圆
phone_circle = cv2.circle(phone, center=(int(x), int(y)), radius=int(r), color=(0, 255, 0), thickness=2)  # 绘制外接圆
cv2.imshow('phone_circle', phone_circle)
cv2.waitKey(0)

# 2. 最小外接矩形示例
x, y, w, h = cv2.boundingRect(cnt)  # 计算轮廓的最小外接矩形
phone_rectangle = cv2.rectangle(phone, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 0), thickness=2)  # 在图像上绘制矩形
cv2.imshow('phone_rectangle', phone_rectangle)
cv2.waitKey(0)

# ======================================================================
# 轮廓近似 cv2.approxPolyDP(curve, epsilon, closed)
# 参数说明：
# curve：输入轮廓。
# epsilon：近似精度，即两个轮廓之间最大的欧式距离。该参数越小，得到的近似结果越接近实际轮廓；反之，得到的近似结果会更加粗略。
# closed：布尔类型的参数，表示是否封闭轮廓。如果是 True，表示输入轮廓是封闭的，近似结果也会是封闭的；否则表示输入轮廓不是封闭的，近似结果也不会是封闭的。
# 返回值：approx：近似结果，是一个ndarray数组，为1个近似后的轮廓，包含了近似出来的轮廓上的点的坐标

# 3. 轮廓近似多边形示例
phone = cv2.imread('phone.png')  # 重新读取图片
phone_gray = cv2.cvtColor(phone, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
ret, phone_thresh = cv2.threshold(phone_gray,120,255, cv2.THRESH_BINARY)  # 二值化
# image, contours, hierarchy = cv2.findContours(phone_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #旧版OpenCV返回3个值
contours = cv2.findContours(phone_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2]  # 获取轮廓

epsilon = 0.01 * cv2.arcLength(contours[0], closed=True)  # 设置近似精度 【h要<ε；ε越小，点越多，越精确】
approx = cv2.approxPolyDP(contours[0], epsilon, closed=True)  # 对轮廓进行近似

print(contours[0].shape)
print(approx.shape)

phone_new = phone.copy()
image_contours = cv2.drawContours(phone_new, [approx], contourIdx=-1, color=(0, 255, 0), thickness=3)  # 绘制近似轮廓
cv2.imshow('phone', phone)
cv2.waitKey(0)
cv2.imshow('image_contours', image_contours)
cv2.waitKey(0)
