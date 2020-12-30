from xmlrpc.client import ServerProxy
import Settings

if __name__ == '__main__':
    server = ServerProxy("http://%s:%d" % (Settings.RPC_Server, Settings.RPC_Server_Port), allow_none=True)  # 初始化服务器
    try:
        # ConnectionRefusedError
        is_alive = server.is_alive()
        print(is_alive)
        # ret = server.Demo_Web({'mth': 'b', 'rg': '1', 'comment': '备注'})  # 调用函数1并传参
        # ret = server.Demo_Api({'mtd': 'all', 'rg': None, 'comment': '', 'tester': 'TED'})  # 调用函数并传参
        ret = server.Demo_Api_GH1018Q1({'mtd': 'test_GH1018Q1_valid', 'rg': '1', 'comment': None, 'tester': 'TED'})
        print(ret)
    except TimeoutError as time_out:
        print(time_out)
    except ConnectionRefusedError as e:
        print(e)



