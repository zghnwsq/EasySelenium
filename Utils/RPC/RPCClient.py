from xmlrpc.client import ServerProxy
import Settings

if __name__ == '__main__':
    server = ServerProxy("http://%s:%d" % (Settings.RPC_Server, Settings.RPC_Server_Port))  # 初始化服务器
    try:
        ret = server.test_run_remote('a', '1', '备注')  # 调用函数1并传参
        print(ret)
    except TimeoutError:
        print('error')



