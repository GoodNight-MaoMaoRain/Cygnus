"""
检测进程是否在运行，如果某一个进程不在运行，则向硬件传输停止信号，之后重启整个服
务器或者进行修复（修复会对结果有影响，比如图片拼接、漏掉某张图片的分析结果）
"""
import sys
sys.path.append("/mnt/home/project/Cygnus")

from app.common.redis import RedisQueue

import subprocess
import psutil
# import torch
from logger.logger import CygnusLogger as logger



class SystemInfo:

    __instance = None

    @staticmethod
    def get_instance():
        if SystemInfo.__instance is None:
            SystemInfo.__instance = SystemInfo()
        return SystemInfo.__instance

    # @staticmethod
    # def gpu():
    #     # 判断显存是否存在
    #     if not torch.cuda.is_available():
    #         return True
    #     else:
    #         return None

    @staticmethod
    def internal_storage():
        # 获取内存信息
        mem = psutil.virtual_memory()
        percent = round(mem.percent, 2)

        return percent

    # 写一个判断是否存活接口，超时30s，就判断为故障，提示用户重启机器，并把go模块、写入模块、算法模块重启
    @staticmethod
    def ping_ip(ip="192.168.3.15"):
        # if subprocess.call(["ping", "-c", "2", ip]) == 0:
        #     return None
        # else:
        #     return True
        return None

    def get_disk_info(self):
        # 检测磁盘使用情况
        result = self.run_cmd()
        result = result.split('\n')

        for line in result:
            if 'mnt' in line:
                print(line)
                line = line.split()
                return int(line[4].split("%")[0])

    @staticmethod
    def run_cmd():
        process = subprocess.Popen('df -h', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_f, error_f = process.stdout, process.stderr
        errors = error_f.read()
        if errors:
            pass
        result = result_f.read().decode()
        if result_f:
            result_f.close()
        if error_f:
            error_f.close()
        return result

    @staticmethod
    def receive_image_info():
        err_info = RedisQueue.get_instance().pop("err")

        if err_info:

            if type(err_info) == str:
                return err_info
            info = err_info.decode()
            return info

        else:
            return None

    @staticmethod
    def receive_task_info():
        err_info = RedisQueue.get_instance().pop("task_info")

        if err_info:

            if type(err_info) == str:
                return err_info

            task_info = err_info.decode()
            return task_info

        else:
            return None

    @staticmethod
    def receive_hardware_info():
        # print(client.llen("hardware_info"))
        hardware_info_str = RedisQueue.get_instance().pop("hardware_info")

        if hardware_info_str:

            if type(hardware_info_str) == str:
                return hardware_info_str

            hard_info = hardware_info_str.decode()
            return hard_info

        else:
            return None


# def send_image_info(seaweed):
#     RedisQueue.get_instance().push("err", seaweed)
#
#
# def monitor_python_process():
#     process = subprocess.Popen("ps -ef|grep -E "
#                                "'TXTWP|TXTWR|TXTWW'", shell=True, stdout=subprocess.PIPE,
#                                stderr=subprocess.PIPE)
#     result_f, error_f = process.stdout, process.stderr
#     errors = error_f.read()
#     if errors:
#         pass
#     result = result_f.read().decode()
#     if result_f:
#         result_f.close()
#     if error_f:
#         error_f.close()
#
#     result = result.split('\n')
#     monitor_process_list = []
#     for line in result[0:-1]:
#
#         if "grep" not in line:
#             line = line.split()
#             monitor_process_list.append(line[-1])
#
#     print(monitor_process_list)
#     return monitor_process_list
#
#
# def monitor_go_process():
#     process = subprocess.Popen('ps -ef|grep main4.go', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     result_f, error_f = process.stdout, process.stderr
#     errors = error_f.read()
#     if errors:
#         pass
#     result = result_f.read().decode()
#     if result_f:
#         result_f.close()
#     if error_f:
#         error_f.close()
#
#     result = result.split('\n')
#     monitor_process_list = []
#     for line in result[0:1]:
#         line = line.split()
#         monitor_process_list.append(line[-1].split("/")[-1])
#
#     return monitor_process_list
#
#
# def monitor_run():
#     monitor_process_list = []
#     monitor_python_process_list = monitor_python_process()
#     monitor_go_process_list = monitor_go_process()
#
#     monitor_process_list.extend(monitor_python_process_list)
#     monitor_process_list.extend(monitor_go_process_list)
#
#     if "TXTWW" not in monitor_process_list:
#         # err = "数据记录白模块,运行失败，即将重启该模块"
#         err = "数据记录白模块,运行失败"
#         send_image_info(err)
#         logger.error(err)
#         # command = "/home/xiaoying/project/Draco-V2.2/sh_folder/kill_process"
#         # subprocess.Popen(command, shell=True)
#
#     if "TXTWR" not in monitor_process_list:
#         # err = "数据记录红模块,运行失败，即将重启该模块"
#         err = "数据记录红模块,运行失败"
#         send_image_info(err)
#         logger.error(err)
#         # command = "/home/xiaoying/project/Draco-V2.2/sh_folder/kill_process"
#         # subprocess.Popen(command, shell=True)
#
#     if "TXTWP" not in monitor_process_list:
#         # err = "数据记录血小板浓度模块,运行失败，即将重启该模块"
#         err = "数据记录血小板浓度模块,运行失败"
#         send_image_info(err)
#         logger.error(err)
#
#     if "main" not in monitor_process_list:
#         # err = "图片处理模块,运行失败，即将停止整个任务，并重启系统"
#         err = "图片处理模块,运行失败，需要重启系统"
#         send_image_info(err)
#         logger.error(err)
#         # os.system(os.path.join(ROOT, "/sh_folder/draco_core"))
#         # return response_data.get("info", {})
#
#     if SystemInfo.get_instance().gpu():
#         err = "显卡不存在"
#         send_image_info(err)
#         logger.error(err)
#
#     # if internal_storage():
#     #
#     #     err = "内存使用超过90%"
#     #     send_image_info(err)
#     #     log.logger.critical(err)
#
#     # if ping_ip():
#     #
#     #     err = "硬件服务器不可用"
#     #     send_image_info(err)
#     #     # stop_result = stop_scan()
#     #     log.logger.critical(err)
#     #     # print(stop_result)
#
#
# if __name__ == '__main__':
#
#     while True:
#         monitor_run()
#         time.sleep(2)
