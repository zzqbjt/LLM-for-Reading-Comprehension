import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from google.generativeai import GenerativeModel
import google.generativeai as genai
import os

def get_answer(article, questions, options): 
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
    genai.configure(api_key='AIzaSyAYV70XLy0risGhsLylCNNwQZaqZr5jotQ')
    model = GenerativeModel('gemini-pro')

    # 构建输入字符串
    input_str = f"I'd like to ask you to solve an English reading comprehension problem. {article} **Questions:**"
    for i, question in enumerate(questions):
        input_str += f"\n\n{i + 1}. {question}"
        for j, option in enumerate(options[i]):
            input_str += f"\n{chr(ord('A') + j)}. {option}"

    input_str += """
You should return me the result as a list in json format. For example, [{"answer": "A", "explanation": " ..."}, {"answer": "D", "explanation": "I think ..."}, ...]
"""

    try:
        response = model.generate_content(input_str)
    except ValueError as e:
        print("ERROR generate content:", e)

    try:
        out = response.text
    except ValueError as e:
        feedback = response.prompt_feedback
        print("ERROR in response.text:", e)
        print(feedback)
        return

    s = out.find('[')
    e = out.find(']')
    try:
        result = eval(out[s:e + 1])
    except:
        return

    return result

def calculate_button_clicked():
    article = article_entry.get("1.0", tk.END).strip()
    input_text = input_entry.get("1.0", tk.END).strip()

    if not article or not input_text:
        messagebox.showerror("错误", "请输入文章和问题选项")
        return

    questions = []
    options = []
#将输入转为正确的格式
    while "[" in input_text:
        start_index = input_text.find("[")
        end_index = input_text.find("]") + 1

        if start_index != -1 and end_index != -1:
            question_text = input_text[:start_index].strip()
            options_text = input_text[start_index:end_index].strip()
            print(question_text)
            input_text = input_text[end_index:]
            options_list = eval(options_text) if options_text else []
            options.append(options_list)
            questions.append(question_text)

    if not questions:
        messagebox.showerror("错误", "请正确输入问题和选项")
        return

    output = get_answer(article=article, questions=questions,options=options)
    out = ""
    for i in range(len(output)):
        out = out + f"{i+1}. {output['answer']}"

    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, output)
    result_text.config(state=tk.DISABLED)

# 创建主窗口
window = tk.Tk()
window.title("文章计算工具")

# 创建文章输入框
article_label = tk.Label(window, text="输入文章:")
article_label.pack()

article_entry = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=5)
article_entry.pack()

# 创建问题和选项输入框
input_label = tk.Label(window, text="输入问题和选项:")
input_label.pack()

input_entry = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=10)
input_entry.pack()

# 创建生成按钮
calculate_button = tk.Button(window, text="生成答案和解析", command=calculate_button_clicked)
calculate_button.pack()

# 创建结果显示区域
result_label = tk.Label(window, text="答案及解析:")
result_label.pack()

result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=5)
result_text.config(state=tk.DISABLED)
result_text.pack()

# 运行主循环
window.mainloop()
###aritcle = "I love NLP.Teacher jiang is the best teacher in the world"
###question = ["which class does the author like?","which teacher is the best teacher in the world?"]
###option = [["NLP","CV","DSP","CSAI"],["teacher jiang","teacher zhang","teacher wang","teacher li"]]