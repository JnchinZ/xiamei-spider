# encoding:utf8
import re
import os
import time
import requests
from urllib import request

root_url = r'https://www.nvshens.com'

#请求头
header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
}
#代理
proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}
def get_album_urls(girl_num):
    '''
    获得夏美酱的专辑号列表
    https://www.nvshens.com/girl/21501/
    :param girl_num:夏美酱的编号
    :return:专辑url列表和专辑号列表
    '''
    album_list_url = root_url + '/girl/' + str(girl_num) + '/album/'
    res_txt = requests.get(album_list_url, headers=header, proxies = proxies).text

    # 找出每个专辑的编号
    re_img = re.compile(r"<a class='igalleryli_link' href='/g/[0-9]+/' >")
    album_label_list = re.findall(re_img, res_txt)
    album_num_list = re.findall(re.compile(r'[0-9]+'), str(album_label_list))

    # 由编号组成专辑url
    album_urls_list = []
    for album_num in album_num_list:
        album_urls_list.append(root_url + '/g/' + album_num + '/')
    return album_urls_list, album_num_list


def get_pic_num(album_num):
    '''
    抓取一个专辑中的所有大图url
    https://www.nvshens.com/g/24191/2.html
    :param album_num: 专辑号
    :return: 大图url列表
    '''
    pic_url_list = []

    #获取这个专辑中所有的页
    page_url_list = ['/g/22377/1.html']
    n_page_num = 1
    while True:
        pri_album_url = 'https://www.nvshens.com/g/' + album_num + '/' + str(n_page_num) + '.html'
        pri_res_txt = requests.get(pri_album_url).text
        short_page_url_list = re.findall(r"/g/" + album_num + "/[0-9]+.html", pri_res_txt)
        if short_page_url_list[-2] == short_page_url_list[-1]:
            page_url_list.append(short_page_url_list[-1])
            break
        else:
            page_url_list.append(short_page_url_list[-1])
            n_page_num += 1

    #抓取每页的大图url
    for page_url in page_url_list:
        album_url = root_url+page_url
        res_txt = requests.get(album_url).text

        #       "https://t1.onvshen.com:85/gallery/17596/22747/s/0.jpg"
        # src = "https://t1.onvshen.com:85/gallery/21501/24005/s/009.jpg"
        pri_url = r'https://\S+.onvshen.com:85/gallery/'
        re_img = re.compile(pri_url + '[0-9]+' +'/'+ album_num + '/s/' + '[0-9]+.jpg')
        img_url_list = re.findall(re_img, res_txt)

        if len(img_url_list)!=5:
            print(page_url+' error')

        for img_url in img_url_list:
            index_str = img_url.index('s/')
            pic_url_list.append(img_url[:index_str]+img_url[index_str+2:])
    return pic_url_list

#根据图片url下载图片
def save_pic(pic_url, file_name):
    # pic_url = https: // t1.onvshen.com: 85 / gallery / 21501 / 24005 / 0.jpg
    fi = open(file_name, 'wb')
    try:
        fi.write(request.urlopen(pic_url).read())
    except:
        raise
    finally:
        fi.close()

#获取所有大图url并保存
def save_all_urls(girl_num):
    album_urls_list, album_num_list = get_album_urls(girl_num)
    f = open('all_urls.txt','w')
    for album_num in album_num_list:
        pic_url_list = get_pic_num(album_num)
        for pic_url in pic_url_list:
            f.write(pic_url+'\n')
    f.close()
    return 'All OK!'


#开始抓取
def start_sys(girl_num):
    album_urls_list, album_num_list = get_album_urls(girl_num)
    for album_num in album_num_list:
        unknown_pic_urls = open(r'unknown_pic_urls.txt', 'a')
        pic_url_list = get_pic_num(album_num)
        if pic_url_list == []:
            print(album_num+' album is null!')
            continue
        file_path = r'.\xiameijiang\\'+album_num
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        for pic_num, pic_url in enumerate(pic_url_list):
            file_name = file_path+'\\'+str(pic_num)+'.jpg'
            if os.path.exists(file_name):
                print(file_name + ' has been existed!')
                continue
            else:
                pri_time = time.time()
                try:
                    save_pic(pic_url, file_name)
                except:
                    #删除失败文件
                    os.remove(file_name)
                    #在unknown_pic_urls.txt中写入失败的图片url和本应该存放的路径+文件名
                    unknown_pic_urls.write(pic_url+','+file_name+'\n')
                    print('the '+file_name+' pic is error, has broke and delete! <---------error!')
                    time.sleep(1)
                    continue
                else:
                    #如果没有异常执行这块代码
                    print(file_name+' has been saved! In '+str(time.time()-pri_time)+' seconds!')
                    time.sleep(3)
        unknown_pic_urls.close()
    return 'All Done!'

def del_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        pass
if __name__ == '__main__':
    girl_num = "21501"#夏美酱的编号

    # 代码A
    fail_url_filename = r'unknown_pic_urls.txt'
    del_file(fail_url_filename)
    tips = start_sys(girl_num)
    print(tips)

    #代码B
    tips = save_all_urls(girl_num)
    print(tips)