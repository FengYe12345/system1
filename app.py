from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask import Flask, session, redirect, url_for, request, flash, render_template
from sqlalchemy import and_
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/first_flask'
app.config['SQLCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'iii'
db = SQLAlchemy(app)


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='first_flask', charset='utf8')
cursor = conn.cursor()
cursor.execute('set names utf8')
cursor.execute('set autocommit = 1')
# sql = 'select * from box_config'
# cursor.execute(sql)
# result = cursor.fetchall()
# print(result)

# 用户登录账号密码的ORM
class User(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

# 数据库表box_config的ORM模型
class Box(db.Model):
    __tablename__ = 'box_config'
    id = db.Column(db.Integer(),nullable = True,primary_key=True)
    box_id = db.Column(db.String(20), nullable=True)
    server = db.Column(db.String(20), nullable=True)
    port = db.Column(db.Integer(), nullable=True)
    enable = db.Column(db.Integer(), nullable=True)
    collection_thread_id = db.Column(db.Integer(), nullable=False)
    server_thread_id= db.Column(db.Integer(), nullable=False)
    cloud_id = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Integer(), nullable=True)
    sleep = db.Column(db.Float(0), nullable=True)


# 数据库表box_base_config的ORM
class Box_base(db.Model):
    __tablename__ = 'box_base_config'
    id = db.Column(db.Integer(),nullable = True,primary_key=True)
    box_id = db.Column(db.String(20), nullable=True)
    card_type = db.Column(db.Integer(), nullable=True)
    card_number = db.Column(db.String(20), nullable=True)
    card_cost = db.Column(db.Integer(), nullable=True)
    start_date = db.Column(db.Date(), nullable=False)
    box_type= db.Column(db.Integer(), nullable=False)
    cloud_id = db.Column(db.String(255), nullable=False)
    project = db.Column(db.String(255), nullable=True)
    machine = db.Column(db.String(255), nullable=True)
    machine_type = db.Column(db.Integer(), nullable=True)
    box_msg = db.Column(db.String(255), nullable=True)
    port = db.Column(db.Integer(), nullable=True)
    position = db.Column(db.String(255), nullable=True)
# form表单的wtforms模型
# class BoxForm(FlaskForm):
#     box_id = StringField('box_id', validators=[DataRequired()])
#     server = StringField('server', validators=[DataRequired()])
#     port = StringField('port', validators=[DataRequired()])
#     enable = StringField('enable', validators=[DataRequired()])
#     cloud_id = StringField('cloud_id', validators=[DataRequired()])
#     type = StringField('type', validators=[DataRequired()])
#     sleep = StringField('sleep', validators=[DataRequired()])
#     submit = SubmitField(u'提交')
# 登录功能实现
def valid_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        return True
    else:
        return False





def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login.html', next=request.url))

    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash('登录成功！')
            session['username'] = request.form.get('username')
            return redirect(url_for('_blank'))
        else:
            error = '错误的用户名或者密码!'
    return render_template('login.html', error=error)





# 删除某一行数据
@app.route('/delete_box/<Box_id>')
def delete_box(Box_id):
    sql = "DELETE FROM box_config WHERE ID = '%d'" % (int(Box_id))
    cursor.execute(sql)
    return redirect(url_for('_blank'))
# 删除box_base_config数据
@app.route('/delete_box_base/<Box_id>')
def delete_box_base(Box_id):
    sql = "DELETE FROM box_base_config WHERE ID = '%d'" % (int(Box_id))
    cursor.execute(sql)
    return redirect(url_for('box_base'))



#
# 添加数据
@app.route('/add',methods=['GET','POST'])
def add():
    error = None
    if request.method == 'POST':
        try:
            a2=request.form['box_id']
            a3 = request.form['server']
            a4 = request.form['port']
            a5 = request.form['enable']
            a6 = request.form['cloud_id']
            a7 = request.form['type']
            a8 = request.form['sleep']
            sql = "insert into box_config (box_id, server,port,enable,cloud_id,type,sleep) values('%s','%s','%s','%s','%s','%s','%s')" %(a2,a3,a4,a5,a6,a7,a8)
            cursor.execute(sql)
            return redirect(url_for('_blank'))
        except Exception as e:
            return redirect(url_for('mistake'))
    else:
        flash('添加错误')
    return render_template('member-add.html')

