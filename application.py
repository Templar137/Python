
from flask import Flask, render_template, request, session, redirect
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys
import time
import pymysql
application = Flask(__name__)
application.config['SECRET_KEY'] = 'apptools'

dbconn = pymysql.connect(
    host='localhost',
    port = int(3306),
    user='root',
    passwd='1234',
    db='aifly',
    charset='utf8'
)

@application.route("/",  methods=['GET', 'POST'])
def hello():
    # return "<h1>danbibibi</h1>"
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        content = request.form['content']
        font_path = '/workspace/flask/static/NanumGothic.ttf'
        wordcloud = WordCloud(font_path=font_path, 
                              background_color='white', 
                              width=400, height=400)
        wordcloud = wordcloud.generate(content)
        fig = plt.figure(figsize=(6,6))
        plt.imshow(wordcloud)
        plt.axis('off')
        fig.savefig('/workspace/flask/static/wordcloud.png')
        return render_template('index.html', content=content, time=time.time())

@application.route("/login",  methods=['GET', 'POST'])
def login():
    # return "<h1>danbibibi</h1>"
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        userid = request.form['userid']
        userpw = request.form['userpw']
        cursor = dbconn.cursor()
        sql = """
        	select name from member where userid='%s' and userpw=password('%s');
        """ % (userid, userpw)
        cursor.execute(sql)
        rows = cursor.fetchone()
        dbconn.close()
        if rows:
            session['ss_id'] = userid
            session['ss_name'] = rows[0]
            return redirect('/')
        else:
            return render_template('login.html', msg="틀렸어! 다시 입력해")
        # return render_template('login.html', content=content, time=time.time())

        
@application.route("/logout")
def logout():
    session['ss_id'] = False
    session['ss_pw'] = False
    return redirect('/login')
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(sys.argv[1]))


