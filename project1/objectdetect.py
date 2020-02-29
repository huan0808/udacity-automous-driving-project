import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
#该程序的目的是在图像上划分出一块三角形的区域，并将图形之外的区域置零，而图形之内的区域，根据颜色进行像素点提取
# Read in the image and print some stats
image = mpimg.imread('test.jpg')
print('This image is: ', type(image), 
         'with dimensions:', image.shape)

# Pull out the x and y sizes and make a copy of the image
ysize = image.shape[0]
xsize = image.shape[1]
region_select = np.copy(image)  #注意一定要用copy，会在内存空间中开辟，之后修改图像不影响旧文件

# Define a triangle region of interest 
# Keep in mind the origin (x=0, y=0) is in the upper left in image processing
# Note: if you run this code, you'll find these are not sensible values!!
# But you'll get a chance to play with them soon in a quiz 
left_bottom = [0, 720]         #定义出三角形的边界点
right_bottom = [1050, 720]   
apex = [650, 400]
fig=plt.figure()      #定义出一个图像对象
plot1=fig.add_subplot(121)  #划分出两个子图
plot2=fig.add_subplot(122)
# Fit lines (y=Ax+B) to identify the  3 sided region of interest 
# np.polyfit() returns the coefficients [A, B] of the fit
#使用np.plotfit函数生成拟合曲线的A,B系数，也可以用它生成二次三次曲线，fit_left 就是A,B的列表
fit_left = np.polyfit((left_bottom[0], apex[0]), (left_bottom[1], apex[1]), 2)
fit_right = np.polyfit((right_bottom[0], apex[0]), (right_bottom[1], apex[1]), 1)
fit_bottom = np.polyfit((left_bottom[0], right_bottom[0]), (left_bottom[1], right_bottom[1]), 1)

# Find the region inside the lines 
#meshgrid 用来生成网格点，比如通过输入1*3 和3*1的列表，输出3*3的矩阵的x和y坐标
XX, YY = np.meshgrid(np.arange(0, xsize), np.arange(0, ysize))

#筛选所有在范围外的像素并置零
region_thresholds = ~((YY > (XX*fit_left[0] + fit_left[1])) & \
                    (YY >(XX*fit_right[0] + fit_right[1])) & \
                    (YY < (XX*fit_bottom[0] + fit_bottom[1])))

# Color pixels red which are inside the region of interest
region_select[region_thresholds] = [0,0,0]


#在范围之内的元素进行筛选
select=np.copy(region_select)
red=200
green=200
blue=200
edge=[red,green,blue]


bool_matric=(select[:,:,0]<edge[0])|(select[:,:,1]<edge[1])|(select[:,:,2]<edge[2])
select[bool_matric]=[0,0,0]
# Display the image
plot1.imshow(region_select)
plot2.imshow(select)
plt.show()