# where2party
So where to party? 一款基于百度地图API的多人聚会聚餐地点协商助手

## 设计

以下是**where2party**的初步设计

1. 利用百度地图API的geocoding和suggestion接口获取每个人的地址和目的地(餐厅名、游乐设施种类名、影院名等)地址
2. 利用百度地图API的批量算路分别计算每一组的最佳目的地（最佳的定义：每个人到目的地的平均用时最短、平均距离最小）
3. 最终裁决

工作流程示意图如下：

还没画

## 用法

- 直接克隆并使用：
```bash
git clone https://github.com/QGrain/where2party.git
pip install -r requirements.txt
python where2party.py
```

- 通过pip下载where2party使用 (TBD)：
```bash
pip install where2party
where2party
```

## 参考

[百度地图Web服务API](https://lbsyun.baidu.com/faq/api?title=webapi)