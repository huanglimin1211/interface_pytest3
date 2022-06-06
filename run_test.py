import os,sys
import  pytest
from time import  sleep


if __name__ == '__main__':
    # pytest.main('-s', '-v', '--alluredir', './result')  #会报错，不需要参数，所以在pytest.ini里添加命令行参数
    pytest.main()
    sleep(2)
    os.system("allure generate ./result/ -o ./report/ --clean")