from readData import getData

# 第一次使用 运行后生成6个文件
# test = getData.GetData()
# print(test.get_nor_data())
# test.save_class()

# 后续使用 直接读取所生成的文件即可
test = getData.GetData.load_class()
print(test.get_nor_data().size())
# print(test.get_nor_data())
# print()

# 对结果进行反归一化的方法 xyz为结果的三个维度默认z = 6且不可以大于6
# x = ?
# y = ?
# z = ?
# print(test.renormalization(data_to_re=result, x, y, z))
