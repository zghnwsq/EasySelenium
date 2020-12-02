from xmlrpc.client import ServerProxy
import Settings

if __name__ == '__main__':
    server = ServerProxy("http://%s:%d" % (Settings.RPC_Server, Settings.RPC_Server_Port))  # 初始化服务器
    try:
        # ConnectionRefusedError
        is_alive = server.is_alive()
        # ret = server.test_run_web(mth='b', rg='1', comment='备注')  # 调用函数1并传参
        ret = server.test_run_api(mth='all', comment='备注')  # 调用函数并传参
        print(ret)
    except TimeoutError as time_out:
        print(time_out)
    except ConnectionRefusedError as e:
        print(e)



