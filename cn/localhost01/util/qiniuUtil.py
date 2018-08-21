# encoding: utf-8
from cn.localhost01.__init__ import qiniu_ak, qiniu_sk, qiniu_bucket, qiniu_domain
from qiniu import Auth, put_file
import os

# 构建鉴权对象
auth = Auth(qiniu_ak, qiniu_sk)


def upload_file(local_path):
    # 0.获取文件名
    new_file_name = os.path.basename(local_path)
    # 1.获取上传token
    token = auth.upload_token(qiniu_bucket, new_file_name)
    # 2.上传
    ret, info = put_file(token, new_file_name, local_path)

    if info.status_code == 200:
        return qiniu_domain + "/" + new_file_name
    return None
