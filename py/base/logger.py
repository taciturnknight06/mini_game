from enum import IntEnum
import time
import inspect
import sys
# import base.config_data

class LogLevel(IntEnum):
    """log级别枚举

    log级别排序Critical > Error > Warn > Info > Debug

    """

    Debug = 1           # 调试信息
    Info = 2            # 普通运行时信息
    Warn = 3            # 警告
    Error = 4           # 错误信息
    Critical = 5        # 严重的系统错误信息,会导致程序终止

LogLevelName = ['Debug', 'Info', 'Warn', 'Error', 'Critical']

DefaultLayout = ''# TODO 完善pattern

# TODO 要定义一套layout语言
class LogLayout(object):
    """log信息布局器

    Desc:
        根据预先定义好的pattern,不同级别的log信息布局生成log字符串
        %p
    """
    
    def __init__(self, pattern = DefaultLayout):
        self.pattern = pattern

    def get_log_msg(self, content) -> str:
        """根据pattern生成指定格式log信息

        Args:
            @content: log信息的主要内容

        """
        
        # TODO log信息生成逻辑
        return ''


class BaseLogger(object):
    """基础logger类

    Desc:
        只实现初始化文件描述符接口和关闭接口,派生类自行实现各种logger的写入接口

    """

    write_fd = None # logger写入的文件描述符
    max_buffer_size = None # buffer缓存行数
    buffer = None # logger写入buffer
    ignore_level = None # 屏蔽掉低于这个级别的log输出
    log_layout = None # 不同级别log的布局器

    @classmethod
    def start(cls, file_name, buffer = 0):
        """以追加写入模式打开一个文件

        Args:
            @file_name:     输出文件名
            @config_name:   log信息布局配置
            @buffer:        buffer区长度

        """

        if buffer > 0:
            cls.max_buffer_size = buffer
            cls.buffer = list()

        # cls.initLayout(config_name)
        cls.write_fd = open(file_name, 'a+')


    @classmethod
    def close(cls):
        """关闭logger

        Desc:
            强制把缓冲区的数据写入文件并关闭文件描述符

        """

        if cls.write_fd is not None:
            if cls.max_buffer_size is not None and cls.max_buffer_size > 0:
                cls.write_fd.write(''.join(cls.buffer))
            cls.write_fd.flush()
            cls.write_fd.close()

    @classmethod
    def ignore(cls, log_level: LogLevel):
        """设置屏蔽log级别

        Args:
            @log_level: 屏蔽日志级别

        """

        cls.ignore_level = log_level

    @classmethod
    def initLayout(cls, config_name):
        """初始化log布局器

        Args:
            @config_name: 配置名

        """

        self.log_layout = dict()
        with open(config_name, 'r') as fd:
            for log_level_name in LogLevelName:
                pass


class SysLogger(BaseLogger):
    """系统重要运行信息logger"""

    @classmethod
    def log(cls, content, log_level: LogLevel = LogLevel.Info):
        """打log接口,会屏蔽掉低于cls.ignore_level级别的log输出

        Args:
            @content:   log字符串
            @log_level: log级别,详情参考LogLevel枚举

        """

        if cls.ignore_level is not None and log_level < cls.ignore_level:
            return

        # XXX 暂定格式: [nodeName] [LogLevel] {yyyy-mm-dd hh:mm:ss} {函数名 行数} {content}\n
        log_level_name = LogLevelName[log_level - 1]
        time_str = time.strftime('%Y-%m-%d %H:%M:%S')
        caller_frame = sys._getframe().f_back.f_back
        func_name = caller_frame.f_code.co_name
        lineno = caller_frame.f_lineno

        log_msg = f'[{log_level_name}] {time_str} [{func_name} {lineno}] {content}\n'

        # print(log_msg)
        cls.write_log(log_msg)

    @classmethod
    def write_log(cls, content):
        """写log接口
        
        Desc:
            同步IO写log到文件

        """

        if cls.max_buffer_size is not None and cls.buffer is not None:
            cls.buffer.append(content)
            if len(cls.buffer) >= cls.max_buffer_size:
                buffer = cls.buffer
                cls.buffer = list()
                cls.write_fd.write(''.join(buffer))
        else:
            cls.write_fd.write(content)

    @classmethod
    def debug(cls, content):
        cls.log(content, LogLevel.Debug)

    @classmethod
    def info(cls, content):
        cls.log(content, LogLevel.Info)

    @classmethod
    def warn(cls, content):
        cls.log(content, LogLevel.Warn)

    @classmethod
    def error(cls, content):
        cls.log(content, LogLevel.Error)

    @classmethod
    def critical(cls, content):
        cls.log(content, LogLevel.Critical)

class GameLogger(BaseLogger):
    """游戏玩法logger"""

    @classmethod
    def log(cls, content, log_level: LogLevel = LogLevel.Info):
        """打log接口,会屏蔽掉低于cls.ignore_level级别的log输出

        Args:
            @content:   log字符串
            @log_level: log级别,详情参考LogLevel枚举

        """

        if cls.ignore_level is not None and log_level < cls.ignore_level:
            return

        # XXX 暂定格式: [nodeName] [LogLevel] {yyyy-mm-dd hh:mm:ss} {玩法名 函数名 行数} {content}\n
        log_level_name = LogLevelName[log_level - 1]
        time_str = time.strftime('%Y-%m-%d %H:%M:%S')
        caller_frame = sys._getframe().f_back
        func_name = caller_frame.f_code.co_name
        lineno = caller_frame.f_lineno

        log_msg = f'[{log_level_name}] {time_str} [{func_name} {lineno}] {content}\n'

        # print(log_msg)
        cls.write_log(log_msg)

    @classmethod
    def write_log(cls, content):
        """写log接口
        
        Desc:
            同步IO写log到文件

        """

        cls.buffer.append(content)
        if len(cls.buffer) >= 200:
            buffer = cls.buffer
            cls.buffer = list()
            cls.write_fd.write(''.join(buffer))



# if __name__ == '__main__':
#     from timeit import default_timer as timer
#     SysLogger.start('multi_thread.log', 100)
#     start = timer()
#     for i in range(100000):
#         SysLogger.log(f'{i} writing log......')
#     end = timer()
#     SysLogger.close()
#     print(end - start)


