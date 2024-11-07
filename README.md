3.1 第1关：基本测试
根据S-AES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是16bit的数据和16bit的密钥，输出是16bit的密文。

![O0_YQ4`28P@9F)UGSF3V_%J](https://github.com/user-attachments/assets/079884d0-0e30-46f6-8c40-42760f7fdfa6)

3.2 第2关：交叉测试
考虑到是"算法标准"，所有人在编写程序的时候需要使用相同算法流程和转换单元(替换盒、列混淆矩阵等)，以保证算法和程序在异构的系统或平台上都可以正常运行。
设有A和B两组位同学(选择相同的密钥K)；则A、B组同学编写的程序对明文P进行加密得到相同的密文C；或者B组同学接收到A组程序加密的密文C，使用B组程序进行解密可得到与A相同的P。

赵浚杰组：

![621d627f187d34b2b9984cecc9f791f4](https://github.com/user-attachments/assets/61d1c474-5f74-44b0-a6e1-83c42f551005)

我组：

![58UGD%0$RK5({F49DMZ 7P2](https://github.com/user-attachments/assets/590a1a01-4161-4980-920d-a7632b759056)



3.3 第3关：扩展功能
考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为2 Bytes)，对应地输出也可以是ACII字符串(很可能是乱码)。

![{}@9S$3KFRV96Z)IOG3}A6L](https://github.com/user-attachments/assets/cb013d79-b3c8-4e4e-8043-cfffedf5df27)

