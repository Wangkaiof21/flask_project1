# a_list = [1, 10, 8, "a", 4, 2, "b", 6, 19, 9, 19, 20, 3, 2]
# c = list()

# for i in a:
#     if isinstance(i, int):
#         c.append(i)
# print(sorted(c))
# for i in a_list:
#     if type(i) != type("x"):
#         c.append(i)
#
#
# def q_sort(c):
#     if len(c) <= 0: return c
#     return q_sort([x for x in c[1:] if x < c[0]]) + c[0:1] + q_sort([d for d in c[1:] if d >= c[0]])
#
#
# print(q_sort(c))


# """一个数据先递增再递减，找出数组中不重复的个数
# """
#
# vv = [1, 3, 4, 5, 8, 10, 9, 4, 3, 1]
# index = None
# c_list = dict()
#
# for i in range(len(vv)):
#     if vv[i] in c_list:
#         c_list[vv[i]] += 1
#     else:
#         c_list[vv[i]] = 1
#
# for l in c_list:
#     if c_list[l] == 1:
#         index = l
#         break
# print(c_list)

import pytest
import allure


class TestCase:
    @allure.title('登录用例')
    def test_01(self):
        '''登录用例_操作步骤'''
        with allure.step('输入正确的用户名'):
            print('输入用户名')
        with allure.step('输入正确的密码'):
            print('输入密码')
        with allure.step('点击登录'):
            print('点击登录！')
        assert 1

    @allure.title('退出登录用例')
    def test_02(self):
        '''退出登录_操作步骤'''
        with allure.step('点击退出按钮'):
            print('成功点击退出按钮')
        assert 1


if __name__ == '__main__':
    pytest.main(['-s'])

import pytest
import allure
import requests


class Client:
    """
（1）编程语言：Python
（2）Client()类由于模拟客户端（请忽略登录、初始化等前置操作）
（3）使用Client()类的方法send_recv_msg(proto_name, request_param)发送、
接收协议；proto_name（str）是协议名称，
request_param（dict）是请求参数；
该方法返回协议回包数据（dict）。
（4）基于unittest或pytest框架管理用例、校验等等；可结合ddt做数据驱动。
（5）基于allure生成测试报告。

step = {"agreement": "111",
        "id": "1",
        "body":
            {
                "areaId 0": 1,  # 目标区域id
                "cellId 1": 666  # 目标区域内的格子ID
            }
        }

response = {  # 回包数据
    "err 0": 1,  # 错误码，非0表示服务端异常
    "eventType 1": 1,  # 事件类型；怪物事件=1，宝箱事件=2
    "enemyData 2 ": 123,  # 怪物数据【怪物事件专用】
    "treasureData 3": 0,  # 宝箱数据【宝箱事件专用】
    "uInfoMap 4": 13424,  # 玩家信息
    "nextArea 5": 1,  # 玩家如果跨区前进，区域视野往前推进[到终点后就不给了]
    "eventId 6": 1  # 事件id，自增；怪物事件从1001开始，宝箱事件从2001开始
}


    """

    @allure.title('result用例')
    def __init__(self, proto_name="111"):
        if proto_name != "111":
            assert False
        else:
            self.proto_name = proto_name
        self.success_code = "202"
        self.request_param = {"agreement": self.proto_name,
                              "id": id,
                              "body":
                                  {
                                      "areaId 0": 0,  # 目标区域id
                                      "cellId 1": 0  # 目标区域内的格子ID
                                  }
                              }

    @allure.title('发送数据')
    def send_recv_msg(self, id: str, area_id: int, cell: int) -> dict:
        """

        :param id:
        :param area_id:
        :param cell:
        :return:
        """
        step = self.request_param
        step["id"] = id
        step["body"]["areaId 0"] = area_id
        step["body"]["cellId 1"] = cell

        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/54.0.2840.99 Safari/537.36"}
        response = requests.post('https://www.test.com/try/ajax/demo_post2.php', data=step, header=header)
        if response.status_code == self.success_code:
            return response.json()
        else:
            return {"key": "error"}

    @allure.title('检查返回值')
    def check_result(self) -> int:
        """
        检查返回值
        :return:
        """
        with allure.step('执行发送'):
            ret = self.send_recv_msg("01", 1, 1)
        if ret["err 0"] == 0:
            assert 0
        else:
            with allure.step('校验数据'):
                if ret["uInfoMap 4"] == 1:
                    pass
                    assert 1
                else:
                    assert 0


if __name__ == '__main__':
    pytest.main(['-s'])
