#!/usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import re
import xlrd
import xlwt
import time
from bs4 import BeautifulSoup
import ConfigParser
import threading
import urllib

urlfile = xlwt.Workbook()
table = urlfile.add_sheet(u"信息", cell_overwrite_ok=True)
table.write(0, 0, u"名字")
table.write(0, 1, u"链接")

serailfile = xlwt.Workbook()
wtable = serailfile.add_sheet(u"信息", cell_overwrite_ok=True)
wtable.write(0, 0, u"名字")
wtable.write(0, 1, u"链接")
wtable.write(0, 2, u"车牌号")

user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27"
headers = {"User-Agent": user_agent}
headers2 = {
    'Accept': 'text/css,*/*;q=0.1',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': user_agent,
}


class GetFuli():
    def __init__(self, page):
        self.page = page

    def get_url(self):
        for p in range(1, self.page + 1):
            url = "https://javpee.com/cn/actresses"
            rq = requests.get(url, headers=headers)
            html = rq.text
            # print html.encode("utf-8")

            soup = BeautifulSoup(html, "lxml")
            i = (p - 1) * 50 + 1
            for tag in soup.find_all(href=re.compile("https://javpee.com/cn/star")):
                table.write(i, 1, tag.attrs["href"])
                i += 1
            j = (p - 1) * 50 + 1
            for tag in soup.find_all(class_="photo-info"):
                for gg in tag.find_all('span'):
                    # print gg.string
                    table.write(j, 0, gg.string)
                    j += 1
            print u"完成读取第{}页信息".format(p)

    def get_serial(self, name):
        data = xlrd.open_workbook(name)
        tb = data.sheets()[0]
        nrows = tb.nrows

        for j in range(nrows):
            try:
                cf = ConfigParser.ConfigParser()
                cf.read("liao.ini")
                p = cf.getint("num", "p")
                if j == 0:
                    continue
                else:
                    url = tb.cell(j, 1).value

                    rq = requests.get(url, headers=headers)
                    html = rq.text
                    soup = BeautifulSoup(html, "lxml")

                    i = 0
                    for tag in soup.find_all('date'):
                        if i % 2 == 0:
                            wtable.write(p, 2, tag.string)
                            wtable.write(p, 0, tb.cell(j, 0).value)
                            wtable.write(p, 1, tb.cell(j, 1).value)
                            p += 1
                        i += 1
                    print j
                    cf.set("num", "p", p)
                    cf.write(open("liao.ini", "w"))
            except:
                filename = str(time.strftime('%Y%m%d%H%M%S',
                                             time.localtime())) + "serial.xlsx"
                serailfile.save(filename)
                print u"出现异常自动保存%s的车牌号备份" % time.strftime('%Y%m%d%H%M%S',
                                                         time.localtime())

    def get_link(self, conf, excel):
        myfile = xlwt.Workbook()
        mtable = myfile.add_sheet(u"信息", cell_overwrite_ok=True)
        mtable.write(0, 0, u"名字")
        mtable.write(0, 1, u"车牌号")
        mtable.write(0, 2, u"文件大小")
        mtable.write(0, 3, u"文件更新日期")
        mtable.write(0, 4, u"链接")
        mtable.write(0, 5, u"磁力链接")

        data = xlrd.open_workbook(excel)
        tb = data.sheets()[0]
        nrows = tb.nrows

        for j in range(nrows):
            try:
                cf = ConfigParser.ConfigParser()
                cf.read(conf)

                p = cf.getint("num", 'p')
                if j == 0:
                    continue
                else:
                    serail = tb.cell(j, 2).value
                    url = "https://javpee.com/cn/search/" + serail

                    rq = requests.get(url, headers=headers2, timeout=30)
                    import pdb
                    pdb.set_trace()
                    # rq.encoding = "utf-8"
                    html = rq.text
                    print html.encode("utf-8")
                    soup = BeautifulSoup(html, "lxml")

                    for tag in soup.find_all('div', class_="row"):
                        for gg in tag.find_all(
                                class_='col-sm-2 col-lg-1 hidden-xs text-right size'):
                            print gg.string
                            mtable.write(p, 0, tb.cell(j, 0).value)
                            mtable.write(p, 1, tb.cell(j, 2).value)
                            mtable.write(p, 2, gg.string)

                        for aa in tag.find_all(
                                class_='col-sm-2 col-lg-2 hidden-xs text-right date'):
                            print aa.string
                            mtable.write(p, 3, aa.string)

                        for xx in tag.find_all(href=re.compile(
                                "https://javpee.com/cn/magnet/detail/hash")):
                            print xx.attrs['href']
                            mtable.write(p, 4, xx.attrs['href'])
                            r1 = requests.get(xx.attrs['href'], headers=headers,
                                              timeout=30)
                            html1 = r1.text
                            # print html1
                            soup1 = BeautifulSoup(html1)
                            for tag1 in soup1.find_all('textarea',
                                                       id='magnetLink'):
                                print tag1.string
                                mtable.write(p, 5, tag1.string)
                            p += 1
                    cf.set("num", "p", p)
                    cf.write(open(conf, "w"))
            except Exception as err:
                print str(err)
                return
                # filename = str(time.strftime('%Y%m%d%H%M%S',
                #                              time.localtime())) + "link.xls"
                # myfile.save(filename)
                # print u"出现异常自动保存%s的磁力链接备份" % time.strftime('%Y%m%d%H%M%S',
                #                                            time.localtime())
        filename = str(
            time.strftime('%Y%m%d%H%M%S', time.localtime())) + "link.xls"
        myfile.save(filename)
        print u"自动保存%s的磁力链接备份" % time.strftime('%Y%m%d%H%M%S', time.localtime())


if __name__ == '__main__':
    test = GetFuli(1)
    # test.get_url()
    # filename = str(time.strftime('%Y%m%d%H%M%S', time.localtime())) + "url.xls"
    # urlfile.save(filename)
    # print u"完成{}的url备份".format(time.strftime('%Y%m%d%H%M%S', time.localtime()))
    #
    # test.get_serial(filename)
    # filename = str(time.strftime('%Y%m%d%H%M%S',
    #                              time.localtime())) + "serial.xls"
    # serailfile.save(filename)
    # print u"完成%s的车牌号备份" % time.strftime('%Y%m%d%H%M%S', time.localtime())

    test.get_link("liao.ini", "20180110175221serial.xls")
    print u"福利完成"

    # threads = []
    #
    # t1 = threading.Thread(target=test.get_link,
    #                       args=('liao.ini', filename,))
    # threads.append(t1)
    # t2 = threading.Thread(target=test.get_link,
    #                       args=('link2.ini', 'serial2.xls',))
    # threads.append(t2)
    # t3 = threading.Thread(target=test.get_link,
    #                       args=('link3.ini', 'serial3.xls',))
    # threads.append(t3)
    # t4 = threading.Thread(target=test.get_link,
    #                       args=('link4.ini', 'serial4.xls',))
    # threads.append(t4)
    # t5 = threading.Thread(target=test.get_link,
    #                       args=('link5.ini', 'serial5.xls',))
    # threads.append(t5)
    # t6 = threading.Thread(target=test.get_link,
    #                       args=('link6.ini', 'serial6.xls',))
    # threads.append(t6)
    #
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    #     t.join()
    # print u"完成所有进程"


