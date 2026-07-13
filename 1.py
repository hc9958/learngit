# import cv2  # 读取的格式是BGR
# import numpy as np

# # # 1、图像腐蚀，函数为：
# # # cv2.erode(src, kernel, dst, anchor, iterations, borderType, borderValue)
# # # src:输入的图像
# # # kernel:用于腐蚀的结构元件，他的形状和大小直接影响腐蚀的效果
# # # dst:它是与src相同大小和类型的输出图像。
# # # iterations:腐蚀操作的迭代次数，默认为1。次数越多，腐蚀操作执行的次数越多，腐蚀效果越明显

# sun = cv2.imread('sun.png')
# cv2.imshow('src', sun)
# # cv2.waitKey(0)
# kernel = np.ones((3, 3), np.uint8)
# erosion_1 = cv2.erode(sun, kernel, iterations=2)
# cv2.imshow('erosion_1', erosion_1)
# cv2.waitKey(0)

# # # 2、图像膨胀，函数为：
# # # cv2.dilate(img, kernel, iterations)
# # # 参数含义：
# # # img-目标图片
# # # kernel- 进行操作的内核，默认为3x3的矩阵
# # # iterations- 膨胀次数，默认为1

# wenzi = cv2.imread('wenzi.png')
# cv2.imshow('src1', wenzi)
# # cv2.waitKey(0)
# kernel = np.ones((2, 2), np.uint8)
# wenzi_new = cv2.dilate(wenzi, kernel, iterations=2)
# cv2.imshow('wenzi_new', wenzi_new)
# cv2.waitKey(0)

# import cv2
# import numpy as np

# 3、开运算与闭运算
## 开运算：先腐蚀后膨胀。作用：平滑物体的轮廓、断开较窄的狭颈并消除细的突出物。
# zhiwen = cv2.imread('zhiwen.png')
# cv2.imshow('src2', zhiwen)
# cv2.waitKey(0)

# kernel = np.ones((3, 3), np.uint8)
# zhiwen_new = cv2.morphologyEx(zhiwen, cv2.MORPH_OPEN, kernel)
# cv2.imshow('zhiwen_new', zhiwen_new)
# cv2.waitKey(0)

# zhiwen_duan = cv2.imread('zhiwen.png')
# cv2.imshow('src3', zhiwen_duan)
# cv2.waitKey(0)

# kernel = np.ones((4, 4), np.uint8)
# zhiwen_new = cv2.morphologyEx(zhiwen_duan, cv2.MORPH_CLOSE, kernel)
# cv2.imshow('zhiwen_new1', zhiwen_new)
# cv2.waitKey(0)

# # 梯度运算：膨胀—腐蚀  作用：突出显示图像中强度变化剧烈的地方
# wenzi = cv2.imread('wenzi.png')
# cv2.imshow('wenzi', wenzi)
# cv2.waitKey(0)

# kernel = np.ones((2, 2), np.uint8)
# # 膨胀
# pz_wenzi = cv2.dilate(wenzi, kernel, iterations=1)
# cv2.imshow('pz_wenzi', pz_wenzi)
# cv2.waitKey(0)

# # 腐蚀
# fs_wenzi = cv2.erode(wenzi, kernel, iterations=1)
# cv2.imshow('fs_wenzi', fs_wenzi)
# cv2.waitKey(0)

# # 膨胀—腐蚀（梯度运算）
# bianyuan = cv2.morphologyEx(wenzi, cv2.MORPH_GRADIENT, kernel)
# cv2.imshow('bianyuan', bianyuan)
# cv2.waitKey(0)

# # 关闭所有窗口
# cv2.destroyAllWindows()


# import cv2
# import numpy as np

# # 5、顶帽和黑帽
# # 顶帽= 原始图像 - 开运算结果(先腐蚀后膨胀)    用于提取比周围区域亮的细节。
# # 黑帽= 闭运算(先膨胀后腐蚀) - 原始图像      用于提取比周围区域暗的细节。
# sun = cv2.imread('sun.png')
# cv2.imshow('sun_yuantu', sun)
# cv2.waitKey(0)
# kernel = np.ones((2, 2), np.uint8)
# # 开运算
# open_sun = cv2.morphologyEx(sun, cv2.MORPH_OPEN, kernel)
# cv2.imshow('open_sun', open_sun)
# cv2.waitKey(0)
# # 顶帽
# tophat = cv2.morphologyEx(sun, cv2.MORPH_TOPHAT, kernel)
# cv2.imshow('TOPHAT', tophat)
# cv2.waitKey(0)
# # 闭运算
# close_sun = cv2.morphologyEx(sun, cv2.MORPH_CLOSE, kernel)
# cv2.imshow('close_sun', close_sun)
# cv2.waitKey(0)
# # 黑帽
# blackhat = cv2.morphologyEx(sun, cv2.MORPH_BLACKHAT, kernel)
# cv2.imshow('BLACKHAT', blackhat)
# cv2.waitKey(0)