# box_base添加
@app.route('/add_box_base',methods=['GET','POST'])
def add_box_base():
    error = None
    if request.method == 'POST':
        try:
            a2=request.form['box_id']
            a3 = request.form['card_type']
            a4 = request.form['card_number']
            a5 = request.form['card_cost']
            a6 = request.form['start_date']
            a7 = request.form['box_type']
            a8 = request.form['cloud_id']
            a9 = request.form['project']
            a10 = request.form['machine']
            a11 = request.form['machine_type']
            a12 = request.form['box_msg']
            a13 = request.form['port']
            a14 = request.form['position']
            sql = "insert into box_base_config (box_id, card_type,card_number,card_cost,start_date,box_type,cloud_id,project,machine,machine_type,box_msg,port,position) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14)
            cursor.execute(sql)
            return redirect(url_for('box_base'))
        except Exception as e:
            return redirect(url_for('mistake'))
    else:
        flash('添加错误')
    return render_template('box_base_add.html')

@app.route('/404')
def mistake():
    return render_template('404.html')
# 循环查询数据封装在列表中

# 主页面index
@app.route('/index')
def index():
    return render_template('index.html')
# 基础信息页面
@app.route('/_blank')
def _blank():
    id_list = []
    a = Box.query.all()
    # print(a)
    j = 0
    for i in a:
        id_list.append(i.id)
    # print(id_list)
    data_list = []
    while (j < len(id_list)):
        data_j = {
            'id': a[j].id,
            'box_id': a[j].box_id,
            'server': a[j].server,
            'port': a[j].port,
            'enable': a[j].enable,
            'collection_thread_id': a[j].collection_thread_id,
            'server_thread_id': a[j].server_thread_id,
            'cloud_id': a[j].cloud_id,
            'type': a[j].type,
            'sleep': a[j].sleep
        }
        data_list.append(data_j)
        j = j + 1
    return render_template('_blank.html',data_list =data_list)
# 基础配置信息页面
@app.route('/_blue')
def _blue():
    return  render_template('_blue.html')
# 网关配置信息
@app.route('/box_base')
def box_base():
    id_list = []
    a = Box_base.query.all()
    # print(a)
    j = 0
    for i in a:
        id_list.append(i.id)
        # print(id_list)
    data_list = []
    while (j < len(id_list)):
        data_j = {
            'id': a[j].id,
            'box_id': a[j].box_id,
            'card_type': a[j].card_type,
            'card_number': a[j].card_number,
            'card_cost': a[j].card_cost,
            'start_date': a[j].start_date,
            'box_type': a[j].box_type,
            'cloud_id': a[j].cloud_id,
            'project': a[j].project,
            'machine': a[j].machine,
            'machine_type': a[j].machine_type,
            'box_msg': a[j].box_msg,
            'port': a[j].port,
            'position': a[j].position
        }
        data_list.append(data_j)
        j = j + 1
    return render_template('box_base_config.html', data_list=data_list)

# 根据日期来查询
@app.route('/select',methods=['GET','POST'])
def select():
    return render_template('select.html')
# 日期查询的返回结果
@app.route('/result',methods=['GET','POST'])
def result():
    a1 = request.form.get('time1')
    print(a1)
    a2 = request.form.get('time2')
    sql = "select * from box_base_config where start_date between '%s' and '%s'" %(a1,a2)
    cursor.execute(sql)
    result = cursor.fetchall()
    data_list = result
    print(data_list)
    a = data_list
    j = 0
    result_list=[]
    while (j<len(a)):
        data_j = {
            'id': a[j][0],
            'box_id': a[j][1],
            'card_type': a[j][2],
            'card_number': a[j][3],
            'card_cost': a[j][4],
            'start_date': a[j][5],
            'box_type': a[j][6],
            'cloud_id': a[j][7],
            'project': a[j][8],
            'machine': a[j][9],
            'machine_type': a[j][10],
            'box_msg': a[j][11],
            'port': a[j][12],
            'position': a[j][13]
        }
        result_list.append(data_j)
        j = j + 1
    return  render_template('result.html',result_list=result_list)


# 根据id来查询
@app.route('/boxid_select')
def id_select1():
    return render_template('boxid_select.html')

@app.route('/result_box_id',methods=['GET','POST'])
def result_box_id():
    a1 = request.form.get('box_id')
    sql = "select * from box_config where box_id =('%s') " % (a1)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    a= result
    data_list = []
    j=0
    while (j < len(a)):
        data_j = {
            'id': a[j][0],
            'box_id':a[j][1],
            'server': a[j][2],
            'port': a[j][3],
            'enable': a[j][4],
            'collection_thread_id': a[j][5],
            'server_thread_id': a[j][6],
            'cloud_id': a[j][7],
            'type': a[j][8],
            'sleep': a[j][9],
        }
        data_list.append(data_j)
        j = j + 1
    return render_template('result_box_id.html',data_list=data_list)


if __name__ == '__main__':
    app.run(debug=True)
