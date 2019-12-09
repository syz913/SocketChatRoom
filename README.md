# SocketChatRoom
- [数据库](#数据库)

> 以下为界面优化部分
- [加背景图](#背景图)
- [实现聊天界面的气泡效果](#聊天气泡)


##### 数据库
决定使用轻量级的`sqlite`数据库存储用户信息和聊天信息
其中简单建立了两个表格 

```
CREATE TABLE users(
    username  TEXT  PRIMARY KEY   NOT NULL,
    password  TEXT  NOT NULL
);

CREATE TABLE messages(
    username  TEXT  PRIMARY KEY  NOT NULL,
    date  TEXT  NOT NULL,
    message   TEXT  NOT NULL
);
```
##### 背景图
导入资源文件 #https://blog.csdn.net/weixin_42296333/article/details/81178915
```
pyrcc5 -o images_rc.py images.qrc
```
为了使得每条信息之间有空隙，都append了空行
##### 聊天气泡
decrypted
//尽管其实是可以做出来的，但是`pyqt5`不支持这些css样式，就只是改了一下背景色还有字体样式
//再改用其他可视化控件没必要，其中直接使用正则匹配选出css样式并进行修改。