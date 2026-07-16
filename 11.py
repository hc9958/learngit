# ====================== 1. 导入基础库 & 打印版本 ======================
import torch
import torchvision
import torchaudio
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

# 打印各库版本
print(torch.__version__)
print(torchvision.__version__)
print(torchaudio.__version__)

"""
MNIST包含70,000张手写数字图像：60,000张用于训练，10,000张用于测试。
图像是灰度的，28x28像素的，并且居中的，以减少预处理和加快运行。
"""

# ====================== 2. 加载MNIST数据集 ======================
'''下载训练数据集（包含训练图片+标签）'''
training_data = datasets.MNIST(
    root="data",  # 数据集存放路径
    train=True,   # 读取训练集
    download=True,# 无文件则自动下载
    transform=ToTensor(), # 图片转为张量
)

'''下载测试数据集'''
test_data = datasets.MNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)

# ====================== 3. 可视化图片（注释状态，取消注释可查看） ======================
'''展示手写字图片，把训练数据集中的前9张图片展示一下'''
# from matplotlib import pyplot as plt
# figure = plt.figure()
# for i in range(9):
#     img, label = training_data[i]  # 提取第i张图片
#     figure.add_subplot(3, 3, i+1)  # 3行3列子图
#     plt.title(label)
#     plt.axis("off")
#     plt.imshow(img.squeeze(), cmap="gray") # squeeze去除通道维度，灰度图显示
# plt.show()

# ====================== 4. 构建DataLoader数据加载器 ======================
'''创建数据DataLoader（数据加载器）
batch_size:将数据集分成多份，每一份为batch_size个数据。
优点：可以减少内存的使用，提高训练速度。
'''
train_dataloader = DataLoader(training_data, batch_size=64) #64张图片为一个批次
test_dataloader = DataLoader(test_data, batch_size=64)

# 打印一批数据的张量形状
for X, y in test_dataloader:
    print(f"Shape of X [N, C, H, W]: {X.shape}")
    print(f"Shape of y: {y.shape} {y.dtype}")
    break

# ====================== 5. 自动选择训练设备（GPU/CPU/MPS） ======================
'''判断当前设备是否支持GPU，其中mps是苹果m系列芯片的GPU。'''
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using {device} device")

# ====================== 6. 定义全连接神经网络模型 ======================
'''定义神经网络 类的继承'''
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__() # 父类初始化
        self.flatten = nn.Flatten() # 28*28图片展平为一维向量
        # 三层全连接层
        self.hidden1 = nn.Linear(28*28, 128)
        self.hidden2 = nn.Linear(128, 256)
        self.out = nn.Linear(256, 10) # 输出10个数字类别

    def forward(self, x):
        # 前向传播数据流
        x = self.flatten(x)
        x = self.hidden1(x)
        x = torch.sigmoid(x) # sigmoid激活函数
        x = self.hidden2(x)
        x = torch.sigmoid(x)
        x = self.out(x)
        return x

# 模型迁移到GPU/CPU
model = NeuralNetwork().to(device)
print(model)

# ====================== 7. 训练函数 train ======================
def train(dataloader, model, loss_fn, optimizer):
    model.train() # 开启训练模式，启用Dropout/BatchNorm训练逻辑
    batch_size_num = 1  # 批次计数
    for X, y in dataloader:
        # 数据、标签迁移到对应设备
        X, y = X.to(device), y.to(device)
        pred = model(X) # 前向推理（forward可省略，model(X)自动调用forward）
        loss = loss_fn(pred, y) # 计算损失

        # 反向传播更新权重
        optimizer.zero_grad() # 梯度清零，防止累加
        loss.backward()       # 反向传播求梯度
        optimizer.step()      # 根据梯度更新模型参数

        loss_value = loss.item() # 提取张量内纯数值
        # 每100个批次打印一次损失
        if batch_size_num % 100 == 0:
            print(f"loss: {loss_value:>7f}  [number:{batch_size_num}]")
        batch_size_num += 1

# ====================== 8. 测试函数 test ======================
def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset) # 测试集总样本数
    num_batches = len(dataloader)  # 总批次数量
    model.eval() # 开启评估模式，关闭Dropout、不更新参数
    test_loss, correct = 0, 0
    # 关闭梯度计算，节省显存
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item() # 累加每一批损失
            # argmax(1)取每行最大值索引=预测数字，和标签对比统计正确数量
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    # 平均损失、平均正确率
    test_loss /= num_batches
    correct /= size
    print(f"Test result: \n Accuracy: {(100*correct):.2f}%, Avg loss: {test_loss:.6f}")

# ====================== 9. 损失函数 & 优化器 ======================
loss_fn = nn.CrossEntropyLoss() # 多分类交叉熵损失，适配10个数字分类
# SGD随机梯度下降优化器，学习率lr=0.01
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# ====================== 10. 执行一轮训练 + 一轮测试 ======================
# 完整遍历一次训练集
train(train_dataloader, model, loss_fn, optimizer)
# 在测试集验证模型效果
test(test_dataloader, model, loss_fn)