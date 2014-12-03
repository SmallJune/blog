#coding:utf-8
class LovePaginator:
    '''
    @zhangfeng
    @param url <str>:链接地址,  total_count <int>: 总数, page_size <int>: 每页显示数, cur_page <int>: 当前页数
    '''
    home_link = u'首页'
    prev_link = u'←'
    next_link = u'→'
    last_link = u'尾页'
    num_tag_open = '<li>'
    num_tag_close = '</li>'

    def __init__(self, total_count, page_size=20, cur_page=1,url=None ):
        self.url = url and url or '?p=%s'
        self.total_count = total_count#总条目数
        self.page_size = page_size#每页条目数
        self.cur_page = cur_page#当前页数
        self.page_count,tail = divmod(self.total_count,self.page_size)#获取总分页数
        if tail is not 0:
            self.page_count += 1
        self.pages=[]

    def getPage(self):
        if self.total_count <= self.page_size:
            return ''
        if self.cur_page>1:
            self.pages.append('%s<a href="%s">%s</a>%s' %(self.num_tag_open, self.url %(self.cur_page-1), self.prev_link, self.num_tag_close))
            # self.pages.append('%s<a href="%s">%s</a>%s' %(self.num_tag_open, self.url %1,self.last_link, self.num_tag_close))
        if self.cur_page<=5:
            limit_s=1
        else:
            limit_s=self.cur_page-4

        if self.page_count>=self.cur_page+5:
            limit_e=self.cur_page+5
        else:
            limit_e=self.page_count
            if self.cur_page>=10:
                limit_s=self.cur_page-9

        for i in xrange(limit_s,limit_e+1):
            if self.cur_page==i:
                self.pages.append('%s<a href="javascript:;" class="active">%s</a>%s'%(self.num_tag_open, self.cur_page, self.num_tag_close))
            else:
                self.pages.append('%s<a href="%s">%s</a>%s' %(self.num_tag_open, self.url%i, i, self.num_tag_close))
        
        if self.cur_page<self.page_count:
            self.pages.append('%s<a href="%s">%s</a>%s' %(self.num_tag_open,(self.url%(self.cur_page+1)), self.next_link, self.num_tag_close))
            # self.pages.append('%s<a href="%s">%s</a>%s'%(self.num_tag_open, (self.url %self.page_count), self.last_link, self.num_tag_close))
        return "".join(self.pages)