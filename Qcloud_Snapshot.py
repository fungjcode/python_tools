#!/usr/bin/python3
# -*-coding:UTF-8-*-

# 风之翼灵
# www.fungj.com

"""
腾讯云轻量云自动进行快照备份
轻量云免费提供2个快照，所以该脚本只备份两个快照
"""

import json
import os
import time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.lighthouse.v20200324 import lighthouse_client, models


def main(SecretId, SecretKey, region, InstanceIds):
    """
    GOGO
    :param SecretId: str 腾讯云账号SecretId
    :param SecretKey: str 腾讯云账号SecretKey
    :param region: str 实例地域
    :param InstanceIds: str 实例ID
    """
    get_rest = get_info(SecretId, SecretKey, region, InstanceIds)
    if get_rest != False:
        TotalCount = get_rest['TotalCount']
        # 快照数
        if TotalCount < 2:
            # 直接备份
            CreateInstanceSnapshot(SecretId, SecretKey, region, InstanceIds)
        elif TotalCount == 2:
            # 删除之前较早一个备份,就是列表里的第二个,状态需要正常才能删除
            SnapshotState = (get_rest['SnapshotSet'][1]['SnapshotState'])
            if SnapshotState == 'NORMAL':
                SnapshotId = (get_rest['SnapshotSet'][1]['SnapshotId'])
                DeleteSnapshots_re = DeleteSnapshots(SecretId, SecretKey, SnapshotId, region)
                if DeleteSnapshots_re != False:
                    # 删除之前一个后，再进行备份
                    print('已经删除完成快照ID为{0}的快照，现在准备开始备份实例'.format(SnapshotId))
                    CreateInstanceSnapshot(SecretId, SecretKey, region, InstanceIds)
        else:
            print('当前快照数量存在问题，请登录腾讯云后台检查并删除多余的快照后操作')
            time.sleep(5)
            exit()


def CreateInstanceSnapshot(SecretId, SecretKey, region, InstanceIds):
    """
    创建快照
    """
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lighthouse.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
        req = models.CreateInstanceSnapshotRequest()
        params = {
            "InstanceId": InstanceIds
        }
        req.from_json_string(json.dumps(params))
        resp = client.CreateInstanceSnapshot(req)
        resp_re = json.loads(resp.to_json_string())
        SnapshotId = resp_re['SnapshotId']
        print('轻量云快照备份完成，快照ID为：{0},程序在5秒钟后关闭'.format(SnapshotId))
        time.sleep(5)
        exit()

    except TencentCloudSDKException as err:
        print(err)
        return False


def DeleteSnapshots(SecretId, SecretKey, SnapshotId, region):
    """
    删除快照
    """
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lighthouse.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = lighthouse_client.LighthouseClient(cred, region, clientProfile)

        req = models.DeleteSnapshotsRequest()
        params = {
            "SnapshotIds": [SnapshotId]
        }
        req.from_json_string(json.dumps(params))
        resp = client.DeleteSnapshots(req)
        return json.loads(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)
        return False


def get_info(SecretId, SecretKey, region, InstanceIds):
    """
    获取快照信息
    :param SecretId: str 腾讯云账号SecretId
    :param SecretKey: str 腾讯云账号SecretKey
    :param region: str 实例地域
    :param InstanceIds: str 实例ID
    :return: json 腾讯云实例流量情况
    """
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "lighthouse.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = lighthouse_client.LighthouseClient(cred, region, clientProfile)
        req = models.DescribeSnapshotsRequest()
        params = {
        }
        req.from_json_string(json.dumps(params))
        resp = client.DescribeSnapshots(req)
        return json.loads((resp.to_json_string()))
    except TencentCloudSDKException as err:
        print(err)
        return False


if __name__ == '__main__':
    """
    腾讯云API库安装
    pip install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python
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
    # 执行
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('---------' + str(nowtime) + ' 程序开始执行------------')
    main(SecretId, SecretKey, region, InstanceIds)
