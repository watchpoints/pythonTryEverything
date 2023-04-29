ps -ef | grep pythonTryEverything.py | grep -v grep | awk '{print $2}' | xargs kill

nohup python3 ./pythonTryEverything.py &