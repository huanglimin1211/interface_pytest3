def digital(s):
    try:
        float(s)
        print("字符串是数字")
        # return True
    except:
        pass
        print("字符串不是数字")
    # return  False



current_users=['Niuniu','Niumei','GurR','LoLo']
new_users=['GurR','Niu Ke Le','LoLo','Tuo Rui Chi']
for i  in new_users:
    if  i  in current_users:
        print('The user name %s has already been registered! Please change it and try again!' %i)
    else:
        print('Congratulations, the user name  %s is available!' %i)

if __name__ == '__main__':
    print(digital('aaa'))