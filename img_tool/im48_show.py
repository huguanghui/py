# coding:utf-8
import numpy as np
import matplotlib.pyplot as plt

# width = 80
# height = 62
width = 773
height = 512

# 读取ARGB8888图片数据
# image_data = np.fromfile('image.argb8888', dtype=np.uint8)
image_data = np.fromfile('output.yuv', dtype=np.uint8)
print(type(image_data))
# 将图片数据转换为RGBA格式
image_data = image_data.reshape((height, width, 4))
image_data = image_data[:, :, 1:4]
print(image_data.shape)
print("dtim {}".format(image_data.ndim))
# 创建一个新的Figure对象
fig = plt.figure()
# 在Figure对象上创建一个子图
ax = fig.add_subplot(111)
# 显示图片
ax.imshow(image_data)
# 显示图形
plt.show()
