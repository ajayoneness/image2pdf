from datetime import datetime
import os
import MySQLdb
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename


class MyServer:
    def __init__(self):
        self.tname = f"ajay"


app=Flask(__name__)

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="img2pdf"

mysql=MySQL(app)


obj = MyServer()


UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=["POST","GET"])
def index():
    return render_template('index.html')

@app.route('/upload',methods=['GET','POST'] )
def upload():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    count=0
    if request.method == 'POST':
        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute(f"INSERT INTO {obj.tname} (img, date) VALUES (%s,%s)", [filename,now])
                mysql.connection.commit()
                count = count+1
        cur.close()
        if count==0:
            sub='no file selected'
        else:
            sub='sucessufully submited to database'
    else:
        sub = ''

    cur = mysql.connection.cursor()
    dimg = cur.execute(f'select * from {obj.tname}')

    if dimg > 0:
        dimages = cur.fetchall()
        print(dimages)
    else:
        dimages = ''

    return render_template('index.html',subm=sub,images=dimages)


@app.route('/convert',methods=['GET','POST'])
def convert():
    cur = mysql.connection.cursor()
    dbimg = cur.execute(f'select * from {obj.tname}')

    if dbimg > 0:
        dbimages=[]
        dbimage = cur.fetchall()
        for i in dbimage:
            dbimages=(f"{i[0]}")
    else:
        dbimages = ''
    con="converted sucessfully"
    return render_template('index.html',convert=con, im=dbimage)







@app.route('/download',methods=['GET','POST'])
def download():
    return render_template('download.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)