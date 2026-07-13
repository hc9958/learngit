# 导入 argparse 模块，它提供了一种方式来处理命令行参数
import argparse

# 创建 ArgumentParser 对象，这个对象将用于定义和解析命令行参数
parser = argparse.ArgumentParser()

# 添加一个字符串类型的参数 SERIAL_PORT1，用于指定第一个报警器的串口号
# 如果没有在命令行中指定，则使用默认值 'COM5'
# 当用户使用 -h 或 --help 选项时，将显示此参数的帮助信息
parser.add_argument("--SERIAL_PORT1", type=str, default='COM5', help='第一个报警器的串口号')

# 添加一个整数类型的参数 area_thred，用于设定物体面积的阈值
# 默认值为 1500，如果没有在命令行中指定，则使用这个默认值
parser.add_argument("--area_thred", type=int, default=1600, help='物体面积的阈值')

# 添加一个浮点数类型的参数 confid_level，用于设定识别的置信度
# 默认值为 0.8，如果没有在命令行中指定，则使用这个默认值
parser.add_argument("--confid_level", type=float, default=0.8, help='识别的置信度')

# 添加一个整数类型的参数 aaa，默认值为 100
# 如果没有在命令行中指定，则使用这个默认值
parser.add_argument("--aaa", type=int, default=100)

# 添加一个整数类型的参数 bbb，默认值为 10
# 如果没有在命令行中指定，则使用这个默认值
parser.add_argument('-b', "--bbb", type=int, default=10)

# 使用 parse_args() 方法解析命令行参数，返回的 Namespace 对象将包含所有的参数值
# 如果参数在命令行中被指定，则使用指定的值；否则使用默认值
opt = parser.parse_args()

# 从 opt 对象中获取参数 aaa 的值
a = opt.aaa
# 从 opt 对象中获取参数 bbb 的值
b = opt.bbb

# 打印参数 aaa 和 bbb 的和
print(a+b)