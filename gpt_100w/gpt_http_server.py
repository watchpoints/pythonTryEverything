""" baidu gpt"""
import logging
from flask import Flask, request, jsonify  
app = Flask(__name__)

LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


#@app.route('/api/json', methods=['POST'])
app.route('/', methods=['POST'])
def example():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        # 从 POST 请求的 JSON 数据中获取参数
        # 解析 JSON 数据  
        data = request.get_json()
        print(data)

        # 在服务端进行一些处理
        # ...

        # 返回 JSON 格式的响应
        # 构建JSON响应对象并返回  
        response = {  
            'status': 'success',  
            'message': 'POST请求已收到',
            'data': data
        }
        return jsonify(response)
#pip install --upgrade Werkzeug
if __name__ == "__main__":

    # not  execute logging  fucntion before  here
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        filename="./pythonTryEverything.log"
                        )

    logging.info("""
        ┌──────────────────────────────────────────────────────────────────────┐
        │                                                                      │    
        │                      •  Start Beemove  •                             │
        │                                                                      │
        └──────────────────────────────────────────────────────────────────────┘
    """)

   
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)
    # http://127.0.0.1:8080/
    #curl -X POST -H "Content-Type: application/json" -d '{"key1":"value1", "key2":"value2"}' http://example.com/post_json
