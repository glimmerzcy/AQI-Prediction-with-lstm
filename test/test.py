from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import torch


def singleTest(real, predict):
    return [mean_squared_error(real, predict), mean_absolute_error(real, predict), r2_score(real, predict)]


class Test:
    a, b, c = 1500, 367, 6

    def test(self, real: [torch.Tensor], predict: [torch.Tensor]):
        for item in real, predict:
            item.view(-1, self.c)

        i, j = 0, 0
        testResult = [[]]
        while i < len(real):
            i = i + 1
            while j < self.c:
                j = j + 1
                testResult.append(singleTest(real[i][j], predict[i][j]))
        return testResult
