# TODO

[toc]

## DONE

1. 定义 BloomFilter 结构的 ADT,该 ADT 应支持在 BloomFilter 中加入一个新的数据,查询数据是否在此过滤器中,并完成该结构的设计和实现.
2. 可视化。
3. 

## TODO

### 基本要求

1. 散列函数的个数与设计。
2. c和c++的所有关键字。
3. 针对上述 C 语言关键词拼写检查器进行分析,如错误分析,设计散列函数个数分析,运行时间复杂性、空间复杂性的分析。
4. 自己实现一个简单的散列函数，与库函数的性能做对比。

### 高级实现

1. 文件管理能力，`打开，保存，新建，另存为`。
2. 撤回功能。
3. 代码行数显示。



## 课程设计目的

学习 BloomFilter 结构,能应用该结构解决一些实际问题。

### 基本要求

1. 定义 BloomFilter 结构的 ADT,该 ADT 应支持在 BloomFilter 中加入一个新的数据,查询数据是否在此过滤器中,并完成该结构的设计和实现.
2. 应用 BloomFilter 结构拼写检查,许多人都对 Word 的拼写检查功能非常了解,当用户拼错一个单词的时候, Word 会自动将这个单词用红线标注出来。 Word的具体工作原理不得而知,但另一个拼写检查器 UNIXspell-checkers 这个软件中就用到了 BloomFilter。UNIXspell-checkers 将所有的字典单词存成 BloomFilter数据结构,而后直接在 BloomFilter 上进行查询。本课程设计要求针对 C 语言设计和实现上述拼写检查器,即当写了一个正确的关键词,如 int 时,给该词标上颜色,如蓝色。
3. 针对上述 C 语言关键词拼写检查器进行分析,如错误分析,设计散列函数个数分析,运行时间复杂性、空间复杂性的分析。
4. 上述 C 语言关键词拼写检查器最好是在 VC++或 Java 等可视化开发环境下实现。
5. 上述 C 语言关键词拼写检查器最好能支持所有的 C++关键词。

### 实现提示

BloomFilter 结构中的散列函数(包括散列函数的个数和散列函数的设计)是本题目中需要深入思考的一个环节。