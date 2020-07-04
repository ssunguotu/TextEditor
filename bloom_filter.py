import mmh3
import numpy as np


"""
思路：
1. 将字符串生成的int数据对bitNum取余，得到的便是下标，将bits[inx]设为1。
2. 重复一过程7次，其中将mmh3的seed设置为2^i。
示例
f = BloomFilter()
f.input(['123', '321', '132'])
print(f.isInBits('123'), f.isInBits('132'), f.isInBits('321'))
"""


class BloomFilter():
    """布隆过滤器
    Attribute：
        __hashNum：int类型，表示hash函数的个数。
        __bits：位数组，用于记录某字符串是否在其中。
    """
    __hash_num = 7
    __bits = []
    __bit_size = 480

    def __init__(self, hash_num=7, bitSize=480):
        self.__hash_num = hash_num
        self.__bits = np.zeros(bitSize, dtype=bool)
        self.__bit_size = bitSize

    def input(self, strList):
        """
        函数说明：
        输入字符串列表，此函数根据字符列表中的值对位数组更改。
        param:
            strList:字符串列表，表示要加进来的字符串。
        """
        for s in strList:
            for i in range(1, 8):
                inx = mmh3.hash(s, 2 ^ i) % self.__bit_size
                self.__bits[inx] = True

    def is_in_bits(self, s):
        """
        函数说明：
        判断字符串是否在数据中。
        param：
            s：字符串
        """
        for i in range(1, 8):
            inx = mmh3.hash(s, 2 ^ i) % self.__bit_size
            if ~self.__bits[inx]:
                return False
        return True
