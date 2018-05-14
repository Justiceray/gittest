#coding=utf-8
import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    except:
        return "Error"
def get_content(url):
    comments = []
    html = get_html(url)
    soup = BeautifulSoup(html,'lxml')
    
    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})
    
    for li in liTags:
        comment = {}
        try:
            comment['title'] = li.find(
                'a', attrs={'class': 'j_th_tit '}).text.encode('utf-8').strip()
            comment['link'] = "http://tieba.baidu.com/" + \
                li.find('a', attrs={'class': 'j_th_tit '})['href']
            comment['name'] = li.find(
                'span', attrs={'class': 'tb_icon_author '}).text.encode('utf-8').strip()
            comment['time'] = li.find(
                'span', attrs={'class': 'pull-right is_show_create_time'}).text.encode('utf-8').strip()
            comment['replyNum'] = li.find(
                'span', attrs={'class': 'threadlist_rep_num center_text'}).text.encode('utf-8').strip()
            comments.append(comment)
        except:
            print('error')
        return comments
def Out2File(dict):
    
    with open('TTBT.txt', 'a+') as f:
        for comment in dict:
            f.write('title： {} \t link：{} \t writer：{} \t time：{} \t comments： {} \n'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))

        print('finish')
def main(base_url, deep):
    url_list = []
    
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50 * i))
    print('All Loaded。。。。')

    
    for url in url_list:
        content = get_content(url)
        Out2File(content)
    print('All Finished')


base_url = 'https://tieba.baidu.com/f?kw=2ch&ie=utf-8'

deep = 3
if __name__ == '__main__':
    main(base_url, deep)
