import math
#计算两个用户的相似度
def euclid(user1,user2):
    """
    :param user1:
    user={
        "moviename":"score",
    }
    :param user2:
    :return:

    """
    #两人的相似距离
    distance=0
    for key in user1.keys():
        #是否含有相同电影评分
        if key in user2.keys():
            distance+=pow(float(user1[key])-float(user2[key]),2)
    return 1/(1+math.sqrt(distance))

#计算有个用户和其他用户相对比

def top_similar(user,user_all):
    """
    :param user: 当前用户的电影字典user={"moviename":"score"}
    :param user_all: 所有用户user_all={"user":{"moviename":"score",},}
    :return:
    """
    resualt=[]
    for user_other in user_all.keys():
        if not user_other==user:
            similiar=euclid(user,user_other)
            resualt.append((user.id,similiar))

    resualt.sort(key=lambda val:val[1])
    return resualt

def reconmment(user,user_all):
    #获得匹配度较高的人
    top_user=top_similar(user,user_all)[0][0]
    #相似度高的用户所看电影信息
    items=user_all[top_user]
    #推荐列表
    reconmmend_list=[]
    #排除自己的
    for item in items.keys():
        if item not in user_all[user].keys():
            reconmmend_list.append((item,items[item]))

    reconmmend_list.sort(key=lambda val:val[1])
    return reconmmend_list