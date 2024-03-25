from google.generativeai import GenerativeModel
import google.generativeai as genai
import os
import json
def get_answer(article, questions, options): 
    # 获取阅读答案的函数，并附上相应的解释
    # 输入格式为：（可参考数据集）
    # ariticle: str, 文章内容
    # questions: list, 题干字符串组成的列表
    # options: list嵌套, 各个题目的选项列表组成的列表

    # 例：
    # article = "I love XJTU. XJTU is the best university in the world."
    # questions = ["Which university does the author like?", "Which university is the best in the world?"]
    # options = [["XJTU", "THU", "PKU", "SJTU"], ["MIT", "THU", "XJTU", "PKU"]]

    os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890" #访问谷歌api需要挂vpn(最好是clash)，后四位是端口(port)，根据实际情况修改
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
    genai.configure(api_key='AIzaSyAYV70XLy0risGhsLylCNNwQZaqZr5jotQ') #我的谷歌api key，免费
    model = GenerativeModel('gemini-pro')
    '''
    # prompt 1
    prompt = """I'd like to ask you to solve an English reading comprehension problem. You should answer these questions according to the article by giving the corresponding letter of options, and explain why. 
You can think in a step by step manner. Firstly, read the passage and summarize its main points.
Next, read the question carefully and find out which paragraphs it relates to.
Then, reason according to the request of the question and the information in the article.
Finally, read the four choices and determine which one is the best.
You should return me the result as a list in json format. For example, [{"answer": "A", "explanation": " ..."}, {"answer": "D", "explanation": "I think ..."}, ...]
    """
    '''

    '''
    # prompt2
    prompt = """
I'd like to ask you to solve an English reading comprehension problem.\
You should answer these questions according to the article by giving the corresponding letter of options, and explain why.\

You can think in a step by step manner. \
Firstly, read the passage and summarize its main points.\
Next, read the question carefully and find out which paragraphs it relates to.\
Then, reason according to the request of the question and the information in the article.\
Finally, read the four choices and determine which one is the best.\

You should explan why the option you choose is correct and the others are not.\

You should return me the result as a list in json format. For example, [{"answer": "A", "explanation": "explanation":"As shown in the article,A is correct because ...*reasons*,B is incorrect because...*reasons*, C is incorrect because...*reasons*, D is incorrect because...*reasons*"}, 
{"answer": "D", "explanation":"As shown in the article,A is incorrect because ...*reasons*,B is incorrect because...*reasons*, C is incorrect because...*reasons*, D is correct because...*reasons*"}, ...]\
the numbers of answers must match the numbers of questions.\

Reasons have to be shown directly in article and highly correlated with questions and that option.\
At least two sentence in article should be mentioned in each reason.\
you have to give reasons for not only correct answer to prove it but incorrect answer to disprove it.\
    """
    '''
    #prompt3
    prompt_f = f"""please act as a experimental english teacher to solve an English reading comprehension problem correctly.\
You should answer these questions according to the article by giving the corresponding letter of options, and explain why.\
Most of the Question can be solved by restatement passage and summarize.\

You can think in a step by step manner. \
Firstly, read the passage and summarize its main points.\
Next, read the question carefully and find out which paragraphs it relates to.\
Then, reason according to the request of the question and the information in the article.\
Finally, read the four choices and determine which one is the best.\
"""
    prompt_e = """your answer and explaination should contain:\
1.At least 100 words.\
2.At least 4 reason,1 for each options. Prove the best choice, disprove the others.\
3.One or two evidence in passage for each reason which can prove it. Evidence must be consistent with the article\
4.Connect best choice and question with chain of evidence and logically\
5.Rethink about your answer. Espeacially if you are feeling multiple answers make sence.\

You should return me the result as a list in json format. For example, [{"answer": "A", "explanation": "explanation":"As shown in the article,A is correct because ...*reasons*,B is incorrect because...*reasons*, C is incorrect because...*reasons*, D is incorrect because...*reasons*"}, 
{"answer": "D", "explanation":"As shown in the article,A is incorrect because ...}, ...]\
the numbers of answers must match the numbers of questions.\
Be careful when using " and , in json. Recheck whether output is json format or not.\
"""
    input = prompt_f + '\n\n**Article:**\n' + article + "\n\n**Questions:**"
    for i in range(len(questions)):
        input += f'\n\n{i+1}. {questions[i]}'
        for j in  range(4):
            input += f"\n{chr(ord('A')+j)}. {options[i][j]}"
    input = input + prompt_e
    try:
        response = model.generate_content(input)
    except ValueError as e:
        print("ERROR generate content:",e)

    try:
        out = response.text
    except ValueError as e:
        feedback = response.prompt_feedback
        print("ERROR in response.text:",e)
        print(feedback)
        return
    s = out.find('[')
    e = out.find(']')
    try:
        j = json.loads(out[s:e+1])
    except SyntaxError as e:
        print("resp:",out)
        print("json load error",e)
        return
    

    # 输出格式：由字典组成的列表。列表由n项，表示n个问题的答案；每项为一个字典，给出答案和相应的解释
    # 例：
    # [{"answer": "A", "explanation": "As shown in the article, ..."}, {"answer": "D", "explanation": "I think ..."}, ...]

    return j

def generate_new(article, questions, options):
    # 根据给定的文章生成相似的文章和问题，输入格式同上
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:23457"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:23457"
    genai.configure(api_key='AIzaSyAYV70XLy0risGhsLylCNNwQZaqZr5jotQ')
    model = GenerativeModel('gemini-pro')

    prompt = """I'd like to ask you to generate an article as an English reading comprehension problem for Chinese students. You should give at most 5 questions after the article, and provide 4 options for each question. Only one of the options is correct. Don't forget to give the answer at the end.
Here is an example:"""
    input = prompt + '\n\n**Article:**\n' + article + "\n\n**Questions:**"
    for i in range(len(questions)):
        input += f'\n\n{i+1}. {questions[i]}'
        for j in  range(4):
            input += f"\n{chr(ord('A')+j)}. {options[i][j]}"
    input += """\n\nHere are some instructions:
1. The article you generate should be similar to the example I gave. Specifically, they should be similar in terms of length, vocabulary difficulty, etc.
2. The types of questions you write should also be similar to those in the examples. The types of questions can be: details understanding, reasoning, main ideas judging and so on. 
"""
    response = model.generate_content(input)
    out = response.text
    # 输出为字符串，包括文章、问题、选项和参考答案
    return out

if(__name__ == "__main__"):
    article = "I love XJTU. XJTU is the best university in the world."
    questions = ["Which university does the author like?", "Which university is the best in the world?"]
    options = [["XJTU", "THU", "PKU", "SJTU"], ["MIT", "THU", "XJTU", "PKU"]]
    resp = get_answer(article, questions, options)
    print(resp)