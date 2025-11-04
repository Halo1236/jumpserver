import requests
import requests.exceptions


def cert_check(serial_number: str) -> (bool, str):
    """
    检查证书状态
    :param serial_number: 证书ID
    :return: 证书状态, 证书详情
    """

    headers = {
        'Authorization': 'token xxxxxx',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.get(
            f'http://secca.devops.sit.xiaohongshu.com/ca/api/v1/cert/verify?serialNumber={serial_number}', headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200 and data['data']['status'] == 'VALID':
                return True, ''
            return False, data['message']
        return False, str(response.status_code)
    except Exception as e:
        return False, str(e)
