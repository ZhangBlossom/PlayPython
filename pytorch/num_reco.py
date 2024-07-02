import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import MNIST
import matplotlib.pyplot as plt
from PIL import Image

# 定义神经网络模型
class Net(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = torch.nn.Linear(28*28, 64)  # 第一个全连接层，将输入从784维映射到64维
        self.fc2 = torch.nn.Linear(64, 64)     # 第二个全连接层，将输入从64维映射到64维
        self.fc3 = torch.nn.Linear(64, 64)     # 第三个全连接层，将输入从64维映射到64维
        self.fc4 = torch.nn.Linear(64, 10)     # 第四个全连接层，将输入从64维映射到10维（对应10个类别）

    def forward(self, x):
        x = torch.nn.functional.relu(self.fc1(x))  # 应用ReLU激活函数
        x = torch.nn.functional.relu(self.fc2(x))  # 应用ReLU激活函数
        x = torch.nn.functional.relu(self.fc3(x))  # 应用ReLU激活函数
        x = torch.nn.functional.log_softmax(self.fc4(x), dim=1)  # 应用log_softmax激活函数
        return x

# 定义数据加载函数
def get_data_loader(is_train):
    to_tensor = transforms.Compose([transforms.ToTensor()])  # 定义数据转换
    data_set = MNIST("", is_train, transform=to_tensor, download=True)  # 加载MNIST数据集
    return DataLoader(data_set, batch_size=15, shuffle=True)  # 创建数据加载器

# 定义模型评估函数
def evaluate(test_data, net):
    n_correct = 0
    n_total = 0
    with torch.no_grad():  # 禁用梯度计算
        for (x, y) in test_data:
            outputs = net.forward(x.view(-1, 28*28))  # 前向传播计算输出
            for i, output in enumerate(outputs):
                if torch.argmax(output) == y[i]:  # 比较预测结果与真实标签
                    n_correct += 1
                n_total += 1
    return n_correct / n_total  # 返回准确率

# 定义模型保存函数
def save_model(net, path="mnist_model.pth"):
    torch.save(net.state_dict(), path)  # 保存模型权重到文件

# 定义模型加载函数
def load_model(net, path="mnist_model.pth"):
    net.load_state_dict(torch.load(path))  # 从文件加载模型权重

# 定义图像预测函数
def predict_image(image, net):
    net.eval()  # 设置为评估模式
    with torch.no_grad():  # 禁用梯度计算
        output = net(image.view(-1, 28*28))  # 前向传播计算输出
        predicted = torch.argmax(output, dim=1)  # 获取预测结果
    return predicted.item()  # 返回预测类别

# 定义图像加载函数
def load_image(image_path):
    image = Image.open(image_path).convert('L')  # 打开图像并转换为灰度图
    transform = transforms.Compose([transforms.Resize((28, 28)), transforms.ToTensor()])  # 定义图像转换
    image = transform(image)  # 应用转换
    return image  # 返回处理后的图像

def main():
    # train_data = get_data_loader(is_train=True)  # 加载训练数据
    # test_data = get_data_loader(is_train=False)  # 加载测试数据
    # net = Net()  # 初始化神经网络模型
    #
    # # 训练模型
    # optimizer = torch.optim.Adam(net.parameters(), lr=0.001)  # 定义Adam优化器
    # for epoch in range(2):  # 训练2个epoch
    #     for (x, y) in train_data:
    #         net.zero_grad()  # 清零梯度
    #         output = net.forward(x.view(-1, 28*28))  # 前向传播计算输出
    #         loss = torch.nn.functional.nll_loss(output, y)  # 计算损失
    #         loss.backward()  # 反向传播计算梯度
    #         optimizer.step()  # 更新模型参数
    #     print("epoch", epoch, "accuracy:", evaluate(test_data, net))  # 打印每个epoch后的准确率
    #
    # # 保存模型
    # save_model(net)
    #
    # # 加载模型
    net = Net()  # 初始化新的神经网络模型
    # load_model(net)  # 加载已保存的模型权重
    # print("Loaded model accuracy:", evaluate(test_data, net))  # 打印加载模型后的准确率

    # 使用模型预测新图像
    image_path = "8.png"  # 替换为你要预测的图像路径
    image = load_image(image_path)  # 加载并预处理图像
    prediction = predict_image(image, net)  # 使用模型进行预测
    print(f"Predicted digit: {prediction}")  # 打印预测结果

if __name__ == "__main__":
    main()  # 运行main函数
