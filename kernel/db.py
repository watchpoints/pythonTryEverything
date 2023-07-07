with open('filename.txt', 'r') as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        if i % 3 == 0:
            print(line.strip() + " 😊")
        elif i % 3 == 1:
            print(line.strip() + " 😃")
        else:
            print(line.strip() + " 😉")
            
1.v7功能测试
2.故障节点session优化实现


MON适配快切脚本给ctdb调用，在故障时快速切换对应节点MGR状态


 移植主线

 移植主线
MDS支持阶段故障快切

1. MDS快速切换
2. MDS seesion快速切换
   2.1 3秒预重连
    2.2 支持 根据参数ip/client_id 直接kill session的命令，支持tell 和daemon2个方式。
    2.3 故障快切调整tick周期为1秒
3. 配合mon,CDTB调用脚本实现
4. 历史1300断流问题跟踪。

session优化：移植主线调整故障期间设置tick周期为1秒，加速session检测
session优化：移植主线reconnect阶段3秒预重连机制
session优化：移植主线kill session,减少60秒等待

封装命令kill
封装命令 配合MON/MDS适配快切脚本给ctdb调用

MDS快切优化



功能点封装脚本，供CTDBS脚本使用

移植主线 recover并发扫描
MDS配合CDTB调用脚本实现


1. MDS适配快切脚本给ctdb调用
2. 

MON适配快切脚本给ctdb调用，在故障时快速切MDS以及SESSION状态。SESSION快速下线处理事情
1.调整tick周期为1秒 2. 引入预重连机制 3 强制KILL指定IP/连接的SESSION 

快速切换
SESSION快速切换

MON适配快切脚本给ctdb调用，在故障时快速切MDS以及SESSION状态。
SESSION快速下线处理事情
1.调整tick周期为1秒 2. 引入预重连机制 3 强制KILL指定IP/连接的SESSION


MON适配快切脚本给ctdb调用，在故障时快速切MDS以及SESSION状态。SESSION快速下线处理事情
1.调整tick周期为1秒 2. 引入预重连机制 3 强制KILL指定IP/连接的SESSION 




