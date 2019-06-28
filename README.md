# OnekkiSite
## onekki的个人网站
### 启动项目
```python
python manager.py runserver -h 127.0.0.1 -p 5000 -d
```
### 生成数据模型
```python
flask-sqlacodegen 'mysql+pymysql://username:password@host:port/database' --outfile "gen_models.py" --flask
```
## 网站模块:
### 博客
### 后台管理