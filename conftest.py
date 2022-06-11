import os,requests,pytest


'''conftest.py 测试用例的一些fixture配置
pytest.ini 它是pytest的主配置文件，可以改变pytest的默认行为'''
#不同测试环境切换，通过一个变量os.environ['host']来维护
# def pytest_addoption(parser):
#     parser.addoption(
#         "--cmdhost",
#         action='store',
#         default='https://jieroutest.digitalexpo.com',
#         help='test case project host address'
#     )
#
# @pytest.fixture(scope="session",autouse=True)
# def host(request):
#     os.environ['host']=request.config.getoption('--cmdhost')
#     print(os.environ['host'])
#     print("当前用例有运行的测试环境:%s"%os.environ['host'])