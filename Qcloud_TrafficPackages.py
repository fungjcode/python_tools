#!/usr/bin/python3
# -*-coding:UTF-8-*-

# 风之翼灵
# www.fungj.com

"""
腾讯云 轻量云监控流量超标自动关机
"""

import json
import os
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models

def main(SecretId, SecretKey, region, InstanceIds, all_proportion):
    """
    GOGO
    :param SecretId: str 腾讯云账号SecretId
    :param SecretKey: str 腾讯云账号SecretKey
    :param region: str 实例地域
    :param InstanceIds: str 实例ID
    :param all_proportion: int 预警值
    """
    qrest = qcloud(SecretId, SecretKey, region, InstanceIds)
    if qrest != False:
        # 取数
        TrafficPackageSet = qrest['InstanceTrafficPackageSet'][0]['TrafficPackageSet']
        # 使用量
        TrafficUsed = TrafficPackageSet[0]['TrafficUsed']
        # 总量
        TrafficPackageTotal = TrafficPackageSet[0]['TrafficPackageTotal']
        # 使用比例,保留两位小数
        use_proportion = round(TrafficUsed / TrafficPackageTotal, 2)
        print('当前流量使用比例为：{0}%'.format(use_proportion * 100))
        # 判断使用量是否超标
        if use_proportion > all_proportion:
            # 超标，关机保平安
            print('当前流量已经使用操作预警值，服务器将在3秒钟后关闭...')
            shut_down()
        else:
            # 没有超标，结束脚本
            print('流量正常...')
            time.sleep(3)
            exit()


def qcloud(SecretId, SecretKey, region, InstanceIds):
    """
    腾讯云的SDK不管他
    :param SecretId: str 腾讯云账号SecretId
    :param SecretKey: str 腾讯云账号SecretKey
    :param region: str 实例地域
    :param InstanceIds: str 实例ID
    :return: json 腾讯云实例流量情况
    """
    try:
        cred = credential.Credential(SecretId, SecretKey)
        region = region
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lighthouse.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
        req = models.DescribeInstancesTrafficPackagesRequest()
        params = {
            "InstanceIds": [InstanceIds]
        }
        req.from_json_string(json.dumps(params))

        resp = client.DescribeInstancesTrafficPackages(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(err)
        return False


def shut_down():
    """
    关闭系统
    """
    os.system('shutdown -s -t 3')

if __name__ == '__main__':
    """
    腾讯云API库安装
    pip install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python
    流量包解释
    https://cloud.tencent.com/document/api/1207/47576#InstanceTrafficPackage
    腾讯云账号ID获取地址
    https://console.cloud.tencent.com/cam/capi
    实例地域
    "ap-beijing", "ap-chengdu", "ap-guangzhou", "ap-hongkong", "ap-nanjing", "ap-shanghai", "ap-singapore", "ap-tokyo", "eu-moscow", "na-siliconvalley"
    """
    # SecretId
    SecretId = "你的SecretId"
    # SecretKey
    SecretKey = "你的SecretKey"
    # 实例地域
    region = "你的实例地域"
    # 轻量云实例ID
    InstanceIds = "你的轻量云实例ID"
    # 预计比例0.95代表95%，0.9就是90%，具体自行修改
    all_proportion = 0.95
    # 执行
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('---------' + str(nowtime) + ' 程序开始执行------------')
    main(SecretId, SecretKey, region, InstanceIds, all_proportion)
