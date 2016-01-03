"""
    交互式shell,基于扩展库cmd,提供如下功能:
    1. 输入命令,交予解析模块,等待响应,打印响应结果
    2. 如果等待响应的时间较长,可以选择让命令进入后台执行
"""

import cmd


class Shell(cmd.Cmd):
    """ 实现交互式shell """
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "


if __name__ == "__main__":
    shell = Shell()
    # 循环退出的唯一原因是触发了非KeyboardInterrupt异常
    while True:
        try:
            shell.cmdloop()
        # 获取用户按下^C触发的exception,实现让命令转入后台执行
        except KeyboardInterrupt:
            print("User pressed ^C")
        except Exception:
            print("Catch other exceptions")
            raise
