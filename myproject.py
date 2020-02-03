from werkzeug.utils import secure_filename
import os
import time
from mylibrary import check_photo
from flask import Flask, render_template, request,redirect,url_for, session
import pymysql
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='./static/photos'
app.secret_key="Super secret key"
@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/admin_reg', methods= ['GET','POST'])
def admin_reg():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method=='POST':
                #write code of submit button
                #receive the form data
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                email=request.form['T4']
                password=request.form['T5']
                name=name.strip()
                address=address.strip()
                contact=contact.strip()
                email=email.strip()
                if name=='':
                    msg='Enter name'
                elif address=='':
                    msg='Enter address'
                elif contact=='':
                    msg='Enter contact'
                elif email=='':
                    msg='Enter email'
                else:
                    try:
                        conn=pymysql.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='',
                        db='madhur',
                        autocommit=True
                        )
                        cur=conn.cursor()
                        sql1="INSERT INTO admindata VALUES('"+name+"','"+address+"','"+contact+"','"+email+"')"
                        sql2="INSERT INTO logindata VALUES('"+email+"','"+password+"','"+ut+"')"
                        print(sql1)
                        print(sql2)
                        cur.execute(sql1)
                        n=cur.rowcount
                        cur.execute(sql2)
                        m=cur.rowcount
                        msg="error:cannot save data"
                        if(n==1 and m==1):
                            msg="data saved and login created"
                        elif(n==1):
                            msg="Data saved but login not created"
                        elif(m==1):
                            msg="Login created but data not saved"
                        #Show the form again with response
                    except:
                        msg='email already exists'
                return render_template('AdminReg.html',madhur=msg)
            else:
                return render_template('AdminReg.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/show_admins')
def show_admins():
    if 'usertype' in session:
        ut=session['usertype']

        if ut=='admin':
            conn=pymysql.connect(
            host='localhost',
            user='root',
            port=3306,
            passwd='',
            db='madhur',
            autocommit=True
            )
            cur=conn.cursor()
            sql="SELECT * FROM admindata"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template('ShowAdmins.html',Kota=data)
            else:
                msg="No data found"
                return render_template('ShowAdmins.html',jpr=msg)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/hospital')
def show_hospital():

    conn=pymysql.connect(
                user='root',
                host='localhost',
                passwd='',
                port=3306,
                db='madhur',
                autocommit=True
            )
    cur=conn.cursor()
    sql="Select * from hospital_data"
    cur.execute(sql)
    n=cur.rowcount
    if(n>0):
        data=cur.fetchall()
        return render_template('Hospital.html',Kota=data)
    else:
        msg='Data not found'
        return render_template('Hospital.html',jpr=msg)

@app.route('/hospital_reg', methods= ['GET','POST'])
def hospital_reg():
    if 'usertype' in session:
        ut=session['usertype']

        if ut=='admin':

            if request.method=='POST':
                #write code of submit button

                #receive the form data
                name=request.form['T1']
                speciality=request.form['T2']
                address=request.form['T3']
                contact=request.form['T4']
                ac_beds=request.form['T5']
                non_ac_beds = request.form['T6']
                email= request.form['T7']
                password= request.form['T8']
                usertype='hospital'
                conn=pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='madhur',
                autocommit=True
                )
                cur=conn.cursor()
                sql1="INSERT INTO hospital_data VALUES('"+name+"','"+speciality+"','"+address+"','"+contact+"','"+ac_beds+"','"+non_ac_beds+"','"+email+"')"
                sql2="INSERT INTO logindata VALUES('"+email+"','"+password+"','"+usertype+"')"
                print(sql1)
                print(sql2)
                cur.execute(sql1)
                n=cur.rowcount
                cur.execute(sql2)
                m=cur.rowcount
                msg="error:cannot save data"
                if(n==1 and m==1):
                    msg="data saved and login created"
                elif(n==1):
                    msg="Data saved but login not created"
                elif(m==1):
                    msg="Login created but data not saved"
                #Show the form again with response
                return render_template('hospitalReg.html',madhur=msg)
            else:
                return render_template('hospitalReg.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/show_hospitals')
def show_hospitals():
    if 'usertype' in session:
        utype = session['usertype']
        if utype == 'admin':

            conn=pymysql.connect(
                user='root',
                host='localhost',
                port=3306,
                passwd='',
                db='madhur',
                autocommit=True
            )
            cur=conn.cursor()
            sql="select * from hospital_data"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template('ShowHospitals.html',kota=data)
            else:
                msg='Data not found'
                return render_template('ShowHospitals.html',jpr=msg)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/edit_hospital', methods=['GET','POST'])
