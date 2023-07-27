import copy
import re
import scrapy
from yamaxun.items import YamaxunItem
from scrapy_redis.spiders import RedisSpider
import numpy as np

class AmazonSpider(RedisSpider):
    name = 'amazon'
    # allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/s?srs=1546136071&bbn=1546134071&rh=n%3A1546134071&dc&qid=1651040484&ref=lp_1546136071_ex_n_1']
    redis_key = 'py21'

    def __init__(self,*args,**kwargs):
        domain = kwargs.pop('domain','')
        self.allowed_domains = list(filter(None,domain.split(',')))
        super(AmazonSpider,self).__init__(*args,**kwargs)

    def make_requests_from_url(self, url):
        # 创建临时储存文件并初始化
        dict = {'np_i':-1,'filter_result_dict':{},'filter_commodity_dict':{}}
        np.save('E:\my_file.npy', dict)

        # 初始化商品数组，存放商品字典
        item = YamaxunItem()
        item['startUrl'] = url
        # temp = 'session-id=457-8661111-8163056; ubid-acbcn=458-7313919-3569065; session-token=3RD0ohrjinQEUFIpjNXj1MZ13p0r2Y5xRsa4QgP/yEtmRvbfmmPK4XNLMteeff54pf0rQdAkSBZ818uSl0OS6fgdWEFvUX3OXSPSc0mxQiSdqR6zWNTt9ULQEIhPR64CDh3akqkp6qg9tM/f6Fj3VwslOvSH2KjO+XWv0Si3FT/AUkJo8VRMlJdT2toeSFxTVGb8v8DAGKWzq1vVkVIi4cPWq5nFON0vF378x8Eh4uSMq1UkGEYDd99tJIzYwL/6; x-acbcn="M816yCvA?eNmP90R3SAPePe?wL@ploXvwPxXUYeDsj@sP4Djl3RA0zmBKAW35JP7"; at-main=Atza|IwEBIA74ph_bCnR0vQrdzEZbfeKYSCTxsrzBLLsREXHP3ZwocCrzF-8CF1QjTDIDPNnMionKq199ec-xqd118AoOTPQrEFmCy8Yn23WV49zp6xgqjqUVFvPKw7QoY1FeEzOzppzKsAXuiwrV0vN1H1g4v4DnmYdI2zNOjg4ZdlPWaZcoJYbNTu3sud-mqxe3W5rI1jx_6Zokq7jsf1cnk5RGVg6N; sess-at-main="bdOGurp9f8Q/Ydt0t4Qch/SaJtyxmC4lC9FjgHcbUVI="; sst-main=Sst1|PQFfp167ZHYf1g9EZQkFIBFQCTLJbo2GssE00WrypApVaXjUz9zd3PobqmbNhcGkwVZ1aLXbANQtMh2wf4kV0xtoLQu-EfRA0Ilt8baAdfB7BFXF8L93Ke5RnsIdSSPz-hiUqd6x1errb-yOEAY8nBdSjKFfrIbgUU9betWpvInob73nCRZnc81G09Qck8HOvycLeMdYobHdv0oszAqhs9DFl50WK_wLlC3rXZCzjFE8fyrMNAF0bg5q5bMICtmuk4Wc9lW2QGvDUnKuOZIKLAmI_SZnlA7OiKNZA9ZQX3TQWxk; lc-acbcn=zh_CN; i18n-prefs=CNY; session-id-time=2082729601l; csm-hit=tb:Y0M74NJJZGB1GND7ZEXE+s-3GGY43HV1GPEWWKHX7MM|1654282325679&t:1654282325679&adb:adblk_no'
        # cookies = {data.split("=")[0]: data.split("=")[-1]for data in temp.split('; ')}
        return scrapy.Request(url,
                              dont_filter=True,
                              meta={'item': copy.deepcopy(item)},
                              # cookies=cookies
                              )

        # 获取一级链接数据
    def parse(self, response):
        # 判断是否登录成功
        print(response.xpath('//*[@id="nav-link-accountList-nav-line-1"]/text()').extract_first())
        item = response.meta['item']
        # 获取二级目录总链接
        node_list = response.xpath('//*[@id="departments"]/ul/li[@class="a-spacing-micro"]')
        # 判断二级目录为空则进行一级目录爬取，不为空则爬取商品
        if len(node_list) != 0:
            classification_node_list = response.xpath('//*[@class="a-spacing-micro"]')
            for classification_node in classification_node_list:
                item['big_classification_text'] = classification_node.xpath('./span/a/span/text()')[0].extract().strip()
                patter = re.compile("&qid=\d+")
                big_classification_link = patter.sub("",response.urljoin(classification_node.xpath('./span/a/@href')[0].extract()))
                item['big_classification_link'] = big_classification_link
                yield scrapy.Request(
                    url=item['big_classification_link'],
                    callback=self.get_pages,
                    meta={'item': copy.deepcopy(item)},
                    dont_filter=True
                )
        else:
            # 批量翻页（在获取商品详情信息时行不通）
            # 判断翻页
            #获取页数控件，根据有没有控件来确定请求链接数
            sum_pages = response.xpath('//*[@class="s-pagination-strip"]/span[last()]/text()')
            # 没有页数，只有一页则直接请求一页
            if len(sum_pages) == 0:
                patter = re.compile("qid=\d+")
                page_link = patter.sub("", item['startUrl'])
                item['page_link'] = page_link
                yield scrapy.Request(
                    url=item['page_link'],
                    callback=self.get_commodity_link,
                    meta={'item': copy.deepcopy(item)},
                    dont_filter=True
                )
            else:
                # 有页数，有页数则构建多页请求
                sum_page = response.xpath('//*[@class="s-pagination-strip"]/span[last()]/text()')[0].extract()
                # 页数组件没有缩减影藏
                if sum_page == '1':
                    sum_pages = response.xpath('//*[@class="s-pagination-strip"]/a[last()-1]/text()')[0].extract()
                    for page in range(1, int(sum_pages) + 1):
                        patter = re.compile("qid=\d+")
                        page_link = patter.sub("", item['startUrl'])
                        item['page_link'] = page_link + '&page=' + str(page)
                        print(item['page_link'])
                        # 构造商品页数链接，批量发起请求
                        yield scrapy.Request(
                            url=item['page_link'],
                            callback=self.get_commodity_link,
                            meta={'item': copy.deepcopy(item)},
                            dont_filter=True
                        )
                else:
                    # 页数组件有缩减影藏
                    sum_pages = response.xpath('//*[@class="s-pagination-strip"]/span[last()]/text()')[0].extract()
                    for page in range(1, int(sum_pages) + 1):
                        patter = re.compile("qid=\d+")
                        page_link = patter.sub("", item['startUrl'])
                        item['page_link'] = page_link + '&page=' + str(page)
                        print(item['page_link'])
                        # 构造商品页数链接，批量发起请求
                        yield scrapy.Request(
                            url=item['page_link'],
                            callback=self.get_commodity_link,
                            meta={'item': copy.deepcopy(item)},
                            dont_filter=True
                        )



    # 翻页操作
    def get_pages(self, response):
        # 判断是否登录成功
        print(response.xpath('//*[@id="nav-link-accountList-nav-line-1"]/text()').extract_first())
        item = response.meta['item']
        # 批量翻页（在获取商品详情信息时行不通）
        # 判断翻页
        # 获取页数控件，根据有没有控件来确定请求链接数
        sum_pages = response.xpath('//*[@class="s-pagination-strip"]/span[last()]/text()')
        # 没有页数，只有一页则直接请求一页
        if len(sum_pages) == 0:
            patter = re.compile("qid=\d+")
            page_link = patter.sub("", item['startUrl'])
            item['page_link'] = page_link
            yield scrapy.Request(
                url=item['page_link'],
                callback=self.get_commodity_link,
                meta={'item': copy.deepcopy(item)},
                dont_filter=True
            )
        else:
            # 有页数，有页数则构建多页请求
            sum_page = response.xpath('//*[@class="s-pagination-strip"]/span[last()]/text()')[0].extract()
            # 页数组件没有缩减影藏
            if sum_page == '1':
                sum_pages = response.xpath('//*[@class="s-pagination-strip"]/a[last()-1]/text()')[0].extract()
                for page in range(1, int(sum_pages) + 1):
                    patter = re.compile("qid=\d+")
                    page_link = patter.sub("", item['startUrl'])
                    item['page_link'] = page_link + '&page=' + str(page)
                    print(item['page_link'])
                    # 构造商品页数链接，批量发起请求
                    yield scrapy.Request(
                        url=item['page_link'],
                        callback=self.get_commodity_link,
                        meta={'item': copy.deepcopy(item)},
                        dont_filter=True
                    )
            else:
                # 页数组件有缩减影藏
                sum_pages = response.xpath('//*[@class="s-pagination-strip"]/span[last()]/text()')[0].extract()
                for page in range(1, int(sum_pages) + 1):
                    patter = re.compile("qid=\d+")
                    page_link = patter.sub("", item['startUrl'])
                    item['page_link'] = page_link + '&page=' + str(page)
                    print(item['page_link'])
                    # 构造商品页数链接，批量发起请求
                    yield scrapy.Request(
                        url=item['page_link'],
                        callback=self.get_commodity_link,
                        meta={'item': copy.deepcopy(item)},
                        dont_filter=True
                    )


    # 获取每个商品链接
    def get_commodity_link(self, response):
        # 判断是否登录成功
        print(response.xpath('//*[@id="nav-link-accountList-nav-line-1"]/text()').extract_first())
        item = response.meta['item']
        commodity_node_list = response.xpath('//*[@class="s-main-slot s-result-list s-search-results sg-row"]//h2')
        for commodity_node in commodity_node_list:
            patter = re.compile("qid=\d+")
            commodity_link = patter.sub("", response.urljoin(commodity_node.xpath('./a/@href')[0].extract()))
            item['commodity_link'] = commodity_link
            print(item['commodity_link'])
            yield scrapy.Request(
                url=item['commodity_link'],
                callback=self.getSkulink,
                meta={'item': copy.deepcopy(item)},
                dont_filter=True
            )


    # 获取sku链接
    def getSkulink(self, response):
        load_dict = np.load('E:\my_file.npy', allow_pickle=True).item()
        filter_result_dict = load_dict['filter_result_dict']
        filter_commodity_dict = load_dict['filter_commodity_dict']
        np_i = load_dict['np_i']
        np_i += 1
        filter_result_dict[np_i] = []
        filter_commodity_dict[np_i] = []
        # 实时保存
        new_dict = {'np_i':np_i,'filter_result_dict':filter_result_dict,'filter_commodity_dict':filter_commodity_dict}
        np.save('E:\my_file.npy', new_dict)
        print(np_i)
        # 判断不同sku列表参数
        judge_skuList_type = ''

        item = response.meta['item']

        # 不同的sku列表格式不同
        judge_nodes=response.xpath('//*[@id="twister"]')
        judge_nodes2 = response.xpath('//*[@id="twister-plus-inline-twister"]')
        # 根据不同的sku列表进行不同操作
        # 第一种sku列表
        if len(judge_nodes) != 0:

            judge_nodes = response.xpath('//*[@id="twister"]//li')
            # 有些有列表但是没有li,判断是否有li
            # 有li构建请求链接
            if len(judge_nodes) != 0:
                # 带有选择下拉框sku列表
                select_nodes = response.xpath('//*[@id="twister"]//select')
                # 如果有选择下拉框sku列表
                if len(select_nodes) != 0:
                    print('66666666666')
                    judge_skuList_type = 'judge_nodes6'
                    select_nodes2=response.xpath('//*[@id="twister"]//select/option')
                    # 存放select_skuLink和li_skuLink所有链接的列表，最后再一起发送请求
                    select_list = []
                    for select_skuLink in select_nodes2:
                        select_value = select_skuLink.xpath('./@value').extract_first()
                        if select_value!='-1':
                            patter = re.compile("\S+,")
                            newselect_value = patter.sub("",select_value)
                            newselect_skuLink = "https://www.amazon.cn/dp/"+newselect_value+"?th=1&psc=1"
                            select_list.append(newselect_skuLink)
                    sku_nodes = response.xpath('//*[@id="twister"]//li')
                    for skuLink in sku_nodes:
                        # 匹配sku链接正则,修改链接
                        patter = re.compile("ref=\S+")
                        newskuLink= patter.sub("", response.urljoin(skuLink.xpath('./@data-dp-url').extract_first()))
                        select_list.append(newskuLink)
                    for select_list_sku in select_list:
                        yield scrapy.Request(
                            url=select_list_sku,
                            callback=self.filter_Skulink,
                            meta={'item': copy.deepcopy(item),
                                  'judge_skuList_type': judge_skuList_type,
                                  'np_i': copy.deepcopy(np_i)},
                            dont_filter=True
                        )


                else:
                    # 没有选择下拉框sku列表则按照正长li爬取
                    judge_skuList_type = 'judge_nodes1'
                    print('111111111')
                    sku_nodes = response.xpath('//*[@id="twister"]//li')
                    for skuLink in sku_nodes:
                        # 匹配sku链接正则,修改链接
                        patter = re.compile("ref=\S+")
                        newskuLink= patter.sub("", response.urljoin(skuLink.xpath('./@data-dp-url').extract_first()))
                        yield scrapy.Request(
                            url=newskuLink,
                            callback=self.filter_Skulink,
                            meta={'item': copy.deepcopy(item),
                                  'judge_skuList_type': judge_skuList_type,
                                  'np_i': copy.deepcopy(np_i)},
                            dont_filter=True
                        )
            # 没有li直接爬取数据
            else:
                judge_skuList_type = 'judge_nodes5'
                print('5555555')
                yield scrapy.Request(
                    url=item['commodity_link'],
                    callback=self.filter_Skulink,
                    meta={'item': copy.deepcopy(item),
                          'judge_skuList_type': judge_skuList_type,
                          'np_i': copy.deepcopy(np_i)},
                    dont_filter=True
                )
        # 第二种sku列表
        elif len(judge_nodes2) != 0:
            judge_skuList_type = 'judge_nodes2'
            judge_nodes = response.xpath('//*[@id="twister-plus-inline-twister"]//li')
            # 有些有列表但是没有li,判断是否有li
            # 有li构建请求链接
            if len(judge_nodes) != 0:
                print('222222222')
                sku_nodes = response.xpath('//*[@id="twister-plus-inline-twister"]//li')
                for skuLink in sku_nodes:
                    # 有多余的没有编码的li
                    skuLink2 = skuLink.xpath('./@data-asin')
                    # 去除多余的没有编码的li
                    if len(skuLink2) != 0:
                        newskuLink = "https://www.amazon.cn/dp/"+skuLink2.extract_first()+"?th=1&psc=1"
                        yield scrapy.Request(
                            url=newskuLink,
                            callback=self.filter_Skulink,
                            meta={'item': copy.deepcopy(item),
                                  'judge_skuList_type': judge_skuList_type,
                                  'np_i': copy.deepcopy(np_i)},
                            dont_filter=True
                        )
            # 没有li直接爬取数据
            else:
                judge_skuList_type = 'judge_nodes3'
                print('333333333')
                yield scrapy.Request(
                    url=item['commodity_link'],
                    callback=self.filter_Skulink,
                    meta={'item': copy.deepcopy(item),
                          'judge_skuList_type': judge_skuList_type,
                          'np_i': copy.deepcopy(np_i)},
                    dont_filter=True
                )
        # 没有sku列表直接爬取数据
        else:
            judge_skuList_type = 'judge_nodes4'
            print('44444444')
            yield scrapy.Request(
                url=item['commodity_link'],
                callback=self.filter_Skulink,
                meta={'item': copy.deepcopy(item),
                      'judge_skuList_type': judge_skuList_type,
                      'np_i': copy.deepcopy(np_i)},
                dont_filter=True
            )

    # 过滤重复url
    def filter_Skulink(self, response):
        np_i = response.meta['np_i']
        item = response.meta['item']
        judge_skuList_type = response.meta['judge_skuList_type']

        # # 读取保存sku数据列表（用来存储sku数据）
        load_dict = np.load('E:\my_file.npy', allow_pickle=True).item()
        np_filter_result_dict = load_dict['filter_result_dict'][np_i]


        # 根据不同的sku列表进行不同操作
        if judge_skuList_type == 'judge_nodes1':
            print(judge_skuList_type)
            # 定义去重后数组
            sku_nodes2 = response.xpath('//*[@id="twister"]//li')
            for skuLink2 in sku_nodes2:
                patter = re.compile("ref=\S+")
                newskuLink2 = patter.sub("", response.urljoin(skuLink2.xpath('./@data-dp-url').extract_first()))
                # 如果链接在去重数组中存在，则不添加，不存在则添加,(为了得到去重后的数量数组，可以在后面getskudata时进行判断什么时候提交数据)
                if newskuLink2 not in np_filter_result_dict:
                    # 把不重复的链接存入数组
                    np_filter_result_dict.append(newskuLink2)
                    # 实时保存sku数据列表（不保存会为空）
                    np.save('E:\my_file.npy', load_dict)
                    yield scrapy.Request(
                        url=newskuLink2,
                        callback=self.get_commodity_data,
                        meta={'item': copy.deepcopy(item),
                              'judge_skuList_type': copy.deepcopy(judge_skuList_type),
                              'np_i': copy.deepcopy(np_i)},
                        dont_filter=False,
                    )
        elif judge_skuList_type == 'judge_nodes2':
            sku_nodes = response.xpath('//*[@id="twister-plus-inline-twister"]//li')
            for skuLink in sku_nodes:
                # 有多余的没有编码的li
                skuLink2 = skuLink.xpath('./@data-asin')
                # 去除多余的没有编码的li
                if len(skuLink2) != 0:
                    newskuLink = "https://www.amazon.cn/dp/" + skuLink2.extract_first() + "?th=1&psc=1"
                    if newskuLink not in np_filter_result_dict:
                        # 把不重复的链接存入数组
                        np_filter_result_dict.append(newskuLink)
                        # 实时保存sku数据列表（不保存会为空）
                        np.save('E:\my_file.npy', load_dict)
                        yield scrapy.Request(
                            url=newskuLink,
                            callback=self.get_commodity_data,
                            meta={'item': copy.deepcopy(item),
                                  'judge_skuList_type': copy.deepcopy(judge_skuList_type),
                                  'np_i': copy.deepcopy(np_i)},
                            dont_filter=False,
                        )

        elif judge_skuList_type == 'judge_nodes3':
            # 因为3和2提取数据方式一样，所以3重定向到2
            judge_skuList_type = 'judge_nodes2'
            print(judge_skuList_type)
            # 把不重复的链接存入数组（这里其实不用，为了统一后面操作）
            np_filter_result_dict.append(item['commodity_link'])
            # 实时保存sku数据列表（不保存会为空）
            np.save('E:\my_file.npy', load_dict)
            yield scrapy.Request(
                url=item['commodity_link'],
                callback=self.get_commodity_data,
                meta={'item': copy.deepcopy(item),
                      'judge_skuList_type': copy.deepcopy(judge_skuList_type),
                      'np_i': copy.deepcopy(np_i)},
                dont_filter=False
            )
        elif judge_skuList_type == 'judge_nodes5':
            # 因为5和1提取数据方式一样，所以5重定向到1
            judge_skuList_type = 'judge_nodes1'
            print(judge_skuList_type)
            # 把不重复的链接存入数组（这里其实不用，为了统一后面操作）
            np_filter_result_dict.append(item['commodity_link'])
            # 实时保存sku数据列表（不保存会为空）
            np.save('E:\my_file.npy', load_dict)
            yield scrapy.Request(
                url=item['commodity_link'],
                callback=self.get_commodity_data,
                meta={'item': copy.deepcopy(item),
                      'judge_skuList_type': copy.deepcopy(judge_skuList_type),
                      'np_i': copy.deepcopy(np_i)},
                dont_filter=False
            )
        elif judge_skuList_type == 'judge_nodes4':
            print(judge_skuList_type)
            # 把不重复的链接存入数组（这里其实不用，为了统一后面操作）
            np_filter_result_dict.append(item['commodity_link'])
            # 实时保存sku数据列表（不保存会为空）
            np.save('E:\my_file.npy', load_dict)
            yield scrapy.Request(
                url=item['commodity_link'],
                callback=self.get_commodity_data,
                meta={'item': copy.deepcopy(item),
                      'judge_skuList_type': copy.deepcopy(judge_skuList_type),
                      'np_i': copy.deepcopy(np_i)},
                dont_filter=False
            )
        elif judge_skuList_type == 'judge_nodes6':
            # 因为6和1提取数据方式一样，所以6重定向到1
            print(judge_skuList_type)
            select_nodes2 = response.xpath('//*[@id="twister"]//select/option')
            # 存放select_skuLink和li_skuLink所有链接的列表，最后再一起发送请求
            select_list = []
            for select_skuLink in select_nodes2:
                select_value = select_skuLink.xpath('./@value').extract_first()
                if select_value != '-1':
                    patter = re.compile("\S+,")
                    newselect_value = patter.sub("", select_value)
                    newselect_skuLink = "https://www.amazon.cn/dp/" + newselect_value + "?th=1&psc=1"
                    select_list.append(newselect_skuLink)
            sku_nodes = response.xpath('//*[@id="twister"]//li')
            for skuLink in sku_nodes:
                # 匹配sku链接正则,修改链接
                patter = re.compile("ref=\S+")
                newskuLink = patter.sub("", response.urljoin(skuLink.xpath('./@data-dp-url').extract_first()))
                select_list.append(newskuLink)
            for select_list_sku in select_list:
                # 如果链接在去重数组中存在，则不添加，不存在则添加,(为了得到去重后的数量数组，可以在后面getskudata时进行判断什么时候提交数据)
                if select_list_sku not in np_filter_result_dict:
                    # 把不重复的链接存入数组
                    np_filter_result_dict.append(select_list_sku)
                    # 实时保存sku数据列表（不保存会为空）
                    np.save('E:\my_file.npy', load_dict)
                    yield scrapy.Request(
                        url=select_list_sku,
                        callback=self.get_commodity_data,
                        meta={'item': copy.deepcopy(item),
                              'judge_skuList_type': copy.deepcopy(judge_skuList_type),
                              'np_i': copy.deepcopy(np_i)},
                        dont_filter=False
                    )

    # 获取商品数据
    def get_commodity_data(self, response):
        # 判断是否登录成功
        print(response.xpath('//*[@id="nav-link-accountList-nav-line-1"]/text()').extract_first())

        np_i = response.meta['np_i']
        # 读取sku数据列表和存储商品数据列表，通过两者对比，相等就提交数据到数据库
        load_dict = np.load('E:\my_file.npy',allow_pickle=True).item()
        filter_result_dict = load_dict['filter_result_dict']
        np_filter_result_dict = filter_result_dict[np_i]
        filter_commodity_dict = load_dict['filter_commodity_dict']
        np_filter_commodity_dict = filter_commodity_dict[np_i]


        item = response.meta['item']
        judge_skuList_type = response.meta['judge_skuList_type']
        # getSku_data存放整体数据字典
        commodity_data_dict = {}
        # 图片列表
        commodityImage_link_list = []

        # sku_link链接
        commodity_data_dict['sku_link'] = response.url

        # 根据不同的sku列表进行不同操作
        if judge_skuList_type == 'judge_nodes1':
            # sku_属性：值
            sku_classification = response.xpath('//*[@id="twister"]/div/div')
            for sku_type_classification in sku_classification:
                sku_type = sku_type_classification.xpath('.//label/text()').extract_first().strip()
                sku_value = sku_type_classification.xpath('.//span/text()').extract_first().strip()
                commodity_data_dict[sku_type] = sku_value

        elif judge_skuList_type == 'judge_nodes2':
            # sku_属性：值
            sku_classification = response.xpath('//*[@id="twister-plus-inline-twister"]/div')
            for sku_type_classification in sku_classification:
                classification = sku_type_classification.xpath('./span/div/div/div/span[1]/text()')
                if len(classification) != 0:
                    sku_type = sku_type_classification.xpath('./span/div/div/div/span[1]/text()').extract_first().strip()
                    sku_value = sku_type_classification.xpath('./span/div/div/div/span[2]/text()').extract_first().strip()
                    commodity_data_dict[sku_type] = sku_value
                else:
                    sku_type = sku_type_classification.xpath('./span[1]/text()').extract_first().strip()
                    sku_value = sku_type_classification.xpath('./span[2]/text()').extract_first().strip()
                    commodity_data_dict[sku_type] = sku_value
        # 因为judge_nodes3的处理方式和judge_nodes2一致，所以在这里不用考虑judge_nodes3
        elif judge_skuList_type == 'judge_nodes4':
            commodity_data_dict['sku_type'] = '无sku，只有一个'

        elif judge_skuList_type == 'judge_nodes6':
            # sku_属性：值
            sku_classification = response.xpath('//*[@id="twister"]/div')
            for sku_type_classification in sku_classification:
                sku1_classification = sku_type_classification.xpath('.//select')
                sku2_classification = sku_type_classification.xpath('./ul')
                if len(sku1_classification)!=0:
                    sku_type = sku_type_classification.xpath('./div[2]/label/text()').extract_first().strip()
                    sku_value = sku_type_classification.xpath('.//option[@class="dropdownSelect"]/text()').extract_first()
                    commodity_data_dict[sku_type] = sku_value
                elif len(sku2_classification)!=0:
                    sku_type = sku_type_classification.xpath('./div/label/text()').extract_first().strip()
                    sku_value = sku_type_classification.xpath('./div/span/text()').extract_first().strip()
                    commodity_data_dict[sku_type] = sku_value





        # 商品名
        commodity_data_dict['commodity_name'] = response.xpath('//*[@id="productTitle"]/text()')[0].extract().strip()
        if len(response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[1]/text()')) != 0:
            # 商品价格
            # 把¥字符替换成空
            commodity_price = re.sub('¥', "", response.xpath(
                '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[1]/text()')[0].extract().strip())
            commodity_data_dict['commodity_price'] = commodity_price
        elif len(response.xpath('//*[@id="corePrice_desktop"]/div/table/tr[1]/td[2]/span[1]/span[1]/text()')) != 0:
            # 商品价格
            # 把¥字符替换成空
            commodity_price = re.sub('¥', "", response.xpath(
                '//*[@id="corePrice_desktop"]/div/table/tr[1]/td[2]/span[1]/span[1]/text()')[0].extract().strip())
            commodity_data_dict['commodity_price'] = commodity_price
        else:
            commodity_data_dict['commodity_price'] = '商品目前无货'

        #商品图片
        image_classification = response.xpath('//*[@id="altImages"]/ul/li[@class="a-spacing-small item"]')
        for image_link_classification in image_classification:
            image_link = re.sub("._AC_US40_","",image_link_classification.xpath('.//img/@src').extract_first())
            commodityImage_link_list.append(image_link)
        commodity_data_dict['commodityImage_link'] = commodityImage_link_list

        # 把商品数据统一添加到商品数组
        np_filter_commodity_dict.append(commodity_data_dict)
        # 实时保存存储商品数据列表（不保存会为空）
        np.save('E:\my_file.npy', load_dict)
        print(str(np_i) + '\n' + str(len(np_filter_result_dict))+ '\n' + str(len(np_filter_commodity_dict)))

        # 根据商品数据数组大小和去重的sku数据数组大小是否相等来判断提交数据
        if len(np_filter_commodity_dict) == len(np_filter_result_dict):
            item['commodity_data'] = np_filter_commodity_dict
            yield item













    # # 获取每个商品数据
    # def get_commodity_data(self, response):
    #     print(response.xpath('//*[@id="nav-link-accountList-nav-line-1"]/text()').extract_first())
    #     item = response.meta['item']
    #     # 获取sku参数列表xpath
    #     print(str(len(response.xpath('//*[@id="twister"]'))))
    #
    #     # 如果没有sku参数列表，则直接爬取数据
    #     if len(response.xpath('//*[@id="twister"]')) == 0:
    #         item['commodity_name'] = response.xpath('//*[@id="productTitle"]/text()')[0].extract().strip()
    #         if len(response.xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[1]/text()')) != 0:
    #             # 把¥字符替换成空
    #             commodity_price = re.sub('¥', "", response.xpath(
    #                 '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span/span[1]/text()')[0].extract().strip())
    #             item['commodity_price'] = commodity_price
    #         else:
    #             # 把¥字符替换成空
    #             commodity_price = re.sub('¥', "", response.xpath(
    #                 '//*[@id="corePrice_desktop"]/div/table/tr[1]/td[2]/span[1]/span[1]/text()')[0].extract().strip())
    #             item['commodity_price'] = commodity_price
    #
    #         # item['commodity_Imge_link'] = response.xpath('//*[@class="a-spacing-small item imageThumbnail a-declarative"]//img/@src')[0].extract()
    #         yield item
    #
    #     # 如果有sku参数列表，则构建每一个sku链接
    #     # else:

































    #逐级链接爬取 批量翻页
    # def make_requests_from_url(self, url):
    #     # 存放数据
    #     item = {}
    #     # 数据名字标识
    #     i = 0
    #     return scrapy.Request(url,
    #                           dont_filter=False,
    #                           meta={'item1': item,"i":i},
    #                           )
    #
    #
    #
    #
    #
    # # 处理链接数据
    # def parse(self, response):
    #     item = response.meta['item1']
    #     i = response.meta['i']
    #
    #     # 判断目录
    #     # 根据最后一个目录有没有链接来判断是不是最后一级目录
    #     last_classification = response.xpath('//*[@id="departments"]/ul/li[last()]/span/a')
    #
    #     # 目录到底则爬取对应商品数据
    #     if len(last_classification) == 0:
    #         # 判断翻页
    #         #获取页数控件，根据有没有控件来确定请求链接数
    #         sum_pages = response.xpath('//*[@class="s-pagination-strip"]/span[last()]/text()')
    #         # 没有页数，只有一页则直接请求一页
    #         if len(sum_pages) == 0:
    #             yield scrapy.Request(
    #                 # url="https://www.amazon.cn/s?i=toys&srs=1546136071&bbn=1546134071&dc&page="+str(page)+"&qid=1651988262&ref=sr_pg_23",
    #                 url=item['big_classification_link' + str(i - 1)] + '&page=1',
    #                 callback=self.get_commodity_data,
    #                 meta={'item1': copy.deepcopy(item)},
    #                 dont_filter=False
    #             )
    #         else:
    #             # 有页数，有页数则构建多页请求
    #             sum_pages = response.xpath('//*[@class="s-pagination-strip"]/span[last()]/text()')[0].extract()
    #             print("1111111111111111111111111111111111111111111111111" + str(sum_pages))
    #             for page in range(1, int(sum_pages) + 1):
    #                 print("1111111111111111111111" + item['big_classification_link' + str(i - 1)] + '&page=' + str(page))
    #                 # 构造商品页数链接，批量发起请求
    #                 yield scrapy.Request(
    #                     # url="https://www.amazon.cn/s?i=toys&srs=1546136071&bbn=1546134071&dc&page="+str(page)+"&qid=1651988262&ref=sr_pg_23",
    #                     url=item['big_classification_link' + str(i - 1)] + '&page=' + str(page),
    #                     callback=self.get_commodity_data,
    #                     meta={'item1': copy.deepcopy(item)},
    #                     dont_filter=False
    #                 )
    #
    #
    #     # 目录没到底则继续请求下一目录
    #     else:
    #         # 获取二级目录总链接
    #         node_list = response.xpath('//*[@class="a-spacing-micro s-navigation-indent-2"]')
    #
    #         # 判断二级目录为空则进行一级目录爬取，不为空则进行二级目录爬取，防止二级目录中存在一级目录而导致重复爬取
    #         if len(node_list) == 0:
    #             # 一级
    #             classification_node_list = response.xpath('//*[@class="a-spacing-micro"]')
    #         else:
    #             # 二级
    #             classification_node_list = response.xpath('//*[@class="a-spacing-micro s-navigation-indent-2"]')
    #
    #         for classification_node in classification_node_list:
    #             item['big_classification_text'+str(i)] = classification_node.xpath('./span/a/span/text()')[0].extract().strip()
    #             item['big_classification_link'+str(i)] = response.urljoin(classification_node.xpath('./span/a/@href')[0].extract())
    #             yield scrapy.Request(
    #                 url=item['big_classification_link'+str(i)],
    #                 callback=self.parse,
    #                 meta={'item1': copy.deepcopy(item),"i":i+1},
    #                 dont_filter = False
    #             )
    #
    #
    # # 处理商品数据
    # # 没有目录了则抓取商品数据
    # def get_commodity_data(self, response):
    #     print("ccccccccccccccccccccccccccccccccccccccccccccc", response.request.headers['User-Agent'])
    #     item = response.meta['item1']
    #     commodity_node_list = response.xpath('//*[@class="s-main-slot s-result-list s-search-results sg-row"]/div[@class="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"]')
    #     for commodity_node in commodity_node_list:
    #         item['commodity_link'] = response.urljoin(commodity_node.xpath('.//h2/a/@href')[0].extract())
    #         yield item

















#逐级链接爬取 一页一页翻
# #一级目录
#     def parse(self, response):
#         item = response.meta['item1']
#         i =response.meta['i']
#
#         classification_node_list=response.xpath('//*[@id="departments"]/ul/li/span/a')
#
#
#         if len(classification_node_list) == 0:
#             commodity_node_list = response.xpath('//*[@class="s-main-slot s-result-list s-search-results sg-row"]/div[@class="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"]')
#             for commodity_node in commodity_node_list:
#                 item['commodity_link'] = response.urljoin(commodity_node.xpath('.//h2/a/@href')[0].extract())
#                 yield item
#
#             # 翻页
#             # 判断是否是最后一页的依据
#             aa = response.xpath('//*[@class="s-pagination-strip"]/a[last()]/@class').extract_first()
#             # 翻页请求链接
#             part_url = response.xpath('//*[@class="s-pagination-strip"]/a[last()]/@href').extract_first()
#             # 判断是否是最后一页
#             if aa != 's-pagination-item s-pagination-button':
#                 print("1111111111111111111111111111111111111111111111111111111111111111111111111下一页")
#                 next_url = response.urljoin(part_url)
#                 yield scrapy.Request(
#                     url=next_url,
#                     callback=self.get_commodity_data,
#                     meta={'item1': copy.deepcopy(item)}
#                 )
#
#         for classification_node in classification_node_list:
#             item['big_classification_text'+str(i)] = classification_node.xpath('./span/text()')[0].extract().strip()
#             item['big_classification_link'+str(i)] = response.urljoin(classification_node.xpath('./@href')[0].extract())
#             yield scrapy.Request(
#                 url=item['big_classification_link'+str(i)],
#                 callback=self.parse,
#                 meta={'item1': copy.deepcopy(item),"i":i+1}
#             )
#
#
#     # 没有目录了则抓取商品数据
#     def get_commodity_data(self, response):
#         print("ccccccccccccccccccccccccccccccccccccccccccccc", response.request.headers['User-Agent'])
#         item = response.meta['item1']
#         commodity_node_list = response.xpath('//*[@class="s-main-slot s-result-list s-search-results sg-row"]/div[@class="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"]')
#         for commodity_node in commodity_node_list:
#             item['commodity_link'] = response.urljoin(commodity_node.xpath('.//h2/a/@href')[0].extract())
#             yield item
#         # 判断是否是最后一页的依据
#         aa=response.xpath('//*[@class="s-pagination-strip"]/a[last()]/@class').extract_first()
#         # 翻页请求链接
#         part_url = response.xpath('//*[@class="s-pagination-strip"]/a[last()]/@href').extract_first()
#         # 判断是否是最后一页
#         if aa != 's-pagination-item s-pagination-button':
#             next_url = response.urljoin(part_url)
#             yield scrapy.Request(
#                 url=next_url,
#                 callback=self.get_commodity_data,
#                 meta={'item1': copy.deepcopy(item)}
#             )
