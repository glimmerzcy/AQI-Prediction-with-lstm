import lstm.model as model
import torch
from readData import getData

# 第一次使用 运行后生成6个文件
# test = getData.GetData()
# print(test.get_nor_data())
# test.save_class()

test = getData.GetData.load_class()
print(test.get_nor_data().size())

# 训练
# 输入数据的形状
# 天数，城市数，指标数
# 必须是torch的tensor变量
# a, b, c = 2000, 337, 6
# train_data = torch.randn(a, b, c)

test = getData.GetData.load_class()
print(test.get_nor_data().size())
all_data = test.get_nor_data()
TRAIN_LEN = 1500
train_data = all_data[:TRAIN_LEN]
print(train_data.size())

# 实例化
lstm = model.LSTM()
# 训练， 返回值为每一轮的损失值组成的数组
loss_res = lstm.lstm_train(train_data)
# 保存模型
save_path = "temp.pkl"
torch.save(lstm, save_path)
#
#
# # 测试
# load_path = "temp.pkl"
# a, b, c = 300, 337, 6
# test_data = torch.randn(a, b, c)
# # 加载模型
# lstm = torch.load(load_path)
# # 返回值为真实值和预测值的数组
# real, pred = lstm.lstm_test(test_data)


