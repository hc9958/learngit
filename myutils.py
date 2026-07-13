import cv2

def sort_contours(cnts,method='left-to-right'):
    reverse=False
    i=0

    if method=='right-to-left' or method=='bottom-to-top':
        reverse=True
    if method=='top-to-bottom' or method=='bottom-to-top':
        i=1
    boundingBoxes=[cv2.boundingRect(c) for c in cnts]
    (cnts,boundingBoxes)=zip(*sorted(zip(cnts,boundingBoxes),
                                     key=lambda b:b[1][i],reverse=reverse))
    #zip(*...) 使用星号操作符解包排序后的元组列表，并将其重新组合成两个列表：一个包含所有轮廓，另一个包含所有边界框。
    return cnts,boundingBoxes


def resize(image,width=None,height=None,inter=cv2.INTER_AREA):
    dim=None
    (h,w)=image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r=height/float(h)
        dim=(int(w*r),height)
    else:
        r=width/float(w)
        dim=(width,int(h*r))
    resized=cv2.resize(image,dim,interpolation=inter)    #默认为cv2.INTER_AREA，即面积插值，适用于缩放图像。
    return resized


# for i,j in enumerate([5,6,7]):
#     print(i,j)
#
# a=[i for i in range(5)]
# print(a)

# a=''.join(['4','0','0','0'])
# print(a)

