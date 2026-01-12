from flask import Flask, render_template, request, session, redirect,url_for, jsonify
from werkzeug.utils import secure_filename


from MyLib import *
import time
import os
import json
from datetime import datetime

app=Flask(__name__)


app.secret_key="super secret key"
app.config['UPLOAD_FOLDER']='./static/photos'
app.config['UPLOAD_FOLDER1']='./static/item_photos'
#Home
@app.route('/')
def home():
    return render_template('home.html')


#Edit Profile admin
@app.route("/admin_profile",methods=["GET","POST"])
def admin_profile():
    if  "usertype" in session :
        e1 = session["email"]
        ut = session["usertype"]
        if  ut == "admin" :
            photo = check_photo(e1)
            cur = create_connection()
            sql = "select * from admin_data where email='" + e1 + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n == 1 :
                data = cur.fetchone()
                return render_template("admin_profile.html", data=data,photo=photo)
            else:
                return render_template("admin_profile.html", msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/admin_profile1",methods=["GET","POST"])
def admin_profile1():
    if "usertype" in session :
        e1 = session["email"]
        ut = session["usertype"]
        if ut == "admin" :
            if request.method=="POST" :
                cur = create_connection()
                name=request.form["T1"]
                address=request.form["T2"]
                contact=request.form["T3"]
                sql = "update admin_data set name='"+name+"',address='"+address+"',contact='"+contact+"' where email='" + e1 + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1 :
                    return render_template("admin_profile1.html", msg="Data changes are saved")
                else:
                    return render_template("admin_profile1.html", msg="No data saved")
            else:
                return render_template("admin_profile1.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Registration
@app.route('/admin_reg',methods=["GET","POST"])
def admin_reg():
    if "usertype" in session:
        ut=session["usertype"]
        if ut=="admin":
            if request.method == "GET":
                print("This is GET request from admin")
                return render_template('admin_reg.html')
            else:
                print("This is POST request from admin")
                #recieve data from html
                name = request.form['t1']
                address = request.form['t2']
                contact = request.form['t3']
                email = request.form['t4']
                password = request.form['t5']
                cpass = request.form['t6']
                usertype = "admin"
                if  password == cpass :
                    cur = create_connection()
                    s1 = "insert into admin_data values('" + name + "','" + address + "','" + contact + "','" + email + "')"
                    s2 = "insert into login_data values('" + email + "','" + password + "','" + usertype + "')"
                    cur.execute(s1)
                    m = cur.rowcount
                    cur.execute(s2)
                    n = cur.rowcount
                    if m == 1 and n == 1 :
                        msg = "Data saved and login created"
                    elif m == 1 :
                        msg = "only data is saved"
                    elif n == 1 :
                        msg = "only login created"
                    else:
                        msg = "no data found"
                else:
                    msg = "ERROR:Password does not matched"
            return render_template('admin_reg.html', kota=msg)

        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/student_reg_admin',methods=["GET","POST"])
def student_reg_admin():
    if "usertype" in session:
        ut=session["usertype"]
        if ut == "admin":
            if request.method == "GET":
                print("This is GET request from admin")
                return render_template('student_reg_admin.html')
            else:
                print("This is POST request from admin")
                #recieve data from html

                name = request.form['t2']
                gender = request.form['t3']
                address = request.form['t6']
                contact = request.form['t7']
                email = request.form['t9']
                password = request.form['t10']
                cpassword = request.form['t11']
                usertype = "user"
                if password==cpassword:

                    cur = create_connection()
                    s1 = "insert into user_data values(0,'" + name + "','" + gender + "','" + address + "','" + contact + "','" + email + "',0) "
                    s2 = "insert into login_data values('" + email + "','" + password + "','" + usertype + "')"
                    cur.execute(s1)
                    n = cur.rowcount
                    cur.execute(s2)
                    m= cur.rowcount
                    if n == 1 and m==1:
                        return render_template('student_reg_admin.html', kota="Data Saved and Login Created", email=email)
                    elif n==1:
                        return render_template('student_reg_admin.html', kota="Only Data Saved", email=email)
                    elif m==1:
                        return render_template('student_reg_admin.html', kota="Only Login Created", email=email)
                    else:
                        return render_template('student_reg_admin.html', kota="No Data Found", email=email)
                else:
                    return render_template('student_reg_admin.html',kota="Password Does Not Matched")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

#Change Password
@app.route("/change_password",methods=["GET","POST"])
def change_password():
    if "usertype" in session:
        e1=session["email"]
        ut=session["usertype"]
        if ut=="admin":
            if request.method=="POST" :
                old_pass=request.form["T1"]
                new_pass=request.form["T2"]
                confirm=request.form["T3"]
                if confirm==new_pass :
                    cur=create_connection()
                    sql="update login_data set password='"+new_pass+"' where email='"+e1+"' AND password='"+old_pass+"'"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1 :
                        msg="Password changed successfully"
                    else:
                        msg="Incorrect old password"
                else:
                    msg="New password and confirm password should be same"
                return render_template("change_pass_admin.html",msg=msg)
            else:
                return render_template("change_pass_admin.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Show All Data
@app.route("/show_admins")
def show_admins():
    if  "usertype" in session :

        ut = session["usertype"]
        if  ut == "admin" :
            cur=create_connection()
            sql="select * from admin_data"
            cur.execute(sql)
            n=cur.rowcount
            if n>0:
                data=cur.fetchall()
                return  render_template("show_admins.html",abc=data)
            else:
                return render_template("show_admins.html",msg="no data found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return render_template("auth_error.html",msg="contact to admin")

@app.route('/show_students')
def show_students():
    if  "usertype" in session :
        ut = session["usertype"]
        if  ut == "admin" :
            cur=create_connection()
            sql1 = "select st_id,name,contact,email from user_data ORDER BY st_id"
            cur.execute(sql1)
            n = cur.rowcount
            if n>0:
                data = cur.fetchall()
                return render_template("show_students.html", result=data)
            else:
                return render_template("show_students.html", msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Update

@app.route('/update_student',methods=["GET","POST"])
def update_student():
    if "usertype" in session:
        ut=session["usertype"]
        if ut== "admin":
            if request.method=="POST":
                cur=create_connection()
                e1=request.form['t1']
                sql = "select * from user_data where email='"+e1+"'"
                cur.execute(sql)
                n = cur.rowcount
                if n==1 :
                    d=cur.fetchone()
                    return render_template('update_student.html',data=d,email=e1)
                else:
                    return render_template('update_student.html',msg="no data found",email=e1)
            else:
                return render_template('update_student.html')
        else:
           return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route('/update_student1',methods=["GET","POST"])
def update_student1():
    if  request.method == "POST" :
        cur=create_connection()
        reg= request.form['t1']
        name = request.form['t2']
        address = request.form['t6']
        contact = request.form['t7']
        email= request.form['t9']
        sql = "update user_data set name='"+name+"',address='"+address+"',contact='"+contact+"' where email='"+email+"'"
        cur.execute(sql)
        n = cur.rowcount
        if  n == 1 :
            return render_template("update_student.html",msg="updated successfully",email=email,reg=reg)
        else:
            return render_template("update_student.html",msg="no change found",email=email,reg=reg)
    else:
        return render_template("update_student.html")

#Delete
@app.route('/delete_admin',methods=["GET","POST"])
def delete_admin():
    if request.method=="POST" :
            cur=create_connection()
            e2 = request.form["H1"]
            sql = "delete from admin_data where email='"+e2+"'"
            cur.execute(sql)
            n = cur.rowcount
            sql2 = "delete from login_data where email='" + e2 + "'"
            cur.execute(sql2)
            m = cur.rowcount

            if n==1 and m==1 :
                return render_template('home.html', msg="data deleted successfully")
            else:
                return render_template('admin_profile.html', msg="data not deleted")
    else:
        return render_template('admin_profile.html')

@app.route('/delete_student',methods=["GET","POST"])
def delete_student():
    if "usertype" in session:
        ut=session["usertype"]
        if ut=="admin":
            if request.method=="POST" :

                    cur=create_connection()
                    e2 = request.form["del1"]
                    st_id= request.form["del2"]
                    photo = check_photo(e2)

                    sql1 = "delete from user_data where email='"+e2+"'"
                    cur.execute(sql1)
                    n = cur.rowcount

                    sql2 = "delete from photo_data where email='" + e2 + "'"
                    cur.execute(sql2)
                    m= cur.rowcount

                    sql4 = "delete from login_data where email='" + e2 + "'"
                    cur.execute(sql4)
                    p = cur.rowcount

                    if n==1 and m==1 and p==1:
                        os.remove("./static/photos/"+photo)
                        return render_template('delete_student.html', msg="All Data Deleted successfully",email=e2)
                    elif n==1 :
                        return render_template('delete_student.html', msg="Student General Details Deleted",email=e2)
                    else:
                        return render_template('delete_student.html', msg="data not deleted",email=e2)
            else:
                return render_template('delete_student.html')
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Upload Profile Photo
@app.route('/upload_admin_photo',methods=['GET','POST'])
def upload_admin_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            if request.method == 'POST':
                file = request.files['F1']
                print(file)
                if file:
                    path = os.path.basename(file.filename) #removes the folder name and keeps only the file name
                    file_ext = os.path.splitext(path)[1][1:]
                    filename = str(int(time.time())) + '.' + file_ext
                    filename = secure_filename(filename)
                    cur = create_connection()

                    sql = "insert into photo_data values('" + email + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n == 1 :
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('upload_admin_photo.html',result="Success")
                        else:
                            return render_template('upload_admin_photo.html',result="Failure")
                    except:
                        return render_template('upload_admin_photo.html',result="Duplicate")
                else:
                    return render_template('upload_admin_photo.html',result="Error !! , No File found")
            else:
                return render_template('upload_admin_photo.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/upload_student_photo',methods=['GET','POST'])
def upload_student_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        if usertype=="admin":
            if request.method == 'POST':
                file = request.files['F1']
                email=request.form["T1"]
                st_no = request.form["T3"]
                print(file)
                if file:

                    path = os.path.basename(file.filename) #removes the folder name and keeps only the file name
                    file_ext = os.path.splitext(path)[1][1:] #extention split and remove another part
                    filename = str(int(time.time())) + '.' + file_ext # after time() function use in current time
                    filename = secure_filename(filename)
                    cur = create_connection()


                    sql = "insert into photo_data values('" + email + "','" + filename + "')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if n == 1 :
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template('upload_student_photo_admin.html',msg="Photo Uploaded",email=email,st_no=st_no)
                        else:
                            return render_template('upload_student_photo_admin.html',msg="Failure",email=email,st_no=st_no)
                    except:
                        return render_template('upload_student_photo_admin.html',msg="Duplicate",email=email,st_no=st_no)
                else:
                    return render_template('upload_student_photo_admin.html',msg="Error!!",email=email,st_no=st_no)
            else:
                return render_template('upload_student_photo_admin.html')

        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/upload_item_photo', methods=['POST'])
def upload_item_photo():
    if 'usertype' in session and session['usertype'] == "admin":
        file = request.files['F1']
        id = request.form['id']
        if file and id:
            ext = os.path.splitext(file.filename)[1]
            filename = secure_filename(str(int(time.time())) + ext)
            cur = create_connection()
            cur.execute("UPDATE food_category SET photo=%s WHERE id=%s", (filename, id))
            if cur.rowcount == 1:
                file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
                msg = "Photo Uploaded"
            else:
                msg = "Upload failed"
            # Fetch updated data for displaying after upload
            cur.execute("SELECT id, name, price, type, photo FROM food_category WHERE id=%s", (id,))
            data = cur.fetchone()
            photo = check_item_photo(id)
            return render_template('edit_item.html', msg=msg, data=data, photo=photo)
        else:
            return render_template('edit_item.html', msg="Missing Photo or ID")
    else:
        return redirect(url_for('auth_error'))

#Delete Profile Photo
@app.route('/delete_admin_photo')
def delete_admin_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        email=session['email']
        if usertype=='admin':
            photo = check_photo(email)
            cur = create_connection()
            sql = "delete from photo_data where email='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n==1:
                os.remove("./static/photos/"+photo)
                return render_template("delete_admin_photo.html",msg="photo deleted successfully")
            else:
                return render_template("delete_admin_photo.html", msg="photo not deleted")
        else:
            return render_template("delete_admin_photo.html", msg="contact to admin")
    else:
        return redirect(url_for('auth_error'))

@app.route('/delete_student_photo',methods=["GET","POST"])
def delete_student_photo():
    if 'usertype' in session:
        usertype=session['usertype']
        if usertype=="admin":
            if request.method=="POST":
                cur = create_connection()
                email = request.form["T2"]
                st_no = request.form["T3"]

                photo = check_photo(email)
                sql = "delete from photo_data where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount

                if n == 1:
                    os.remove("./static/photos/" + photo)
                    return render_template("delete_student_photo_admin.html", msg="photo deleted successfully",email=email,st_no=st_no)
                else:
                    return render_template("delete_student_photo_admin.html", msg="photo not deleted",email=email,st_no=st_no)
            else:
                return render_template("delete_student_photo_admin.html")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/delete_item_photo', methods=['POST'])
def delete_item_photo():
    id = request.form['id']
    cur = create_connection()
    # Remove photo file from disk and set photo field to None or 'nophoto'
    cur.execute("SELECT photo FROM food_category WHERE id=%s", (id,))
    row = cur.fetchone()
    if row and row[0]:
        # Remove file if it exists
        filepath = os.path.join(app.config['UPLOAD_FOLDER1'], row[0])
        if os.path.exists(filepath):
            os.remove(filepath)
    cur.execute("UPDATE food_category SET photo=%s WHERE id=%s", ('nophoto', id))
    # Optionally, fetch the rest of the item data to re-render the template
    cur.execute("SELECT id, name, price, type, photo FROM food_category WHERE id=%s", (id,))
    data = cur.fetchone()
    photo = check_item_photo(id)
    return render_template("edit_item.html", msg="Photo deleted", data=data, photo=photo)

#add wallet points
@app.route('/add_points',methods=["GET","POST"])
def add_points():
    if "usertype" in session:
        ut = session["usertype"]
        if ut == "admin":
            if request.method == "POST":
                current_date = datetime.now().strftime("%y-%m-%d")
                user_id = request.form['C1']
                email = request.form['C2']
                return render_template('add_points.html',email=email,id=user_id,date=current_date)
            else:
                return render_template('add_points.html',msg="Error Found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/add_points1',methods=["GET","POST"])
def add_points1():
    if "usertype" in session:
        ut = session["usertype"]
        if ut == "admin":
            if request.method == "POST":
                current_date = request.form['date']
                user_id = request.form['id']
                email =request.form['email']
                points=request.form['points']
                cur=create_connection()
                sql="insert into transactions_history values(0,'" + current_date + "','" + email + "','" +points + "','" +user_id + "')"
                cur.execute(sql)
                n = cur.rowcount
                if n==1:
                    return render_template('add_points1.html',email=email,id=user_id,msg="Points added successfully")
                else:
                    return render_template('add_points1.html',msg="Points not added")
            else:
                return render_template('add_points.html',msg="Error Found")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

#user profile
@app.route('/student_profile_admin', methods=["GET", "POST"])
def student_profile_admin():
    if "usertype" in session:
        ut = session["usertype"]
        if ut == "admin":
            if request.method == "POST":
                cur = create_connection()
                email = request.form['t1']
                photo = check_photo(email)
                sql = "select * from user_data where email='" + email + "'"
                cur.execute(sql)
                n = cur.rowcount
                if n == 1:
                    data = cur.fetchone()
                    id=request.form['t2']
                    sql1 = "SELECT pt_id, date, email, amount FROM transactions_history WHERE st_id='"+id+"'"
                    cur.execute(sql1)
                    points = cur.fetchall()
                    return render_template("student_profile_admin.html",data=data,photo=photo,email=email,points=points)
                else:
                    return render_template("student_profile_admin.html", msg="No data found")
            else:
                return render_template("student_profile_admin.html")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

# crud menu items
@app.route('/add_items',methods=["GET","POST"])
def add_items():
    if "usertype" in session:
        ut=session["usertype"]
        if ut=="admin":
            if request.method == "GET":
                return render_template('add_items.html')
            else:
                name=request.form['name']
                price=request.form['price']
                type=request.form['type']
                cur = create_connection()
                sql = "INSERT INTO food_category (name, price, type) VALUES (%s, %s, %s)"
                cur.execute(sql, (name, price, type))
                n = cur.rowcount
                if n==1:
                    return render_template('add_items.html' ,msg="item added successfully")
                else:
                    return render_template('add_items.html',msg="item not added")
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/show_items')
def show_items():
    if  "usertype" in session :
        ut = session["usertype"]
        if  ut == "admin" :
            cur=create_connection()
            sql1 = "select * from food_category ORDER BY id"
            cur.execute(sql1)
            n = cur.rowcount
            if n>0:
                data = cur.fetchall()
                return render_template("show_items.html", menu_items=data)
            else:
                return render_template("show_items.html", msg="No data found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route('/edit_item', methods=["GET", "POST"])
def edit_item():
    if "usertype" in session:
        ut = session["usertype"]
        if ut == "admin":
            if request.method == "POST":
                cur = create_connection()
                id = request.form['id']
                photo = check_item_photo(id)
                cur.execute("SELECT id, name, price, type, photo, availability FROM food_category WHERE id=%s", (id,))
                data = cur.fetchone()
                if data:
                    return render_template("edit_item.html", data=data, photo=photo)
                else:
                    return render_template("edit_item.html", msg="No data found")
            else:
                return render_template("show_items.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route("/add_item1", methods=["POST"])
def add_item1():
    if "usertype" not in session or session["usertype"] != "admin":
        return redirect(url_for("auth_error"))

    item_id      = request.form.get("id")
    name         = request.form.get("name")
    price        = request.form.get("price")
    item_type    = request.form.get("type")
    availability = request.form.get("availability")   # NEW

    cur = create_connection()
    try:
        cur.execute(
            """
            UPDATE food_category
            SET name=%s,
                price=%s,
                type=%s,
                availability=%s
            WHERE id=%s
            """,
            (name, price, item_type, availability, item_id)
        )
        cur.connection.commit()
    except Exception as e:
        print("add_item1 error:", e)
        msg = "Error while updating item."
    else:
        msg = "Item updated successfully."
    finally:
        cur.close()

    # Re-fetch data to show updated values on edit page
    cur = create_connection()
    cur.execute("SELECT id, name, price, type, photo, availability FROM food_category WHERE id=%s", (item_id,))
    data = cur.fetchone()
    cur.close()

    photo = check_item_photo(item_id)
    return render_template("edit_item.html", data=data, photo=photo, msg=msg)

@app.route('/delete_item',methods=["GET","POST"])
def delete_item():
    if  "usertype" in session :
        ut = session["usertype"]
        if  ut == "admin" :
            if request.method=="POST":
                cur=create_connection()
                id=request.form['id']
                sql1 = "DELETE FROM food_category WHERE id='"+id+"'"
                cur.execute(sql1)
                n = cur.rowcount
                if n==1:
                    data = cur.fetchone()
                    return render_template("delete_item.html", msg="Item data has been deleted")
                else:
                    return render_template("delete_item.html", msg="No data found")
            else:
                return render_template("delete_item.html",msg="contact to admin")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

@app.route('/transaction_history')
def transaction_history():
    if "usertype" not in session or session["usertype"] != "admin":
        return redirect(url_for("auth_error"))

    cur = create_connection()
    try:
        cur.execute("SELECT * FROM transactions_history")
        transactions = cur.fetchall()
    finally:
        cur.close()

    return render_template('transactions.html', transactions=transactions)

@app.route("/my_profile")
def my_profile():
    if "usertype" not in session or session["usertype"] != "user":
        return redirect(url_for("auth_error"))

    email = session["email"]

    cur = create_connection()
    try:
        # user details + photo filename from photo_data
        cur.execute(
            """
            SELECT u.st_id, u.name, u.gender, u.address, u.contact,
                   u.email, u.balance, p.photo
            FROM user_data AS u
            LEFT JOIN photo_data AS p ON u.email = p.email
            WHERE u.email = %s
            """,
            (email,)
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if not row:
        user = None
    else:
        user = {
            "st_id": row[0],
            "name": row[1],
            "gender": row[2],
            "address": row[3],
            "contact": row[4],
            "email": row[5],
            "balance": row[6],
            "photo": row[7],  # e.g. "1765253374.jpg"
        }

    return render_template("my_profile.html", user=user, user_name=user["name"] if user else None)


@app.route("/my_orders")
def my_orders():
    if "usertype" not in session or session["usertype"] != "user":
        return redirect(url_for("auth_error"))

    user_email = session["email"]
    username=fetch_studnet_name(user_email)

    cur = create_connection()
    try:
        # 1) email se st_id lo
        cur.execute("SELECT st_id, name FROM user_data WHERE email=%s", (user_email,))
        row = cur.fetchone()
        if not row:
            cur.close()
            return render_template("my_orders.html", orders=[], student=None,  username=username)

        st_id, name = row[0], row[1]

        # 2) is student ke saare orders (latest first) + date/time
        cur.execute(
            """
            SELECT order_id,
                   food_name,
                   quantity,
                   total_price,
                   type,
                   status,
                   order_datetime
            FROM order_data
            WHERE st_id = %s
            ORDER BY order_id DESC
            """,
            (st_id,)
        )
        orders = cur.fetchall()
    finally:
        cur.close()

    student = {"st_id": st_id, "name": name, "email": user_email}
    return render_template("my_orders.html", orders=orders, student=student,id=st_id,username=username)

#login System with Security
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["T1"]
        password = request.form["T2"]

        cur = create_connection()
        # IMPORTANT: parametrized query
        cur.execute(
            "SELECT email, password, usertype FROM login_data WHERE email=%s AND password=%s",
            (email, password)
        )
        data = cur.fetchone()
        cur.close()

        if data:
            ut = data[2]

            # create session
            session["email"] = email
            session["usertype"] = ut
            session["show_welcome"] = True   # <- sirf first user_home ke लिए

            if ut == "admin":
                return redirect(url_for("show_orders"))
            elif ut == "user":
                return redirect(url_for("user_home"))
            else:
                return render_template("login.html", msg="contact to admin")
        else:
            return render_template("login.html", msg="Either email or password is incorrect")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    if "usertype" in session :
        #remove session
        session.pop("email",None)
        session.pop("usertype",None)
        return redirect(url_for("home"))
    else:
        return render_template("home.html")

@app.route('/auth_error')
def auth_error():
    return render_template('auth_error.html')

@app.route('/user_home')
def user_home():
    if "usertype" not in session or session["usertype"] != "user":
        return redirect(url_for("auth_error"))

    user_email = session["email"]
    cur = create_connection()

    cur.execute("SELECT st_id, name FROM user_data WHERE email=%s", (user_email,))
    row = cur.fetchone()
    if not row:
        cur.close()
        return redirect(url_for("auth_error"))

    st_id, user_name = row[0], row[1]

    # food items
    cur.execute("SELECT * FROM food_category")
    food_data = cur.fetchall()

    # cart items
    cur.execute("""
        SELECT item_id, quantity 
        FROM cart_items 
        WHERE user_email = %s
    """, (user_email,))
    cart_items = cur.fetchall()

    cart_dict = {r[0]: r[1] for r in cart_items}

    merged_data = []
    for row in food_data:
        item_id = row[0]
        qty = cart_dict.get(item_id, 0)
        merged_data.append(row + (qty,))

    cur.execute("SELECT COALESCE(SUM(quantity), 0) FROM cart_items WHERE user_email=%s", (user_email,))
    total_qty = cur.fetchone()[0]
    cur.close()

    # session flag → only one time
    show_welcome = session.pop("show_welcome", False)

    return render_template(
        'user_home.html',
        data=merged_data,
        total_qty=total_qty,
        id=st_id,
        user_name=user_name,
        show_welcome=show_welcome
    )

@app.route("/update_cart", methods=["POST"])
def update_cart():
    item_id = request.form["item_id"]
    qty     = int(request.form["quantity"])

    cur = create_connection()
    sql = """
        INSERT INTO cart_items (user_email, item_id, quantity)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE quantity=%s
    """
    cur.execute(sql, (session["email"], item_id, qty, qty))
    cur.commit()

    # total_qty calculate from cart table
    cur.execute("SELECT COALESCE(SUM(quantity),0) FROM cart WHERE user_email=%s",
                (session["email"],))
    total_qty = cur.fetchone()[0]

    return {"total_qty": int(total_qty)}

@app.route("/delete_cart", methods=["POST"])
def delete_cart():
    item_id = request.form["item_id"]

    cur = create_connection()
    # quantity 0 => delete row
    cur.execute("DELETE FROM cart_items WHERE user_email=%s AND item_id=%s",
                (session["email"], item_id))
    cur.commit()

    cur.execute("SELECT COALESCE(SUM(quantity),0) FROM cart WHERE user_email=%s",
                (session["email"],))
    total_qty = cur.fetchone()[0]

    return {"total_qty": int(total_qty)}



@app.route("/cart_summary", methods=["POST", "GET"])
def cart_summary():
    if "usertype" not in session or session["usertype"] != "user":
        return redirect(url_for("auth_error"))

    user_email = session["email"]
    st_id = request.form["st_id"]
    username=fetch_studnet_name(st_id)

    cur = create_connection()
    cur.execute("""
        SELECT c.item_id, f.name, f.price, f.type, f.photo, c.quantity,
               (f.price * c.quantity) AS subtotal
        FROM cart_items c
        JOIN food_category f ON c.item_id = f.id
        WHERE c.user_email = %s
        ORDER BY f.name
    """, (user_email,))
    rows = cur.fetchall()
    cur.close()

    cart_items = []
    total_amount = 0
    for row in rows:
        cart_items.append({
            "item_id":  row[0],
            "name":     row[1],
            "price":    row[2],
            "type":     row[3],
            "photo":    row[4] or "nophoto.png",
            "quantity": row[5],
            "subtotal": row[6],
        })
        total_amount += row[6]

    balance = check_balance(st_id)
    can_place = balance >= total_amount

    return render_template(
        "cart_summary.html",
        cart_items=cart_items,
        total_amount=total_amount,
        id=st_id,
        balance=balance,
        can_place=can_place,
        username=username
    )


@app.route("/order", methods=["POST", "GET"])
def order():
    if "usertype" not in session or session["usertype"] != "user":
        return redirect(url_for('auth_error'))

    if request.method == "POST":
        # Get ALL items as lists
        food_names = request.form.getlist("food_name")
        quantities = request.form.getlist("quantity")
        total_prices = request.form.getlist("total_price")
        types_list = request.form.getlist("type")  # renamed to avoid conflict
        st_ids = request.form.getlist("st_id")

        e1 = session["email"]
        cur = create_connection()

        success_count = 0
        try:
            # Insert EACH cart item
            for i in range(len(food_names)):
                sql1 = """
                    INSERT INTO order_data (food_name, quantity, total_price, type, st_id) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cur.execute(sql1, (
                    food_names[i], quantities[i], total_prices[i],
                    types_list[i], st_ids[i]
                ))
                success_count += cur.rowcount

            # Clear entire cart AFTER all inserts
            cur.execute("DELETE FROM cart_items WHERE user_email = %s", (e1,))
            cur.connection.commit()  # Use connection.commit()

            if success_count > 0:
                return render_template('order.html',
                                       msg=f"✅ {success_count} items ordered successfully!")
            else:
                return render_template('order.html', msg="No items to order")

        except Exception as e:
            print(f"Order error: {e}")
            return render_template('order.html', msg="Order failed, try again")

        finally:
            cur.close()

    return render_template('order.html')

#admin operations

@app.route('/show_orders')
def show_orders():
    if "usertype" not in session or session["usertype"] != "admin":
        return redirect(url_for("auth_error"))

    cur = create_connection()
    cur.execute(
        "SELECT order_id, food_name, quantity, total_price, type, st_id, status, order_datetime "
        "FROM order_data WHERE status='pending' ORDER BY st_id, order_id"
    )
    orders = cur.fetchall()
    grouped_orders = {}
    data = None
    for o in orders:
        st_id = o[5]
        cur.execute("select * from user_data where st_id = %s", (st_id,))
        data = cur.fetchone()
        grouped_orders.setdefault(st_id, []).append(o)
        print(data)
    return render_template('show_orders.html', grouped_orders=grouped_orders, data=data)

#accept or reject orders
@app.route("/update_order_status_form", methods=["POST"])
def update_order_status_form():
    if "usertype" not in session or session["usertype"] != "admin":
        return redirect(url_for("auth_error"))

    order_id = request.form.get("order_id")
    status   = request.form.get("status")        # 'accepted' ya 'rejected'
    anchor   = request.args.get("anchor")        # e.g. st-1 (scroll ke liye)

    if not order_id or status not in ("accepted", "rejected"):
        return redirect(url_for("show_orders"))

    cur = create_connection()   # tumhare project me ye cursor hi return karta hai
    try:
        cur.execute(
            "UPDATE order_data SET status=%s WHERE order_id=%s",
            (status, order_id)
        )
        cur.connection.commit()
    except Exception as e:
        print("update_order_status_form error:", e)
    finally:
        cur.close()

    # Ab status pending nahi raha, isliye next reload me ye row pending list se hat jayegi
    if anchor:
        return redirect(url_for("show_orders") + f"#{anchor}")
    return redirect(url_for("show_orders"))




# Accepted orders history
@app.route('/accepted_orders')
def accepted_orders():
    if "usertype" not in session or session["usertype"] != "admin":
        return redirect(url_for("auth_error"))

    cur = create_connection()
    cur.execute("""
        SELECT order_id,
               food_name,
               quantity,
               total_price,
               type,
               st_id,
               status,
               order_datetime
        FROM order_data
        WHERE status = 'accepted'
        ORDER BY st_id, order_id
    """)
    orders = cur.fetchall()
    cur.close()

    grouped_orders = {}
    for o in orders:
        st_id = o[5]          # st_id index same
        grouped_orders.setdefault(st_id, []).append(o)

    return render_template('accepted_orders.html', grouped_orders=grouped_orders)

# Rejected orders history
@app.route('/rejected_orders')
def rejected_orders():
    if "usertype" not in session or session["usertype"] != "admin":
        return redirect(url_for("auth_error"))

    cur = create_connection()
    cur.execute("""
        SELECT order_id,
               food_name,
               quantity,
               total_price,
               type,
               st_id,
               status,
               order_datetime
        FROM order_data
        WHERE status = 'rejected'
        ORDER BY st_id, order_id
    """)
    orders = cur.fetchall()
    cur.close()

    grouped_orders = {}
    for o in orders:
        st_id = o[5]
        grouped_orders.setdefault(st_id, []).append(o)

    return render_template('rejected_orders.html', grouped_orders=grouped_orders)


@app.route('/menu_list')
def menu_list():
    cur = create_connection()
    # food items
    cur.execute("SELECT * FROM food_category")
    food_data = cur.fetchall()
    cur.close()
    return render_template(
        'menu_list.html',
        data=food_data
    )

if __name__=='__main__':
    app.run(debug=True)