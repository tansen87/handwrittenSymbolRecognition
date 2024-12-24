# 基于ResNet的手写数字识别
> Notice: 请使用python3.11来运行此项目

#### 图片识别

![image](https://github.com/tansen87/handwrittenSymbolRecognition/assets/98570790/f295e5e7-27c0-45fc-b981-14006e7be686)
#### 手写识别
![image](https://github.com/tansen87/handwrittenSymbolRecognition/assets/98570790/35931cbe-ac04-4f3e-a627-ed42c873e1ad)



### 直接运行

1. 安装poetry

   ```cmd
   pip install poetry==1.8.5
   ```

2. 使用poetry安装依赖

   ```cmd
   poetry install
   ```

3. 启动项目

   ```cmd
   poetry run python main.py
   ```



### 自己训练

1. 在[Kaggle](https://www.kaggle.com/xainano/handwrittenmathsymbols)下载数据集 (数据集很大,可以把每个分类降至100张图片再来训练)

2. 如果只训练数字 <u>**0-9**</u> ,修改train.py第17行代码

   ```python
   self.BackBone.fc = nn.Linear(self.BackBone.fc.in_features, 10)
   ```

3. 将数据集放在 **train/train_images** ,然后开始训练

   ```cmd
   python train.py
   ```

4. 训练完成后,修改 **require/network.py** 第10行代码

   ```python
   self.BackBone.fc = nn.Linear(self.BackBone.fc.in_features, 10)
   ```

5. 将训练好的模型拷贝至 **require/** 文件夹内,并重命名为 **model.pth** (训练好的模型在 **train/checkpoints/** 文件夹)

6. 修改 **require/dictionary.txt**

   ```txt
   0 0
   1 1
   2 2
   3 3
   4 4
   5 5
   6 6
   7 7
   8 8
   9 9
   ```

7. 按照 **<u>直接运行</u>** 的3个步骤来启动项目

