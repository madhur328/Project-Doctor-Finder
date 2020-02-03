from flask import session,Flask,render_template,request,redirect,url_for
import pymysql
from mylib import *

app=Flask(__name__)

app.secret_key="super secret key"

@app.route('/')
def welcome():
    return render_template('Welcome.html')

@app.route('/admin_reg',methods=['GET','POST'])
def admin_reg():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method == 'POST':
                # Write code of submit button

                # Receive the form data
                name = request.form['T1']
                address = request.form['T2']
                contact = request.form['T3']
                email = request.form['T4']
                password = request.form['T5']
                usertype = "admin"

                name=name.strip()
                address=address.strip()
                contact=contact.strip()
                email=email.strip()

                if name=="":
                    msg="Enter name "
                elif address=="":
                    msg="Enter address"
                elif contact=="":
                    msg="Enter contact"
                elif email=="":
                    msg="Enter email"
                else:
                    try:
                        cur = getdbcur()
                        sql1 = "insert into admindata values('" + name + "','" + address + "','" + contact + "','" + email + "')"
                        sql2 = "insert into logindata values('" + email + "','" + password + "','" + usertype + "')"

                        cur.execute(sql1)
                        n = cur.rowcount

                        cur.execute(sql2)
                        m = cur.rowcount

                        msg = "Error : Cannot save data"
                        if (n == 1 and m == 1):
                            msg = "Data saved and login created"
                        elif (n == 1):
                            msg = "Data saved but login not created"
                        elif (m == 1):
                            msg = "Login created but data not saved"
                    except:
                        msg="Email already exists"
                    # show the form again with response
                return render_template('AdminReg.html', kota=msg)
            else:
                return render_template('AdminReg.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))




@app.route('/admin_profile',methods=['GET','POST'])
def admin_profile():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='admin':
            if request.method=='POST':
                #save the changes
                name=request.form['T1']
                address=request.form['T2']
                contact=request.form['T3']
                cur=getdbcur()
                sql="update admindata set name='"+name+"',address='"+address+"',contact='"+contact+"'  where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n==1:
                    return render_template('AdminProfile1.html',msg="Changes saved successfully")
                else:
                    return render_template('AdminProfile1.html', msg="No changes found.")
            else:
                #fetch data and show it
                cur = getdbcur()
                sql = "select * from admindata where email='"+e1+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    data=cur.fetchone()
                    return render_template('AdminProfile.html',data=data)
                else:
                    return render_template('AdminProfile.html',data1="No data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/show_admins')
def show_admins():
    cur = getdbcur()
    sql="select * from admindata"
    cur.execute(sql)
    n=cur.rowcount
    if(n>0):
        data=cur.fetchall()
        return render_template('ShowAdmins.html',kota=data)
    else:
        msg="No data found"
        return render_template('ShowAdmins.html',jpr=msg)


@app.route('/show_hospitals')
def show_hospitals():
    cur = getdbcur()
    sql="select * from hospital_data"
    cur.execute(sql)
    n=cur.rowcount
    if(n>0):
        data=cur.fetchall()
        return render_template('ShowHospitals.html',kota=data)
    else:
        msg="No data found"
        return render_template('ShowHospitals.html',jpr=msg)

@app.route('/edit_hospital',methods=['GET','POST'])
def edit_hospital():
    if(request.method=='POST'):
        email=request.form['H1']
        cur = getdbcur()
        sql = "select * from hospital_data where email='"+email+"'"

        cur.execute(sql)
        n = cur.rowcount
        if (n == 1):
            data = cur.fetchone()
            return render_template('EditHospital.html', kota=data)
        else:
            msg = "No data found"
            return render_template('EditHospital.html', jpr=msg)
    else:
        return redirect(url_for('show_hospitals'))

@app.route('/edit_hospital_1',methods=['GET','POST'])
def edit_hospital_1():
    if(request.method=='POST'):
        #college the form data
        name=request.form['T1']
        sp=request.form['T2']
        address=request.form['T3']
        contact=request.form['T4']
        ac=request.form['T5']
        nonac=request.form['T6']
        email=request.form['T7']

        cur = getdbcur()

        sql="update hospital_data set name='"+name+"',speciality='"+sp+"',address='"+address+"',contact='"+contact+"',ac_beds='"+ac+"',non_ac_beds='"+nonac+"'  where email='"+email+"'"

        cur.execute(sql)
        n=cur.rowcount
        if n>0:
            return render_template('EditHospital1.html',msg="Data Saved")
        else:
            return render_template('EditHospital1.html', msg="Data not Saved")
    else:
        return redirect(url_for('show_hospitals'))

@app.route('/auth_error')
def auth_error():
    return render_template('AuthorizationError.html')

@app.route('/admin_home')
def admin_home():
    #check the session
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            return render_template('AdminHome.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/hospital_home')
def hospital_home():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='hospital':
            return render_template('HospitalHome.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['T1']
        password=request.form['T2']
        conn = pymysql.connect(passwd='', host='localhost', user='root', port=3306, db='b299', autocommit=True)
        cur = conn.cursor()

        sql = "select * from logindata where email='"+email+"' AND password='"+password+"'"

        cur.execute(sql)
        n = cur.rowcount
        if n==1:    #Correct email and password
            #fetch usertype
            data=cur.fetchone()
            utype=data[2]
            #create session
            session['email']=email
            session['usertype']=utype
            #send to page
            if utype=='admin':
                return redirect(url_for('admin_home'))
            elif utype=='hospital':
                return redirect(url_for('hospital_home'))
        else:
            return render_template('Login.html',msg="Incorrect email or password")
    else:
        return render_template('Login.html')

@app.route('/logout')
def logout():
    #check the session and remove it
    if 'usertype' in session:
        session.pop('email',None)
        session.pop('usertype',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/change_password_admin',methods=['GET','POST'])
def change_password_admin():
    if 'usertype' in session:
        ut=session['usertype']
        e1=session['email']
        if ut=='admin':
            if request.method=='POST':
                oldpass=request.form['T1']
                newpass=request.form['T2']
                cur=getdbcur()
                sql="update logindata set password='"+newpass+"' where email='"+e1+"' AND password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                msg="Old password is incorrect"
                if n==1:
                    msg="New password set successfully"
                return render_template('ChangePasswordAdmin.html',data=msg)
            else:
                return render_template('ChangePasswordAdmin.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

if __name__=='__main__':
    app.run(debug=True)