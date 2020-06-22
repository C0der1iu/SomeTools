import requests
import sys
import time

#  判断是否断网，按挂机需求修改秒数，一般为了夜间做种建议5秒一check

def checker():
    try:
        checker = requests.get('http://www.recorday.cn')
        #print(checker.text)
        if 'eportal' in checker.text:
            params = checker.text.split('jsp?')[1].split('\'</')[0]
            return params
        else:
            return False
    except Exception:
        return False


if __name__ == "__main__":
    if len(sys.argv)== 3:
        username = sys.argv[1]
        password = sys.argv[2]
        url = 'http://172.26.156.158/eportal/InterFace.do?method=login'
        Login_Headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': '172.26.156.158',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip,deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
        }
        while True:
            params = checker()
            if params:
                Logn_Data = {
                     'userId' : username,
                     'password' : password,
                     'service' : '',
                     'queryString' : params,
                     'operatorPwd' : '',
                     'operatorUserId' : '',
                     'validcode' : ''
                     }
                requests.post(url,headers=Login_Headers,data=Logn_Data)
            else:
                time.sleep(5)
    else:
        print(
        '''
        You Input An Error Params
        Usage：WebDoctor.py username password
        '''
        )
        exit()
