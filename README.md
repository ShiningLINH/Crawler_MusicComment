# Crawler_MusicComment
基于Selenium的网易云音乐评论爬虫

## 本项目预期实现功能
1. 抓取网易云音乐中指定歌曲的全部评论，并以csv格式存储（每首歌曲的评论对应唯一csv文件）
2. 根据指定范围内的csv文件和目标图片模板，绘制词云

## 当前进度
1. 输入歌曲网址 → 抓取其下评论（默认筛选出评论内容中的汉字部分，不需要筛选可删去相应代码）
2. 指定歌曲评论文件和目标图片模板 → 去掉无意义词语 → 绘制词云

- - -
*示例： Sakura -- 嵐（Arashi）的歌曲评论词云*
![wordcloud_test2](https://user-images.githubusercontent.com/102664839/160834378-ab31f17c-c077-4cea-ad63-513ce997d901.png)
- - -

## 已上传内容
1. 输入歌曲网址 → 抓取其下评论（默认筛选出评论内容中的汉字部分，不需要筛选可删去相应代码）

## NOTICE
- The copyright belongs to the author, *ShiningLINH*.
- Please feel free to contact me via email: linh852126@gmail.com.
