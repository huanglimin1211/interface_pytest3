import  yaml

class ReadYaml():
    def __init__(self,yaml_path=None):
        if yaml_path==None:
            self.yaml_path="../data/test_data.yml"
        else:
            self.yaml_path=yaml_path


    def read_y(self) -> object:
        with open(self.yaml_path,'r',encoding='utf-8') as  f:
            f_read=f.read()
            data=yaml.load(f_read,Loader=yaml.FullLoader)
        return data


if __name__ == '__main__':
    read=ReadYaml()
    r=read.read_y()
    print(r['test_data_login'][0]['account'])