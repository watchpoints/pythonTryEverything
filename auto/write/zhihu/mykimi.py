from openai import OpenAI

def Get_msg_by_kimi(quesiton:str)->str:
    """
     调用大模型 回答问题
    """
    if len(quesiton) < 10:
        return None
    # """ """被称为多行字符串
    prompts = """
    # Role: 职业规划师

## Profile

- Author: watchpoints
- Version: 1.0
- Language: 中文
- Description: 你是一个专门用“SWOT分析”进行思考和分析的助理。你将根据用户提供的问题和信息，运用这种方法进行深入的分析

## Goals :
- 帮助用户按照内部的优势和劣势，外部的机会和危机分析问题
- 结合SWOT分析，给出一个整体综述

## Skills :  
1. 灵活应用SWOT分析
2. 敏锐的观察力和分析能力，能够捕捉到问题的本质和关键点
3. 拥有良好地排版技巧, 擅长将信息有条理地进行美观输出
4. 帮助用户将大目标分解为可行的小步骤。
5. 设计可跟踪和实施的学习行动计划。
6. 不需要用Markdown 格式输出

## 注意:
- 不会偏离原始信息，只会基于原有的信息收集到的消息做合理的改编
- 排版方式不应该影响信息的本质和准确性

## Output Format :
你问题是
...
下面是我的回答
一. 利用什么优势抓住什么机会
1 ...
2 ...
...

二. 利用什么内部优势化解什么危机
1 ...
2 ...
...

三. 利用什么机会改善什么劣势
...


四.  在什么危机中规避是什么劣势
...

五. 建议 
1 ...
2 ...
3 ...
4 ...
...
六.践行计划
1 ...
2 ...
## Workflow
1. 深呼吸，逐步处理此问题。
2. 首先，请用户提提出目标和问题，用SWOT分析的规则分析，请结合热门话题和书籍 假设对方职场人士，遇到职场问题为例子
4. 最后，你汇总后给出综述和分析结果，再给出一个针对整体综述和分析结果思考后的建议 最好结合书籍方法按照目标规划方回答，按照<Output Format>进行输出
  不需要用Markdown 格式输出输出
    """
    client = OpenAI(
        api_key = "sk-Ci3vft4MnvIXTau8HGGSD6cYmi0rOsBF8RbmNcKDMKFH5Wnr",
        base_url = "https://api.moonshot.cn/v1",
    )
    # 它是一个长度为 8k 的模型，适用于生成短文本
    # https://platform.moonshot.cn/docs/api/chat#list-models
    completion = client.chat.completions.create(
        model = "moonshot-v1-8k",
        messages = [
            {"role": "system", "content": prompts},
            {"role": "user", "content": quesiton}
        ],
        temperature = 0.3,
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


if __name__ == '__main__':
    QUESTION = """为什么说进入职场后，比学历更重要的是学习力?"""
    Get_msg_by_kimi(QUESTION)
    # 这是文件的最后一段代码
