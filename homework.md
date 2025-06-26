## Virtual School
###### 肖博文 2200013174 潘聿阳 
------

### 项目描述
virtual school 是一个基于 javascript 的网页版校园地图。该地图主要提供的功能有：
- 对北大燕园校区的主要场景和建筑相关信息的简易交互式查询
- 对教学楼内部教室的时间安排和空闲状态的可视化
- 对目前正在开设的所有课程的相关信息查询。包括任课老师，上课时间，上课地点等
- 对学生常用校园网站的便捷式访问接口

项目链接：[https://github.com/Bowie375/virtual_school](https://github.com/Bowie375/virtual_school)

### 项目结构
该项目主要由前端网站页面设计，后端服务器接口，以及数据库存储三部分组成。

#### 1. 前端网页
前端网页采用 __Vue__ 框架，利用其热更新和组件化特性等优势实现了项目的高效开发。

实现细节：
1. `App.vue` ：主页面，包括左侧导航栏，中间校园地图和右上角的搜索框。
    - 左侧导航栏为学生常用网站链接，包括树洞，BBS，门户，教学网，课程测评等网站。
    - 地图由基地图，svg 区域框，和指向各建筑和场景的 gif 动画组成。通过设计各区域的 CSS 样式，实现了地图上区域在鼠标 hover 后突出显示的效果。点击地图上的建筑或场景会触发相应的处理函数，如果是教学楼，则 visualize 该教学楼对应的组件。

2. `components/building.vue` ：教学楼模块，显示各教学楼的教室占用情况
    - 教学楼会默认自动查询当天教学楼内部所有教室的占用情况，并显示在地图中央，如果更改查询日期，会 async 处理向服务器请求数据并更新地图。
    - 点击地图上的教室会触发 visualize 该教室对应的组件。
    - 效果展示：
    ![building.vue](building.png)
    <br/>

3. `components/classroom.vue` ：教室模块，显示该教室的具体课程信息。
    - 向服务器请求该教室的课程信息，并显示在地图上，以一天12节课为格式显示。
    - 效果展示：
    ![classroom.vue](classroom.png)
    <br/>

4. `components/course.vue` ：搜索模块，实现根据课程名对课程信息的搜索功能。
    - 输入课程名，点击搜索按钮，会向服务器请求所有匹配的课程信息，并显示在地图上。
    - 进一步点击课程，会显示该课程的详细信息，包括任课老师，上课时间，上课地点等。
    - 效果展示：
    ![course.vue](search.png)

代码位置：`src/vschool/frontend`

#### 2. 后端服务器
后端服务器采用 __flask__ 框架，为网页端 https 请求提供路径接口，并调用数据库接口进行数据查询。

代码位置：`src/vschool/backend`

#### 3. 数据库存储
数据库部分采用 __sqlite__ 作为存储引擎，以 __sqlalchemy__ 构建了 ORM 数据接口。

实现细节：
1. 关系模型：
```python
# 课程表
class Course(Base, SerializerMixin):
    __tablename__ = 'Course'

    course_id = Column(Text, nullable=False)
    class_id = Column(Integer, nullable=False)
    course_name = Column(Text, nullable=False)
    department = Column(Text, nullable=False)
    teacher = Column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint("length(course_id) = 8 AND course_id GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'"),
        PrimaryKeyConstraint('course_id', 'class_id', name='pk_course'),
    )

# 日程表
class Schedule(Base, SerializerMixin):
    __tablename__ = 'Schedule'

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Text, nullable=False)
    class_id = Column(Integer, nullable=False)
    start_week = Column(Integer, nullable=False)
    end_week = Column(Integer, nullable=False)
    weekday = Column(Integer, nullable=False)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    location = Column(Text, nullable=False)
    frequency = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['course_id', 'class_id'], ['Course.course_id', 'Course.class_id']),
    )
```

2. 接口设计：
    - `Database.get_course` ：以输入课程名做模糊匹配（COLUMN LIKE '%INPUT%'），返回所有匹配的课程的相关信息（课程名，任课老师，上课时间，上课地点）。
    - `Database.get_classroom` ：根据教学楼名称，教室号和查询的时间，返回该教室在所查询的这一天的课程安排情况。
    - `Database.get_classroomMeta` ： 根据教学楼名称和查询的时间，返回该教学楼在所查询的这一天的空闲教室情况。

代码位置：`src/vschool/database`

### 运行方式
在项目根目录下，运行以下命令：
```
python run/main.py
```
此时前后端会同时启动，随后在浏览器中打开 http://localhost:3000/ 进行访问即可。详细的环境配置可以参考[代码仓库](https://github.com/Bowie375/virtual_school)的 README。

### 项目分工


### 附录

#### 1. 近期生活照

#### 2. 出勤次数