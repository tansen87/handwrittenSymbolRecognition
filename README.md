# 基于ResNet的手写数字识别
> Notice: 请使用python3.11来运行此项目

#### 图片识别

![image](https://github.com/tansen87/handwrittenSymbolRecognition/assets/98570790/f295e5e7-27c0-45fc-b981-14006e7be686)
#### 手写识别
![image](https://github.com/tansen87/handwrittenSymbolRecognition/assets/98570790/35931cbe-ac04-4f3e-a627-ed42c873e1ad)



### 运行项目

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

1. 如果你想自己训练数据集，可以在[Kaggle](https://www.kaggle.com/xainano/handwrittenmathsymbols)下载数据集 (数据集很大，可以把每个分类降至100张图片再来训练)

2. 训练 `python train.py`
