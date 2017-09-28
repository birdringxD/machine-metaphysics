# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES,\
 patch_request_class
import predict
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = './cache'  # Uploads dir

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>机器算命</h1>
    <form method=post enctype=multipart/form-data>
         <label for="name">姓名 </label>: 
         <input id="name1" name="name1" size="8" type="text" value="" required="required">
         <input id="name2" name="name2" size="8" type="text" value="" required="required">
         <br>
         
         <label for="age">年龄 </label>: 
         <input id="age1" name="age1" size="2" type="text" value="" required="required">
         <input id="age2" name="age2" size="2" type="text" value="" required="required">
         <br>
         
         <label>照片 :</label>
         <input type=file name=photo>
         <input type=submit value=上传>
    </form>
   
    '''


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # print request
    if request.method == 'POST' and 'photo' in request.files:
        name1 = request.form.get("name1")
        name2 = request.form.get("name2")
        age1 = int(request.form.get("age1"))
        age2 = int(request.form.get("age2"))

        f = request.files['photo']
        full_name = './cache/' + name1 + '_' + name2 + '_' + \
                   str(age1) + '_' + str(age2) + '_' + secure_filename(f.filename)
        f.save(full_name)
       # filename = photos.save(r equest.files['photo'])
        #print filename
        filename = secure_filename(f.filename)
        print filename
        # outname = name1 + '_' + name2 + '_' + \
        #           str(age1) + '_' + str(age2) + '_' + filename
        outname = '#$' + filename

        max_sim, ii, jj = predict.save_predict_img(full_name, './cache/' + outname)
        print 'max_sim is :',max_sim, ii, jj

        if abs(age1 - age2) > 1 :
            max_sim = max(max_sim * (1 - (1.0 * abs(age1 - age2)) / 30), 0.01)

        print request.form.to_dict()
        print len(request.form)
        print request.form.get("name1"), request.form.get("name2"), age1, age2

        file_url = photos.url(outname)

    # return html + '<br><img src=' + file_url + '>' + \
    #           '<br> ' + str(ii) + ' and ' +  str(jj) + ' are most similar, ' \
    #           + ' similarity is: ' + str('%.2f' % (max_sim * 100)) + '%' \

        return html + '<br><img src=' + file_url + '>' + '<br>' + \
           str(ii) + ' and ' + str(jj) + ' 的' + \
           ' 匹配程度为: ' + str('%.2f' % (max_sim * 100)) + '%'
    return html
            #return html + '<br><img src=' + file_url + '>' + '<br>' + '老夫掐指一算，这位先生怕是有大凶之兆！'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999)