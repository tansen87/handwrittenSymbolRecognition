import torch
import torch.nn as nn
from torchvision import datasets, transforms
import torchvision.models as models
from PIL import Image


class Net(nn.Module):
    def __init__(self, num_classes=14):
        super(Net, self).__init__()
        self.BackBone = models.resnet18(pretrained=False)
        self.BackBone.fc = nn.Linear(self.BackBone.fc.in_features, 82)

    def forward(self, x):
        x = self.BackBone(x)
        return x

# 初始化模型
model = Net()
# 检查是否有可用的gpu，如果没有则使用cpu
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 权重的路径
model_path = "./require/model.pth"
# 加载训练好的权重
model.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage))
# require.to(device)
# 进入测试模式，不用计算梯度，速度会快一些
model.eval()
# 对图像做处理
data_transform = transforms.Compose([
    # 缩放到224*224
    transforms.Resize((224, 224)),
    # 将图片转换为tensor
    transforms.ToTensor(),
    # 正则化：降低模型复杂度
    transforms.Normalize((0.1307, 0.1307, 0.1307), (0.3081, 0.3081, 0.3081)),
])
dictionaries = ['./require/dictionary.txt']

def load_dict(dictFile):
    fp = open(dictFile)
    stuff = fp.readlines()
    fp.close()
    lexicon = {}
    for dic in stuff:
        w = dic.strip().split()
        lexicon[w[0]] = int(w[1])
    return lexicon

worddicts = load_dict(dictionaries[0])
worddicts_r = [None] * len(worddicts)
for kk, vv in worddicts.items():
    worddicts_r[vv] = kk

# key和value反向
symbol_names = {value: key for key, value in worddicts.items()}