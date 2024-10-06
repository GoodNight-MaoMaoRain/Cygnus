import base64
import requests
import json

# from starlette import requests

TimeOutSeconds = 3  # 超时时间
# url = "http://127.0.0.1:8010"
# url = "http://192.168.100.2:8080/command"
# url = "http://192.168.100.1:8080/command"
# url = "http://192.168.3.173:8080/command"
url = "http://192.168.100.2:8080/command"


# url = "http://127.0.0.1:18080/command"

class HttpClient:
    __instance = None

    @staticmethod
    def get_instance():
        if HttpClient.__instance is None:
            HttpClient.__instance = HttpClient()
        return HttpClient.__instance

    @staticmethod
    def out_slide_to_emergency(slot):
        """
        outSlide
        退出玻片
        """

        request_data = {"slot": slot}
        response_data_json = requests.post(url=url + "/moveSlideToEmergency", data=json.dumps(request_data),
                                           timeout=600)
        response_data = json.loads(response_data_json.text)

        print(response_data)

        return response_data

    @staticmethod
    def reset_oil_percent():
        """
        reset_oil
        输入：无
        输出：json格式，包括但不限于
        result，取值为Success或者Failure，Success表示API请求成功
        """

        request_data = {}
        response_data_json = requests.post(url=url + "/resetOil", data=json.dumps(request_data))
        response_data = json.loads(response_data_json.text)
        print(response_data)
        return response_data

    @staticmethod
    def set_task_id(request_data):
        """
        setTaskID
        给与当前等待任务一个任务ID
        输入：按照槽位排列的taskID，形如[73,74,75,76,,,,,,,,]
        输出：
        json格式，包括但不限于
        • result，取值为Success或者Failure，Success表示API请求成功
        """

        response_data_json = requests.post(url=url + "/setTaskID", data=json.dumps({"taskID": request_data}))
        response_data = json.loads(response_data_json.text)

        print(response_data)
        return response_data

    @staticmethod
    def revise_task_sequence(request_data):
        """
        修改当前设备的任务执行顺序。如果查询失败，则返回Failure
        输入：需要修改的任务队列
        输出：
        json格式，包括但不限于
        	result，取值为Success或者Failure，Success表示API请求成功
        	taskList，修改后的任务队列，排名靠前的优先扫描。内部每个元素取值如下：
        	硬件内部编号，取值为int，不能为空
        	任务ID，不能为空，需要软件分配一个任务ID
        	扫描模式，不能为空
        """

        # request_data = {'taskList': [{'internalID': 1, 'taskID': 23, 'scanMode': 'area'},
        #                              {'internalID': 2, 'taskID': 24, 'scanMode': 'area'}]}
        print("reviseTaskSequence data is ", request_data)
        response_data_json = requests.post(url=url + "/reviseTaskSequence",
                                           data=json.dumps({"taskID": request_data}))
        response_data = json.loads(response_data_json.text)
        print(json.loads(response_data_json.content))

        print("reviseTaskSequencereceive from down machine ", response_data)
        return response_data

    @staticmethod
    def revise_task_scan_mode(task_id_list, new_scan_mode):
        """
        修改当前设备的任务执行顺序。如果查询失败，则返回Failure
        输入：需要修改的任务队列,new scan mode
        输出：
        json格式，包括但不限于
        	result，取值为Success或者Failure，Success表示API请求成功
        	taskList，修改后的任务队列，排名靠前的优先扫描。内部每个元素取值如下：
        	硬件内部编号，取值为int，不能为空
        	任务ID，不能为空，需要软件分配一个任务ID
        	扫描模式，不能为空
        """

        # request_data = {'taskList': [{'internalID': 1, 'taskID': 23, 'scanMode': 'area'},
        #                              {'internalID': 2, 'taskID': 24, 'scanMode': 'area'}]}
        response_data_json = requests.post(url=url + "/reviseTaskScanMode",
                                           data=json.dumps({"taskID": task_id_list, "newScanMode": new_scan_mode}))
        response_data = json.loads(response_data_json.text)

        print(response_data)
        return response_data

    @staticmethod
    def query_scan_parameter():
        """
        queryScanParameter
        查询当前扫描任务的参数。
        输入：无
        输出：
        	硬件内部编号
        	扫描步长stepLength，单位um，如100
        	扫描推进步数stepNumber，如1000
        	扫描起点坐标startCoordinate，如{“x“:100, “y“:100}
        	起点终点行列号scanArea，如{‘White’: {“x“:100, “y“:100, “x1“:400, “y1“:400}, ‘Red: {“x“:100, “y“:100, “x1“:400, “y1“:400}]
        	文件格式format: string格式，如jpg，png
        	任务ID taskID，取值为int，是该任务的ID号，如15；
        	缩略图thumnail，bytes格式
        	最大包络信息bloodBox，如[{“x“:100, “y“:100}, {“x“:400, “y“:400}]
        """

        request_data = {}
        response_data_json = requests.post(url=url + "/queryScanParameter", data=json.dumps(request_data))
        response_data = json.loads(response_data_json.text).get("info")

        step_length = response_data.get("stepLength")
        step_number = response_data.get("stepNumber")
        scan_area = response_data.get("scanArea")
        blood_box = response_data.get("bloodBox")
        image_format = response_data.get("format")
        task_id = response_data.get("taskID")
        thumbnail = response_data.get("thumbnail")

        with open("query_scan_thumbnail.jpg", "wb") as file:
            file.write(base64.b64decode(thumbnail))

        print("query_scan_parameter")
        return response_data.get("info", {})

    @staticmethod
    def stop_scan(task_id_list, reason):
        """
        stopScan
        停止当前扫描任务。该命令为阻塞操作，只有执行完所有现场清理工作、硬件收尾完成才会返回结果。
        输入：任务ID列表，json格式，形如[1,2,3,4]
        输出：json格式，包括但不限于
        result，取值为Success或者Failure，Success表示API请求成功
        """
        request_data = {"task_id_list": task_id_list, "reason": reason}
        response_data_json = requests.post(url=url + "/stopScan", data=json.dumps(request_data), timeout=20)
        response_data = json.loads(response_data_json.text)
        print(response_data)
        return response_data

    @staticmethod
    def get_task_status():
        """
        查询当前设备的所有任务状态。如果查询失败，则返回Failure
        输入：无
        输出：json格式，包括但不限于
        	result，取值为Success或者Failure，Success表示API请求成功
        	scannerID，取值INT，硬件唯一标识
        	taskList，当前所有任务队列，排名靠前的优先扫描。内部每个元素取值如下：
        	internalID, 硬件内部编号，取值为int，不能为空
        	status，取值为scan或者prescan或者idle或者finish或者failure，代表正在扫描、预扫描、空闲、完成、失败六种状态
        	玻片ID，取值为string，可以为空
        	任务ID，可以为空
        	扫描模式scanMode
        	progress，取值为int，是当前扫描任务已完成的图片数量。预扫描阶段扫出来的图片不计入数量，该值为0。

        """

        request_data = {}
        response_data_json = requests.post(url=url + "/getTaskStatus", data=json.dumps(request_data),
                                           timeout=TimeOutSeconds)
        response_data = json.loads(response_data_json.text)
        print("getTaskStatus response_data is ", response_data)
        return response_data.get("info", {})

    @staticmethod
    def start_scan(model_type):
        """
        startScan
        启动扫描任务。该命令为阻塞操作。
        输入：无
        输出：json格式，包括但不限于
        result，取值为Success或者Failure，Success表示API请求成功
        """

        request_data = {"moduleType": model_type}
        response_data_json = requests.post(url=url + "/startScan", data=json.dumps(request_data))
        response_data = json.loads(response_data_json.text)
        print(response_data)
        return response_data

    @staticmethod
    def query_module_status():
        """
        查询当前各个模块是否工作正常
        输入：无
        输出：json格式，包括
        	result，取值为Success或者Failure，Success表示API请求成功
        	油量（immersion_oil）、盖子(cover_closed)、机器温度过高(temperature_over_high)、机器是否水平(is_horizontal)等信息，取值为true或者false

        """

        request_data = {}

        try:
            response_data_json = requests.post(url=url + "/queryModuleStatus", data=json.dumps(request_data),
                                               timeout=TimeOutSeconds)
        except:
            return None, None, None, None, None, None, None

        try:
            response_data = json.loads(response_data_json.text)
        except:
            return None, None, None, None, None, None, None

        result = response_data.get("result")
        # print(response_data)

        if result != "Success":
            return None, None, None, None, None, None, None

        else:
            # {'oil_low': False, 'cover_closed': False, 'is_horizontal': False, 'slide_holder': False,
            #  'temperature_overhigh': False, 'result': 'Success'}
            immersion_oil = response_data.get("oil_percent")
            cover_closed = response_data.get("cover_closed")
            slide_holder = response_data.get("slide_holder")
            temperature_over_high = response_data.get("temperature_overhigh")
            is_horizontal = response_data.get("is_horizontal")
            device_status = response_data.get("device_status")
            error_code = response_data.get("error_code")

            if immersion_oil:
                immersion_oil = round(immersion_oil * 100, 2)

            return immersion_oil, cover_closed, slide_holder, temperature_over_high, is_horizontal, device_status, error_code

    @staticmethod
    def query_hardware_status():
        """
            查询硬件当前各个模块是否工作正常
            输入：无
            输出：json格式，包括
            	result，取值为Success或者Failure，Success表示API请求成功
            	取值为true或者false

            """

        request_data = {}

        try:
            response_data_json = requests.post(url=url + "/queryHardwareStatus", data=json.dumps(request_data),
                                               timeout=TimeOutSeconds)
        except:
            return None

        try:
            response_data = json.loads(response_data_json.text)
        except:
            return None

        result = response_data.get("result")
        # print(response_data)

        if result != "Success":
            return None

        else:
            return response_data

    @staticmethod
    def query_QRcamera_picture():
        """
        查询下位机二维码相机拍照图片
        输入：无
        输出：json格式，包括
        	result，取值为Success或者Failure，Success表示API请求成功
        	取值为true或者false

        """

        request_data = {}

        try:
            response_data_json = requests.post(url=url + "/getPhoto", data=json.dumps(request_data),
                                               timeout=TimeOutSeconds)
        except:
            return None

        try:
            response_data = json.loads(response_data_json.text)
        except:
            return None

        result = response_data.get("result")
        # print(response_data)

        if result != "Success":
            return None

        else:
            return response_data

    @staticmethod
    def get_log():
        """
        getLog
        获取硬件日志
        输入：无
        输出：文件?
        result，取值为Success或者Failure，Success表示API请求成功
        """

        # request_data = {"log_date": model_type}
        request_data = {"log_date": "2024-04-14"}
        response_data_json = requests.post(url=url + "/getLog", data=json.dumps(request_data))
        response_data = json.loads(response_data_json.text)
        for data_name,value in response_data.items():
            if data_name == 'logData':
                response_data = value
        print(response_data)
        return response_data

    @staticmethod
    def hardware_shutdown():
        """
        shutdown
        关闭下位机
        输入：无
        输出：json格式，包括但不限于
        result，取值为Success或者Failure，Success表示API请求成功
        """

        request_data = {}
        response_data_json = requests.post(url=url + "/shutdown", data=json.dumps(request_data))
        response_data = json.loads(response_data_json.text)
        print(response_data)
        return response_data


if __name__ == '__main__':
    print(HttpClient.get_instance().query_module_status())
    # print(HttpClient.get_instance().get_log())
    # start_scan("all")
    # set_task_id([1, 2, 3, 0, 4, 5, 0, 6, 0, 0, 0])
    # stop_scan([1], "ManualStop")
    # # pass
    # revise_task_sequence([1])
    # reason0 = "ReachWhiteModuleLimit"
    # print(HttpClient.get_instance().stop_scan(["1520"], reason0))
