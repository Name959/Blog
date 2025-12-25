# Blog 项目

这是一个使用 Django 构建的简单博客示例项目。

## 依赖

项目依赖列在 `requirements.txt` 中，安装方法：

```powershell
python -m venv ll_env
.\\ll_env\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## 数据库

项目使用默认的 SQLite 数据库（`db.sqlite3`）。在第一次运行前，请执行迁移：

```powershell
python manage.py migrate
python manage.py createsuperuser
```

## 启动开发服务器

```powershell
python manage.py runserver
```

打开浏览器访问 http://127.0.0.1:8000/ 查看项目。

## 备注

- 如果使用不同的虚拟环境路径，请相应调整激活命令。
- `requirements.txt` 中列出的是项目主要依赖，可能不是完整的环境导出。
