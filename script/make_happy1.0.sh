nohup ffmpeg -re  -stream_loop -1 -i ./1_speak.mp4 -vcodec copy -acodec copy -f flv -y  'rtmp://sendtc3a.douyu.com/live/1480416ridKuP2dr?wsSecret=8219ae303aeecfe95c0e5dc8822b9053&wsTime=65050323&wsSeek=off&wm=0&tw=0&roirecognition=0&record=flv&origin=tct&txHost=sendtc3a.douyu.com' &

