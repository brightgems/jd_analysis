# 分布式抓取京东商城评价并且使用 pandas 进行数据分析

现在互联网购物已经非常成熟而且很多人在网上购买商品后都会留下评论信息，而且有些商家为了获得好评还有一些好评优惠或者返点，那么我想试试可以从这些评价信息中获取到怎样的价值呢,我采用分布式快速抓取京东的评价信息，然后使用 pandas 对抓取到的数据进行分析。话不多说先附上使用地址<br>
体验地址：<http://awolfly9.com/jd/><br>
体验示例地址：<http://awolfly9.com/article/jd_comment_analysis><br>


**想要分析京东商城的商品评价信息，那么需要做些什么呢** <br>

* 采用分布式抓取，尽量在短时间内抓取需要分析的商品足够多的评价信息 <br>
* 将抓取到的评价信息都存储到数据库
* 从数据库中取出所有数据进行数据分析
	* 生成好评的词云，并且获取关键字
	* 生成中评的词云，并且获取关键字
	* 生成差评的词云，并且获取关键字
	* 分析购买该商品不同颜色的比例，生成柱状图
	* 分析购买该商品不同配置的比例，生成柱状图
	* 分析该商品的销售数量和评论数量和时间的关系，生成时间则线图
	* 分析该商品不同省份购买的的比例，生成柱状图
	* 分析该商品不同渠道的销售比例，生成柱状图
	
* 利用 Django 搭建后台，将数据抓取和数据分析连起来
* 前端显示数据抓取和分析结果


### 分布式抓取京东商城的评价信息
采用分布式抓取的目的是快速的在短时间内尽量抓取足够多的商品评价

1. 以 [iPhone7](https://item.jd.com/3995645.html) <https://item.jd.com/3995645.html> 为例，通过 Chrome 抓包分析出京东商城的评价请求 URl <https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2940&productId=3995645&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0>
2. 找出评价请求 URL 规律，获取到如下 URL 组合链接
3. 利用 Chrome 插件 Postman 测试链接是否可用，发现京东获取评价信息并没有验证 Cookie 之类的反爬措施
4. 开始编码利用 scrapy 抓取京东商城的商品评价信息并存入数据库以备使用

### 数据分析
1. 从数据库中取出相应数据，开始分析
2. 使用 python 的扩展库 wordcloud 分别提取好评、中评、差评的关键字，并且生成相应的词云图片
3. 分析该商品不同颜色的销量占比，并且生成柱状图，例如 iphone7 的不同颜色金色、玫瑰金色、银色、黑色、亮黑色、还有最新出的红色的占比
4. 分析该商品不同配置的销量占比，并且生成柱状图，例如 iphone7 32G 、 64G、128G 存储
5. 分析该商品销售和评论时间并且生成折线图，分析出商品在什么时间最畅销 
6. 分析用户购买该商品的渠道，例如用户通过京东 Android 客户端、微信京东购物、京东 iPhone 客户端购物的比例，并且生成柱状图
7. 分析购买该商品的用户的地域省份。例如北京、上海、广州那个城市在京东上购买 iPhone7 的人更多
8. 将以上分析结果都存储保留

### Django 后台 WEB
使用 Django 搭建一个简易的后台 jd_analysis，将分布式抓取数据和数据分析连起来，并且将分析结果返回前端显示。

1. jd_analysis 提供一个接口接受用户请求分析的京东商城商品的 URL 链接
2. jd_analysis 接受到商品链接后开启爬虫进程开始抓取需要分析的商品的名称和评价数量
3. 组合出完整的评价链接插入到 redis 中，实现分布式爬虫抓取，尽可能在短时间内抓取足够多的该商品评价信息（我现在是 30s 时间大概可以抓取 3000 条评价信息）
4. 主服务器等待一定的抓取时间，例如主服务器等待 30s，30s 后一定要给前端返回分析结果，所以等 30s 后清空 redis 中该商品的链接，从服务器没有读取不到需要抓取的链接也就自动关闭
5. 开启分析进程，开始分析抓取到的所有数据，并且生成图标等信息

### 前端展示
在客户端第一次请求时，生成一个 GUID，并且存储在 cookie 中。然后开启一个定时器，带上 GUID 不断的向 jd_analysis 后台请求结果。jd_analysis 后台利用请求的 GUID 从 redis 中获取抓取信息和分析结果的所有内容，返回给前端。前端显示请求到的结果。

### 最后附上两张效果图
**购买和评论时间折线图<br>**
![](http://i.imgur.com/dYShBOB.png)
**购买渠道柱状图<br>**
![](http://i.imgur.com/6PKeOOX.png)

### 大功告成
以上就是完整的抓取京东商品的评价信息并且使用 pandas 分析评价然后利用 Django 搭建后台前端显示抓取和分析结果的所有步骤。<br>

再次贴上使用地址：<http://awolfly9.com/jd/> 欢迎多多尝试，多挑毛病~<br>
如果你对这个项目感兴趣欢迎和我交流沟通，我也建立了这个项目和数据分析的微信群，也可以加我好友进微信群，我的个人微信<br>
![](http://awolfly9.com/static/images/weixin.png)