def edit_hospital():
    if 'usertype' in session:
        utype = session['usertype']

        if utype == 'admin':
            if(request.method=='POST'):
                email=request.form['H1']
                conn=pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    port=3306,
                    db='madhur',
                    autocommit=True
                )
                cur=conn.cursor()
                sql="select * from hospital_data where email='"+email+"'"

                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template('editHospital.html',kota=data)
                else:
                    msg="no data found"
                    return render_template('editHospital.html',jpr=msg)
            else:


                return redirect(url_for('show_hospitals'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/edit_hospital_1', methods=['GET','POST'])
def edit_hospital_1():
    if 'usertype' in session:
        utype = session['usertype']
        if utype == 'admin':
            if(request.method=='POST'):
                name=request.form['T1']
                sp=request.form['T2']
                address=request.form['T3']
                contact=request.form['T4']
                ac=request.form['T5']
                nonac=request.form['T6']
                email=request.form['T7']
                conn = pymysql.connect(
                    user='root',
                    host='localhost',
                    port=3306,
                    passwd='',
                    db='madhur',
                    autocommit=True
                )
                cur = conn.cursor()
                sql="update hospital_data set hospital_name='"+name+"',speciality='"+sp+"', address='"+address+"', contact='"+contact+"', ac_beds='"+ac+"',non_ac_beds='"+nonac+"' where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n>0):
                    return render_template('editHospital1.html', msg="Data saved")
                else:
                    return render_template('editHospital1.html', msg="Data not saved")
            else:
                return redirect(url_for('show_hospitals'))
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['T1']
        password=request.form['T2']
        conn=pymysql.connect(
            user='root',
            passwd='',
            port=3306,
            host='localhost',
            db='madhur',
            autocommit=True

        )
        cur=conn.cursor()
        sql="select * from logindata where email='"+email+"' and password='"+password+"'"
        cur.execute(sql)
        n=cur.rowcount
        if(n==1):
            #correct login
            data=cur.fetchone()
            utype=data[2]
            #create session
            session['usertype']=utype
            session['email']=email
            if utype=='admin':
                return redirect(url_for('adminhome'))
            elif utype=='hospital':
                return redirect(url_for('hospital_home'))
        else:
            msg='Incorrect email or password'
            return render_template('Login.html',kota=msg)
    else:
        return render_template('Login.html')
@app.route('/adminhome')
def adminhome():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            photo=check_photo(email)
            return render_template('AdminHome.html',e1=email,photo=photo)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/hospital_home')
def hospital_home():
    if 'usertype' in session:
        utype=session['usertype']
        email=session['email']
        if utype=='hospital':
            photo = check_photo(email)

            return render_template("hospitalHome.html", e1=email, photo=photo)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/logout')
def logout():
    if 'usertype' in session:
        session.pop('usertype',None)
        session.pop('email',None)
        return(redirect(url_for('login')))
    else:
        return (redirect(url_for('login')))

@app.route('/autherror')
def autherror():
    return render_template('authError.html')
@app.route('/change_password_admin',methods=['GET','POST'])
def change_password_admin():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='admin':
            if request.method=='POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                conn=pymysql.connect(user='root',host='localhost',passwd='',port=3306,db='madhur',autocommit=True)
                cur=conn.cursor()
                sql="update logindata set password='"+newpass+"' where email='"+e1+"' and password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    msg='new password set successfully'
                    return render_template('changePasswordAdmin.html',data=msg)
                else:
                    msg="Old password is incorrect"
                    return render_template('changePasswordAdmin.html',data=msg)
            else:
                return render_template('changePasswordAdmin.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/change_password_hospital',methods=['GET','POST'])
def change_password_hospital():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='hospital':
            if request.method=='POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                conn=pymysql.connect(user='root',host='localhost',passwd='',port=3306,db='madhur',autocommit=True)
                cur=conn.cursor()
                sql="update logindata set password='"+newpass+"' where email='"+e1+"' and password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    msg='new password set successfully'
                    return render_template('changePasswordHospital.html',data=msg)
                else:
                    msg="Old password is incorrect"
                    return render_template('changePasswordHospital.html',data=msg)
            else:
                return render_template('changePasswordHospital.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/admin_profile',methods=['GET','POST'])
def admin_profile():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='admin':
            if request.method=='POST':
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                conn=pymysql.connect(
                    user='root',
                    host='localhost',
                    port=3306,
                    passwd='',
                    db='madhur',
                    autocommit=True
                )
                cur=conn.cursor()
                sql="update admindata set name='"+name+"', address='"+address+"', contact='"+contact+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('AdminProfile1.html', msg='changes saved successfully')
                else:
                    return render_template('AdminProfile.html', msg='No changes found')
            else:
                #fetch data and show it
                conn=pymysql.connect(
                    user='root',
                    host='localhost',
                    port=3306,
                    passwd='',
                    db='madhur',
                    autocommit=True
                )
                cur=conn.cursor()
                sql="select * from admindata where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('AdminProfile.html',data=data)
                else:
                    return render_template('AdminProfile.html',data1='no data found')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/hospital_profile', methods=['GET','POST'])
def hospital_profile():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='hospital':
            if request.method=='POST':
                name=request.form['T1']
                speciality=request.form['T2']
                address=request.form['T3']
                contact=request.form['T4']
                ac_beds=request.form['T5']
                non_ac_beds=request.form['T6']

                conn=pymysql.connect(
                    user='root',
                    host='localhost',
                    port=3306,
                    passwd='',
                    db='madhur',
                    autocommit=True
                )
                cur=conn.cursor()
                sql="update hospital_data set hospital_name='"+name+"', speciality='"+speciality+"', address='"+address+"', contact='"+contact+"', ac_beds='"+ac_beds+"',non_ac_beds='"+non_ac_beds+"' where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('HospitalProfile1.html', msg='changes saved successfully')
                else:
                    return render_template('HospitalProfile.html', msg='No changes found')
            else:
                #fetch data and show it
                conn=pymysql.connect(
                    user='root',
                    host='localhost',
                    port=3306,
                    passwd='',
                    db='madhur',
                    autocommit=True
                )
                cur=conn.cursor()
                sql="select * from hospital_data where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('HospitalProfile.html',data=data)
                else:
                    return render_template('HospitalProfile.html',data1='no data found')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/doctor_reg', methods=['GET','POST'])
def doctor_reg():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='hospital':
            if request.method=='POST':
                Name=request.form['T1']
                Speciality=request.form['T2']
                Timing=request.form['T3']
                Experience=request.form['T4']

                conn=pymysql.connect(
                    host='localhost',
                    user='root',
                    passwd='',
                    port=3306,
                    db='madhur',
                    autocommit=True
                )
                cur=conn.cursor()
                sql="Insert into registered_doctors values('"+Name+"','"+Speciality+"' ,'"+Timing+"', '"+Experience+"', '"+e1+"')"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template('DoctorRegistration.html',msg="Data saved")
                else:
                    return render_template('DoctorRegistration.html', msg="Error data not saved")
            return render_template('DoctorRegistration.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))


@app.route('/adminphoto1',methods=['GET','POST'])
def adminphoto1():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='madhur',autocommit=True)
                    cur = conn.cursor()
                    sql = "insert into photodata values('"+email+"','" + filename + "')"

                    try:
                        cur.execute(sql)
                        n = cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('photoupload_admin1.html', result="success")
                        else:
                            return render_template('photoupload_admin1.html', result="failure")
                    except:
                        return render_template('photoupload_admin1.html', result="duplicate")
            else:
                return render_template('photoupload_admin.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/adminphoto')
def adminphoto():
    if 'usertype' in session:
        usertype=session['usertype']
        if usertype == 'admin':
            return render_template('photoupload_admin.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/change_adminphoto')
def change_adminphoto():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            photo = check_photo(email)
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='madhur', autocommit=True)
            cur = conn.cursor()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return render_template('change_adminphoto.html',data="success")
            else:
                return render_template('change_adminphoto.html', data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/show_doctors')
def show_doctors():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='hospital':
            conn=pymysql.connect(
            host='localhost',
            user='root',
            port=3306,
            passwd='',
            db='madhur',
            autocommit=True
            )
            cur=conn.cursor()
            sql="SELECT * FROM registered_doctors where Email_of_hospital='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template('ShowDoctors.html',Kota=data)
            else:
                msg="No data found"
                return render_template('ShowDoctors.html',jpr=msg)
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/hospitalphoto')
def hospitalphoto():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='hospital':
            return render_template('photoupload_hospital.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/hospitalphoto1', methods=['GET', 'POST'])
def hospitalphoto1():
    if 'usertype' in session:
        usertype = session['usertype']
        email = session['email']
        if usertype == 'hospital':
            if request.method == 'POST':
                file = request.files['F1']
                if file:
                    path = os.path.basename(file.filename)
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='madhur',
                                               autocommit=True)
                    cur = conn.cursor()
                    sql = "insert into photodata values('" + email + "','" + filename + "')"

                    try:
                        cur.execute(sql)
                        n= cur.rowcount
                        if n == 1:
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            return render_template('photoupload_hospital1.html', result="success")
                        else:
                            return render_template('photoupload_hospital1.html', result="failure")
                    except:
                        return render_template('photoupload_hospital1.html', result="duplicate")
            else:
                return render_template('photoupload_hospital.html')
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))

@app.route('/change_hospitalphoto')
def change_hospitalphoto():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='hospital':
            photo = check_photo(email)
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='madhur', autocommit=True)
            cur = conn.cursor()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                os.remove("./static/photos/"+photo)
                return render_template('change_hospitalphoto.html',data="success")
            else:
                return render_template('change_hospital.html', data="failure")
        else:
            return redirect(url_for('autherror'))
    else:
        return redirect(url_for('autherror'))
@app.route('/edit_doctor')
def edit_doctor():
    if 'usertype' in session:
        usertype=session['usertype']
        e1=session['email']
        if usertype=='hospital':
            if request.method=='POST':
                name=request.form['T1']
                spec=request.form['T2']
                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='madhur',
                                       autocommit=True)
                cur = conn.cursor()
                sql="select * from registered_doctors where Name='"+name+"' AND Speciality='"+spec+"' AND Email_of_hospital='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('EditDoctor.html',data=data)
                else:
                    return render_template('EditDoctor.html',msg='No Data Found')
            else:
                return redirect(url_for('show_doctors'))
        else:
            return redirect(url_for('autherror'))





if __name__=='__main__':
    app.run(debug=True)

