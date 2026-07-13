import cv2

# ----------------模板匹配----------------
# cv2.matchTemplate(image, templ, method, result=None, mask=None)
# image: 待搜索图像
# templ: 模板图像
# method: 计算匹配程度的方法,可以有：
# TM_SQDIFF 平方差匹配法；该方法采用平方差来进行匹配；匹配越好，值越小；匹配越差，值越大。
# TM_CCORR 相关匹配法；该方法采用乘法操作；数值越大表明匹配程度越好。
# TM_CCOEFF 相关系数匹配法；数值越大表明匹配程度越好。
# TM_SQDIFF_NORMED 归一化平方差匹配法，匹配越好，值越小；匹配越差，值越大。
# TM_CCORR_NORMED 归一化相关匹配法，数值越大表明匹配程度越好。
#-> TM_CCOEFF_NORMED 归一化相关系数匹配法，数值越大表明匹配程度越好。

kele = cv2.imread('imge1.jpg')
template = cv2.imread('tem.png')
cv2.imshow('kele', kele)
cv2.imshow('template', template)
cv2.waitKey(0)

h, w = template.shape[:2]
res = cv2.matchTemplate(kele, template, cv2.TM_CCOEFF_NORMED)  # 返回匹配结果的矩阵,其中每个元素表示该位置与模板的匹配程度
# cv2.minMaxLoc可以获取矩阵中的最小值和最大值，以及最小值的索引号和最大值的索引号
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 最小值、最大值、最小值位置、最大值位置
top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
kele_template = cv2.rectangle(kele, top_left, bottom_right, color=(0, 255, 0), thickness=2)  # 绘制矩形

cv2.imshow('kele_template', kele_template)
cv2.waitKey(0)
cv2.destroyAllWindows()