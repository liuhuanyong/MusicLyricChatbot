# MusicChatbot
chatbot based on music region using method including es and music kb.基于14W歌曲知识库的问答尝试，功能包括歌词接龙，已知歌词找歌曲以及歌曲歌手歌词三角关系的问答。

# 项目由来
听歌识曲，歌词对唱，智能点歌是目前智能音乐中特别火的方向。本项目将使用最为传统的方法，以构建歌曲歌词语料库出发，以歌词为中心，构建歌曲、歌手、歌词三角知识库。并借助es完成相应的查询服务。  
本项目的技术点包括：  
1、歌曲知识库构建  
2、es搜索  
本项目尝试完成的工作：  
1、歌词问答  
2、已知歌词查歌曲  
3、歌曲知识问答  

# 项目步骤:  
1、歌词语料库构建  
2、歌词、歌曲、歌手知识库构建  
3、基于知识库的问答挖掘  

# 项目路线图
![image](https://github.com/liuhuanyong/MusicChatbot/blob/master/img/route.png)  

# 项目运行方式
1、解压data/music.json.zip，解压后文件放在data下。
music.json中为歌曲的信息文件，包含以下几个字段：
1)singer:歌手名
2)album:专辑
3)song:歌曲名称
4)author:作词者
5)composer:作曲者
整个歌曲信息文件包含140068首歌曲。
2、python insert_es.py 将歌曲数据库插入至ES数据库中
3、python chat_main.py 启动歌词问答


# 执行效果






# 总结


