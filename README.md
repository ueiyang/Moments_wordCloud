# Moments_wordCloud
利用appium+python采集自己或好友的朋友圈文本，并生成词云
由于微信朋友圈没有开放接口 ，想要获取朋友圈信息比较困难。
本项目利用appium+python，实现抓取自己或任一好友的朋友圈文本信息，并且可以指定年份。
抓取朋友圈文本信息后，使用jieba分词，并根据ti-idf算法提取关键字，利用python的wordcloud包实现词云可视化。
博客地址：https://blog.csdn.net/weixin_42138362/article/details/96478733、
https://blog.csdn.net/weixin_42138362/article/details/96483847
