---
typora-copy-images-to: ./
typora-root-url: ./
---

# Notes

[networkx.algorithms.simple_paths.all_simple_paths](https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.simple_paths.all_simple_paths.html#networkx.algorithms.simple_paths.all_simple_paths)

get all paths of one pair of nodes.



不能连续换乘两次：连续两条边的mode都是0；一整条路上的mode=0不超过3次2

每条路上流量分配：

![img](file:///C:\Users\zyj\Documents\Tencent Files\835227725\Image\C2C\Q1(]~9~DZ@}%T}1`G2XUT)A.png) 

每条路上流量更新公式：

![TIM图片20180812182355](/TIM图片20180812182355.png)
$$
v_s^w(j+1) = v_s^w(j)+\frac{1}{j}[y_s^w(j)-v_s^w(j)]
$$
收敛规则

![1533887671748](C:/Users/zyj/AppData/Local/Temp/1533887671748.png)

输出：迭代次数，可用的路径，mode分别=1,2,3,4的路段的流量和

要计算的起点终点：

0 480

118 480

222 480

2 480

274-480