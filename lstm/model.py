import torch
import torch.nn as nn
import time

torch.manual_seed(2020)

# 超参设置
TRAIN_WINDOW = 30   # 训练窗口
PREDICTION_WINDOW = 3  # 预测窗口
INPUT_SIZE = 6      # RNN输入尺寸
OUTPUT_SIZE = 6     # RNN输出尺寸
HIDDEN_SIZE = 64    # RNN隐藏神经元个数
NUM_LAYERS = 2      # RNN隐藏层个数

EPOCHS = 100  # 训练回数
INIT_LR = 0.001  # 初始学习率


class LSTM(nn.Module):
    def __init__(self,
                 input_size=INPUT_SIZE,
                 hidden_size=HIDDEN_SIZE,
                 num_layers=NUM_LAYERS,
                 output_size=OUTPUT_SIZE,
                 train_window=TRAIN_WINDOW,
                 prediction_window=PREDICTION_WINDOW):
        super(LSTM, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size
        self.train_window = train_window
        self.prediction_window = prediction_window
        self.lstm = nn.LSTM(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers
        )
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, input_seq):
        lstm_out, _ = self.lstm(input_seq)
        predictions = self.out(lstm_out)
        return predictions[-self.prediction_window:]

    def create_inout(self, input_data):
        inout_seq = []
        data_len = len(input_data)
        tw = self.train_window
        pt = self.train_window + self.prediction_window
        for i in range(data_len - pt + 1):
            train = input_data[i:i + tw]
            target = input_data[i + tw: i + pt]
            inout_seq.append((train, target))
        return inout_seq

    def lstm_train(self, train_data, epochs=EPOCHS):
        time_start = time.time()
        loss_function = nn.MSELoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=INIT_LR)
        train_inout = self.create_inout(train_data)
        print('epochs:', epochs)
        print('train length:', len(train_inout))
        loss_res = []
        for i in range(EPOCHS):
            t1 = time.time()
            for train, target in train_inout:
                optimizer.zero_grad()
                predictions = self(train)
                loss = loss_function(predictions, target)
                loss.backward()
                optimizer.step()
            t2 = time.time()
            loss_res.append(loss.item())
            print(f'epoch: {i:3} loss: {loss.item():10.8f} time:', t2 - t1)
        time_end = time.time()
        print("totally cost:", time_end - time_start)
        return loss_res

    def lstm_test(self, test_data):
        test_inout = self.create_inout(test_data)
        real = []
        pred = []
        with torch.no_grad():
            for train, target in test_inout:
                predictions = self(train)
                real.append(target)
                pred.append(predictions)
        return real, pred
