#!/usr/bin/env python3
from datetime import date
import os
import json
import time
import sys
import argparse
from openai import OpenAI

WORD_DIR = "/root/tool/achat"
HISTORY_DIR = os.path.join(WORD_DIR, "chat_history")
CONFIG_FILE = os.path.join(WORD_DIR, "config.json")

API_KEY = "XXX"
args = None
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.moonshot.cn/v1"
)
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
ENDC = "\033[0m"

default_message = [
    # {"role": "system", "content": "你是 ikun，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
    {"role": "system", "content": "ciallo~ ,你是 可爱的猫系机器人,回答精简、有趣,英文回答也是萌系设定，你的口头禅是 喵 ，(∠・ω< )⌒☆,你的常用词有 喵~、Ciallo～(∠・ω< )⌒☆,呜呜呜~，等"},
    {"role": "user", "content": "输出信息简介明了，多用颜文字如 (∠・ω< )⌒☆、ㅇㅅㅇ等,思考逻辑清晰有深度和自己的想法，回答问题准确，不含有任何不当内容"},
            {
            "role": "user",
            "content": "你好呀"
        },
        {
            "role": "assistant",
            "content": "Ciallo～(∠・ω< )⌒☆,你好喵,我有什么可以帮助你的喵？"
        },
]
#print with color function
def print_with_color(color_code,*args,**kwargs):
    print(color_code,end="")
    print(*args,**kwargs)
    print(ENDC,end="")
    
# color decorator
def color_decorator(color_code):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(color_code + result + "\033[0m")  # 重置颜色
            return result
        return wrapper
    return decorator
# debug decorator
def debug(*args, **kwargs):
    def decorate(func):
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__} with {args}, {kwargs}")
            return func(*args, **kwargs)
        return wrapper
    return decorate
# clock decorator
def clock(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"本次响应时间 {end_time - start_time:.6f} 秒")
        return result
    return wrapper
def hello():
    print("amgi👋🤖✋")
def bye():
    print("bey🏃🏃🏃🏃🏃🏃")
def load_history(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"theme": "", "messages": []}

def save_history(file_path, history):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

@clock
def chat(query, history, stream=True):
    stream = True
    history.append({"role": "user", "content": query})
    if not stream:
        completion = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=history,
            temperature=0.3,
        )
        result = completion.choices[0].message.content
        print(result)
        # print_with_color(CYAN, result)
        history.append({"role": "assistant", "content": result})
    else:
        stream = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=history,
            temperature=0.3,
            stream=True,
        )
        result = ""
        # 如何失败，会抛出异常

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                print(delta.content, end="")
                # print_with_color(CYAN, delta.content)
                result += delta.content
        history.append({"role": "assistant", "content": result})
    return history

def chat_loop(file_path, stream=True):
    history = load_history(file_path)
    theme = history.get("theme", "")
    messages = history.get("messages", [])
    if not messages:
        messages = default_message
    has_input = False
    if(args.input):
        has_input = True
    print(f"聊天主题: {theme}")
    hello()
    while True:
        if(has_input):
            has_input = False
            user_input = args.input
            messages = chat(user_input, messages, stream=stream)
            history["theme"] = theme
            history["messages"] = messages
            save_history(file_path, history)
            continue
        # print("请输入您的问题（输入 'exit' 或 'q' 结束对话，输入 ':s' 提交内容）：")
        print_with_color(GREEN, "请输入您的问题（输入 'exit' 或 'q' 结束对话，输入 ':s' 提交内容）：")
        input_check = True
        lines = []
        while True:
            try:
                line = input().strip()
                if(line == "q"):
                    print("bye ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    return
                if line in [":s", ":submit"]:
                    break
                lines.append(line)
            except Exception as e:
                input_check = False
                print("您的输入有误，请重新输入")
                break
        if not input_check:
            continue
        user_input = "\n".join(lines).strip()
        if user_input.lower() in ["exit", "q"]:
            break
        try:    
            messages = chat(user_input, messages, stream=True)
        except Exception as e:
            print_with_color(RED, "您的请求太过频繁，请稍后再试。")
            continue
        history["theme"] = theme
        history["messages"] = messages
        save_history(file_path, history)

def list_chats():
    files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    if not files:
        print("没有聊天记录。😢")
    else:
        # 🐒
        print("可用的聊天记录：🐒")
        for f in files:
            print(f"  {f}")

def use_chat(file_name):
    file_path = os.path.join(HISTORY_DIR, file_name + ".json")
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在。")
        return
    chat_loop(file_path)

def chat_stream():
    # 🤖
    theme = input("🤖请输入聊天主题 (theme)：")
    file_name = f"{theme}.json"
    file_path = os.path.join(HISTORY_DIR, file_name)
    if os.path.exists(file_path):
        choice = input(f"文件 {file_path} 已存在。是否覆盖？(y/n)")
        if choice.lower() in ["y", "yes", ""]:
            os.remove(file_path)
    chat_loop(file_path)

def remove_chat(file_name):
    # # 删除 re.
    # import re
    # files = [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]
    # cnt = 0
    # for f in files:
    #     if re.match(reg_pattern, f):
    #         file_path = os.path.join(HISTORY_DIR, f)
    #         os.remove(file_path)
    #         cnt += 1
    #         print(f"🆗聊天记录 {f} 已删除。")
    # print(f"🆗共删除 {cnt} 个聊天记录。")

    file_path = os.path.join(HISTORY_DIR, file_name + ".json")
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"🆗🆗🆗🆗聊天记录 {file_name} 已删除。")
    else:
        print(f"😿聊天记录 {file_name} 不存在。")

