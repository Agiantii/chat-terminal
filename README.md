# Chat Terminal

这是一个基于 OpenAI API 的终端聊天工具。你可以使用它与 AI 进行对话，并保存聊天记录。且可以自定义想要的模型

## 项目结构

```
/e:/workbench/code/python/demo/chat-terminal/
├── chat-moon-v2.py       # 主程序文件
└── README.md             # 项目介绍和运行说明
```

## 运行
1. 虚拟环境
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```
2. 安装依赖：
    ```sh
    pip install -r requirements.txt
    ```

3. 运行程序：
- 直接运行
    ```sh
    python chat-moon-v2.py
    ```
- 也可以 用linux 软链接的方式
    ```sh
    chmod  x chat-moon-v2.py
    ln -s chat-moon-v2.py /usr/bin/co
    ```
    然后就可以直接运行 `co` 了
1. 使用命令：
    - 列出聊天记录：`python chat-moon-v2.py ls`
    - 使用聊天记录：`python chat-moon-v2.py use <file_name>`
    - 删除聊天记录：`python chat-moon-v2.py rm <file_name>`
    - 查看聊天记录：`python chat-moon-v2.py cat <file_name>`
    - 编辑配置文件：`python chat-moon-v2.py config -e`
    - 开始新的聊天：`python chat-moon-v2.py stream`
```shell
usage: chat-moon-v2.py [-h] [-e] [-s] [-i INPUT] [-m MESSAGE] [{ls,list,use,rm,remove,cat,read,show,config,stream,pipe,p}] [file_name]  

Terminal chat tool using OpenAI API

positional arguments:
  {ls,list,use,rm,remove,cat,read,show,config,stream,pipe,p}
                        Command to execute
  file_name             File name for use, rm, remove, cat, read, show commands

options:
  -h, --help            show this help message and exit
  -e, --edit            Edit configuration file
  -s, --stream          Use stream mode for chat
  -i INPUT, --input INPUT
                        Input text directly from command line
  -m MESSAGE, --message MESSAGE
                        Send a single message and exit
```