# '''边缘检测'''
# # sobel算子
# # cv2.Sobel(src, ddepth, dx, dy[, ksize[, scale[, delta[, borderType]]]])
# #参数:
# # src:输入图像
# # ddepth:输出图像的深度(可以理解为数据类型)，-1表示与原图像相同的深度
# # dx,dy:当组合为dx=1,dy=0时x方向的一阶导数，当组合为dx=0,dy=1时y方向的一阶导数(如果同时为，通常效果不佳
# # ksize:(可选参数)Sobel算子的大小，必须是1,3,5或者7，默认为3。
# yuan = cv2.imread('yuan.png')
# cv2.imshow('yuan', yuan)
# cv2.waitKey(0)
# # x方向上的边缘
# yuan_x = cv2.Sobel(yuan, -1, dx=1, dy=0)
# cv2.imshow('yuan_x', yuan_x)
# cv2.waitKey(0)
# # x方向上的边缘，包括负数信息，但显示不出来，范围(0~255)
# # 二值黑白对比极强，左右梯度绝对值大小接近，视觉叠加成单条圆弧，
# yuan_x_64 = cv2.Sobel(yuan, cv2.CV_64F, dx=1, dy=0)
# cv2.imshow('yuan_x_64', yuan_x_64)
# cv2.waitKey(0)
# # x方向上的边缘，包括负数信息，进行取绝对值的操作，右端的负值信息就可以显示出来了
# yuan_x_full = cv2.convertScaleAbs(yuan_x_64)
# cv2.imshow('yuan_x_full', yuan_x_full)
# cv2.waitKey(0)
# # y方向上的边缘
# yuan_y = cv2.Sobel(yuan, -1, dx=0, dy=1)
# cv2.imshow('yuan_y', yuan_y)
# cv2.waitKey(0)
# # y方向上的边缘，包括负数信息，但显示不出来，因为范围是(0~255)
# yuan_y_64 = cv2.Sobel(yuan, cv2.CV_64F, dx=0, dy=1)
# yuan_y_full = cv2.convertScaleAbs(yuan_y_64)
# cv2.imshow('yuan_y_full', yuan_y_full)
# cv2.waitKey(0)
# # 如果同时使用x，y方向的结果如何呢?(不建议使用!!)只能检测 45° 斜线条，横竖轮廓全部丢失，边缘残缺；
# yuan_xy = cv2.Sobel(yuan, -1, dx=1, dy=1)
# cv2.imshow('yuan_xy', yuan_xy)
# cv2.waitKey(0)
# # 使用图像加权运算组合x和y方向的2个边缘。
# yuan_xy_full = cv2.addWeighted(yuan_x_full, 1, yuan_y_full, 1, 0)
# cv2.imshow('yuan_xy_full', yuan_xy_full)
# cv2.waitKey(0)

import cv2

# Scharr算子
# cv.Scharr(src, ddepth, dx, dy[, dst[, scale[, delta[, borderType]]]])
# src:输入图像
# ddepth:输出图片的数据深度，由输入图像的深度进行选择
# dx:x轴方向导数的阶数
# dy:y轴方向导数的阶数
zl = cv2.imread('imge1.jpg', cv2.IMREAD_GRAYSCALE)
zl_x_64 = cv2.Scharr(zl, cv2.CV_64F, dx=1, dy=0)
zl_x_full = cv2.convertScaleAbs(zl_x_64)
zl_y_64 = cv2.Sobel(zl, cv2.CV_64F, dx=0, dy=1)
zl_y_full = cv2.convertScaleAbs(zl_y_64)
zl_xy_Scharr_full = cv2.addWeighted(zl_x_full, 1, zl_y_full, 1, 0)
cv2.imshow('zl_xy_Scharr_full', zl_xy_Scharr_full)
cv2.waitKey(0)

# Laplacian拉普拉斯算子
# cv2.Laplacian(src, ddepth[, dst[, ksize[, scale[, delta, borderType]]]])
# 参数说明:
# src:输入图像，可以是灰度图像，也可以是多通道的彩色图像
# ddepth:输出图片的数据深度
# ksize:计算二阶导数滤波器的孔径大小，必须为正奇数，可选项
# scale:缩放比例因子，可选项，默认值为1
# delta:输出图像的偏移量，可选项，默认值为0
zl = cv2.imread('imge1.jpg', cv2.IMREAD_GRAYSCALE)
zl_lap = cv2.Laplacian(zl, cv2.CV_64F, ksize=3)
zl_lap_full = cv2.convertScaleAbs(zl_lap)
cv2.imshow('zl_lap_full', zl_lap_full)
cv2.waitKey(0)

# canny边缘检测
# cv.Canny( image, threshold1, threshold2, apertureSize[, L2gradient]])
# image为输入图像
# threshold1 表示处理过程中的第一个阈值。
# threshold2 表示处理过程中的第二个阈值。
zl = cv2.imread('imge1.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('zl', zl)
cv2.waitKey(0)
zl_canny = cv2.Canny(zl, 100, 150)
cv2.imshow('zl_canny', zl_canny)
cv2.waitKey(0)