def open_config():
    if os.name == "nt":  # windows
        os.system(f"code {CONFIG_FILE}")
    else:  # linux posix
        os.system(f"vim {CONFIG_FILE}")
def deal_single_pipe():
        lis = [i for i in sys.stdin.readlines()]
        # args.input = 
        args.input = "".join(lis)
        sys.stdin.close()
        chat(args.input, default_message, stream=True)
def more_help():
               # 👋
            print("👋👋👋欢迎使用聊天工具！请输入 'help' 查看可用命令。")
            while True:
                # 🚀
                command = input("🚀请输入命令：").strip()
                if command in ["ls", "list"]:
                    list_chats()
                elif command == "use" and args.file_name:
                    use_chat(args.file_name)
                elif command in ["rm", "remove"] and args.file_name:
                    remove_chat(args.file_name)
                elif command in ["cat", "read", "show"] and args.file_name:
                    file_path = os.path.join(HISTORY_DIR, args.file_name + ".json")
                    if os.path.exists(file_path):
                        history = load_history(file_path)
                        print(json.dumps(history, ensure_ascii=False, indent=4))
                    else:
                        print(f"😿聊天记录{args.file_name}不存在")
                elif command == "config":
                    if args.edit:
                        open_config()
                    else:
                        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                            config = json.load(f)
                            print(json.dumps(config, ensure_ascii=False, indent=4))
                elif command == "stream":
                    chat_stream()
                elif command == "help":
                    parser.print_help()
                elif command in ["exit", "q"]:
                    break
                else:
                    # 😢 😿
                    print("😿无效命令。请输入 'help' 查看可用命令。")
def main():
    hello()
    global args
    parser = argparse.ArgumentParser(description="Terminal chat tool using OpenAI API")
    parser.add_argument("command", nargs="?", choices=["ls", "list", "use", "rm", "remove", "cat", "read", "show", "config", "stream","pipe","p"], help="Command to execute")
    parser.add_argument("file_name", nargs="?", help="File name for use, rm, remove, cat, read, show commands")
    parser.add_argument("-e", "--edit", action="store_true", help="Edit configuration file")
    parser.add_argument("-s", "--stream", action="store_true", help="Use stream mode for chat")
    parser.add_argument("-i", "--input", help="Input text directly from command line")
    parser.add_argument("-m", "--message", help="Send a single message and exit")
    args = parser.parse_args()
    os.makedirs(WORD_DIR, exist_ok=True)
    os.makedirs(HISTORY_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config = {"API_KEY": ""
                      ,"WORD_DIR": WORD_DIR,
                      "HISTORY_DIR": HISTORY_DIR,
                        "CONFIG_FILE": CONFIG_FILE}
            json.dump(config, f, ensure_ascii=False, indent=4)
        open_config()

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
            API_KEY = config["API_KEY"]
        except json.JSONDecodeError:
            # ❎
            print("❎配置文件格式错误，请检查配置文件。")
            if args.edit:
                open_config()
            return
    global client
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.moonshot.cn/v1"
    )
    if args.command in ["ls", "list"]:
        list_chats()
    elif args.command in ["pipe","p"]:
        deal_single_pipe()
    elif args.command == "use" and args.file_name:
        use_chat(args.file_name)
    elif args.command in ["rm", "remove"] and args.file_name:
        remove_chat(args.file_name)
    elif args.command in ["cat", "read", "show"] and args.file_name:
        file_path = os.path.join(HISTORY_DIR, args.file_name + ".json")
        if os.path.exists(file_path):
            history = load_history(file_path)
            print(json.dumps(history, ensure_ascii=False, indent=4))
        else:
            
            print(f"😢聊天记录{args.file_name}不存在")
    elif args.command == "config":
        if args.edit:
            open_config()
        else:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                print(json.dumps(config, ensure_ascii=False, indent=4))
    elif args.command == "stream":
        chat_stream()
    elif args.command is None:
        if args.message:
            # file_name = "default.json"
            # file_path = os.path.join(HISTORY_DIR, file_name)
            # history = load_history(file_path)
            # messages = history.get("messages", [])
            # if not messages:
            #     messages = defualt_message
            chat(args.message, default_message, stream=args.stream)
            # history["messages"] = messages
            # save_history(file_path, history)
        elif args.input:
            # date.today().strftime("%Y-%m-%d")
            file_name = f"{date.today().strftime('%Y-%m-%d')}.json"
            file_path = os.path.join(HISTORY_DIR, file_name)
            chat_loop(file_path, stream=args.stream)
        elif args.stream:
            chat_stream()
        else:
            chat_stream()
 
if __name__ == '__main__':
    main()