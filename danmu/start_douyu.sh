ps -ef | grep danmu_douyu.py | grep -v grep | awk '{print $2}' | xargs kill

nohup python3 ./danmu_douyu.py >/dev/null 2>&1 &


