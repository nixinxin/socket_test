import requests
import threading

def music():
    url = "http://172.16.1.210:1322"

    response = requests.request("GET", url)
    print(response.text)


if __name__ == '__main__':
    for i in range(1001):
        music()

