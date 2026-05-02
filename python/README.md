创建虚拟环境
python -m venv .venv
激活虚拟环境
.venv\Scripts\activate
安装依赖，只用装一次
pip install -r requirements.txt
初始化数据库（只用初始化一次，后面不再需要）
python init_db.py
运行
python app.py
或
python app2.py

### 文件说明

init_db.py
初始化数据库。
只用运行一次。

config.py
数据库路径和图片存储目录。

database.py
封装所有数据库操作，包括：
- 插入新图片记录（insert_image）
- 查询状态为 pending 的任务（fetch_pending）
- 更新任务状态（update_status）
- 查询所有图片记录（fetch_all_images）

processing.py
图片处理逻辑。
如果以后要调整处理算法，来这里改。

worker.py
后台工作线程。
持续轮询数据库，发现 pending 任务就取出来处理，处理完更新状态为 done 或 failed。
没有任务时休眠 10 秒再轮询。
处理完会把结果写回数据库。

routes.py
三个接口：上传图片、查询所有记录、直接访问图片文件。
定义所有 HTTP 路由：
- POST /api/ingest                  接收上传的图片，存档并写入数据库
- GET  /api/images                  返回所有图片记录（含处理状态）
- GET  /images/<folder>/<filename>  直接访问原始或处理后的图片文件

app.py
程序入口。连接前端。
运行方式：python app.py

app2.py
后端处理。