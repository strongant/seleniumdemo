# _*_coding: UTF-8_*_
import json
from locale import getpreferredencoding
import os
import gc
import re
import subprocess
import sys
import time
import datetime
from simplejson import JSONDecoder
import simplejson


def scraping_by_phantomjs(phantomjs_path,
                          scarping_js_dir_path, scarping_js_path,
                          url, output_root_dir, output_file_name,
                          width, height, charset,
                          request_timeout, request_interval_timeout, timeout,
                          cookies, headers):
    if not charset:
        charset = 'auto'
    cwd = os.getcwd()
    os.chdir(scarping_js_dir_path)
    # command = (u'{0} --ssl-protocol=any "{1}" "{2}" "{3}" "{4}" {5} {6} {7} ' +
    #            u'{8} {9} {10} "{11}" "{12}"').format(phantomjs_path,
    #                                                  scarping_js_path,
    #                                                  url, output_root_dir,
    #                                                  output_file_name,
    #                                                  width, height,
    #                                                  charset, request_timeout,
    #                                                  request_interval_timeout,
    #                                                  timeout,
    #                                                  json.dumps(cookies),
    #                                                  json.dumps(headers))
    args = [phantomjs_path,
            '--ssl-protocol=any', scarping_js_path,
            url, output_root_dir,
            output_file_name,
            width, height,
            charset, request_timeout,
            request_interval_timeout,
            timeout,
            json.dumps(cookies),
            json.dumps(headers)]
    encoding = getpreferredencoding() or 'utf-8'
    for i in range(len(args)):
        arg = args[i]
        if isinstance(arg, unicode):
            try:
                args[i] = arg.encode(encoding)
            except Exception:
                args[i] = arg.encode('utf-8', errors='ignore')
        elif not isinstance(arg, str):
            args[i] = str(arg)

    env = getattr(os, 'environb', os.environ)
    formated_env = {}
    for key, value in env.iteritems():
        if isinstance(key, unicode):
            try:
                key = key.encode(encoding)
            except Exception:
                key = key.encode('utf-8', errors='ignore')
        if isinstance(value, unicode):
            try:
                value = value.encode(encoding)
            except Exception:
                value = value.encode('utf-8', errors='ignore')
        formated_env[key] = value

    gc.collect()

    process = subprocess.Popen(args, close_fds=True, env=formated_env)
    status = process.wait()
    os.chdir(cwd)

    return status


# 进行命令调用,调用完成之后关闭子进程
def timeout_command(command, timeout):
    start = datetime.datetime.now()
    process = subprocess.Popen(command, bufsize=100000, stdout=subprocess.PIPE, close_fds=True)
    while process.poll() is None:
        time.sleep(0.1)
    now = datetime.datetime.now()
    if (now - start).seconds > timeout:
        try:
            process.terminate()
        except Exception, e:
            return None
    return None
    out = process.communicate()[0]
    if process.stdin:
        process.stdin.close()
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()
    try:
        process.kill()
    except OSError:
        pass
    return out


# 通过外部定义的参数返回网站首页代码
def download(phantomjs_path, scarping_js_path,
             url, charset,
             request_timeout, timeout,
             cookies, headers):
    args = [phantomjs_path,
            '--ssl-protocol=any', scarping_js_path,
            url, charset, request_timeout,
            timeout, json.dumps(cookies),
            json.dumps(headers)]
    env = getattr(os, 'environb', os.environ)
    formated_env = {}
    for key, value in env.iteritems():
        if isinstance(key, unicode):
            try:
                key = key.encode(charset)
            except Exception:
                key = key.encode('utf-8', errors='ignore')
        if isinstance(value, unicode):
            try:
                value = value.encode(charset)
            except Exception:
                value = value.encode('utf-8', errors='ignore')
        formated_env[key] = value
    gc.collect()
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        process = subprocess.Popen(args, close_fds=True, stdout=subprocess.PIPE, env=formated_env)
        process.wait()
        out = process.stdout.readlines()
        if process.stdin:
            process.stdin.close()
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
        try:
            process.kill()
        except OSError:
            pass
        return out
    except Exception, e:
        print e


def tryDownload():
    # 失败后重试一次,重试一次仍然失败,则按照无法访问处理
    data = download('/usr/bin/phantomjs', '../phantomjs/fetch.js', 'http://www.eatonhongkong.com/', 'utf-8',
                    str(1000 * 5),
                    str(1000 * 10), [],
                    {})
    if data is not None:
        print 'dictData:',''.join(data)
        dictData = simplejson.loads(''.join(data))
        statusCode = dictData['status']
        print statusCode
        arrs = statusCode.split(':')
        status = arrs[1]
        if status.find('success') == -1:
            gc.collect()
            time.sleep(1)
            print 'have a retry'
            # 重新下载一次
            tempData = download('/usr/bin/phantomjs', '../phantomjs/fetch.js', 'http://www.eatonhongkong.com/', 'utf-8',
                                str(1000 * 5),
                                str(1000 * 30), [],
                                {})
            dictData2 = eval(tempData)
            print 'datatemp:', dictData2.get('content')
        else:
            print 'data:', dictData.get('content')
    else:
        print '抓取失败:'


if __name__ == '__main__':
    # args = ['/usr/bin/phantomjs',
    #         '--ssl-protocol=any', '../fetch.js']
    # data = timeout_command(args, 1000 * 30)
    # if data is not None:
    #     print data
    #     # if ''.join(statusCode).find('success') == -1:
    #     #     time.sleep(3)
    #     #     # 重新下载一次
    #     #     timeout_command(args, 1000 * 60)
    #     # else:
    #     #     print 'data:', ''.join(data)
    # else:
    #     "请求超时..."
    # print data
    tryDownload()
