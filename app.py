import mysql.connector as mysql
import pandas as pd
import time
from datetime import datetime
from PIL import Image
import json
import base64
import yagmail
import re
from re import search
# import smtplib
 
import streamlit as st
import streamlit.components.v1 as components
from streamlit import caching
 
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from mysql.connector.constants import ClientFlag
from uuid import uuid4
 
st.set_page_config(
    page_title="Admission Form",
    page_icon=":sunny:",
    # layout="wide",
    initial_sidebar_state="expanded",
)
# database localhost connection
# @st.cache()
def get_database_connection():
    db = mysql.connect(host = "localhost",
                      user = "root",
                      passwd = "root",
                      database = "admissiondb",
                      auth_plugin='mysql_native_password')
    cursor = db.cursor()
 
    return cursor, db
 
cursor, db = get_database_connection()
 
cursor.execute("SHOW DATABASES")
 
databases = cursor.fetchall() ## it returns a list of all databases present
 
# st.write(databases)
 
# cursor.execute('''CREATE TABLE ADMISSION (nid varchar(25) PRIMARY KEY,
#                                               sname varchar(255),
#                                               father_name varchar(255),
#                                               mother_name varchar(255),
#                                               address1 varchar(255),
#                                               address2 varchar(255),
#                                               phone varchar(11),
#                                               email varchar(255),
#                                               gender varchar(255),
#                                               date_of_birth date,
#                                               nationality varchar(255),
#                                               r_date date,
#                                               gpa varchar(255),
#                                               religion varchar(255)),
#                                               stat varchar(45)''')
# cursor.execute("show tables from admissiondb")
# tables = cursor.fetchall()
# st.write(tables)

def admin(): #admin panel
    username=st.sidebar.text_input('Username',key='user')
    password=st.sidebar.text_input('Password',type='password',key='pass')
    st.session_state.login=st.sidebar.checkbox('Login')
    if st.session_state.login==True:
        if username=="1" and password=='1':
            st.sidebar.success('Login Success')
            st.subheader('Admin Panel')

            col1,col,col2,col3=st.columns((2,0.2,2,1))
            date1=col1.date_input('Date1')
            col.write('')
            col.write('')
            col.write('')
            col.write('to')
            date2=col2.date_input('Date2')
            col3.write('')
            col3.write('')
            # submit=col3.form_submit_button()
            # if submit:

            cursor.execute(f"select * from admission where r_date between '{date1}' and '{date2}' and stat='In Progress'")
            # db.commit()
            tables =cursor.fetchall()
            size=len(tables)
            st.write(size)
            # st.write(tables)
            j=1
            for i in tables:
                # st.write(i)
                name=i[1]
                father_name=i[2]
                mother_name=i[3]
                gender=i[8]
                phone=i[6]
                email=i[7]
                address1=i[4]
                address2=i[5]
                date_of_birth=i[9]
                nationality=i[10]
                gpa=i[12]
                religion=i[13]
                test=st.expander(f'Student {j}',True)
                with test:
                    j+=1
                    col1,col2=st.columns((2,3))
                    col1.write('Name')
                    col2.write(name)
                    col1.write("Father's Name")
                    col2.write(father_name)
                    col1.write("Mother's Name")
                    col2.write(mother_name)
                    col1.write('Gender')
                    col2.write(gender)
                    col1.write('Contact No.')
                    col2.write(phone)
                    col1.write('Email')
                    col2.write(email)
                    col1.write('Present Address')
                    col2.write(address1)
                    col1.write('Permanent Address')
                    col2.write(address2)
                    col1.write('Date of Birth')
                    col2.write(date_of_birth)
                    col1.write('Nationality')
                    col2.write(nationality)
                    col1.write('GPA')
                    col2.write(gpa)
                    col1.write('Religion')
                    col2.write(religion)
                    Accept=st.button('Accept',key=i[0])
                    if Accept:
                        st.write(i[0])
                        cursor.execute("Update admission set stat='Accepted' where nid='4ef1afb2'")
                        db.commit()
                    Reject=st.button('Reject',key=i[0])
                    if Reject:
                        st.write('WA')
                        cursor.execute(f"Update admission set stat='Rejected' where nid='{i[0]}'")
                        db.commit()



        else:
            st.sidebar.warning('Wrong Credintials')


def form(): #registration form
    st.subheader('Registration form')
    # col1,col2,col3=st.columns((1,5,1))
    nid=uuid4()
    nid=str(nid)[:8]
    with st.form(key='member form'):
        sname=st.text_input('Student Name')
        father_name=st.text_input("Father's Name")
        mother_name=st.text_input("Mother's Name")
        address1=st.text_input('Present Address')
        address2=st.text_input('Permanent Address')
        phone=st.text_input('Mobile Number')
        email=st.text_input('Email')
        gender=st.selectbox('Gender',('Male','Female','Other'))
        date_of_birth=st.date_input('Date of Birth')
        nationality=st.text_input('Nationality')
        r_date=st.date_input('Registration Date')
        gpa=st.text_input('GPA')
        religion=st.selectbox('Religion',('','Islam','Hinduism','Christianity','other'))

        if st.form_submit_button('Submit'):
            query = f'''INSERT INTO ADMISSION (nid,sname,father_name,mother_name,address1,address2,phone,email,
                                                gender,date_of_birth,nationality,r_date,gpa,religion) VALUES ('{nid}','{sname}',
                                                 '{father_name}','{mother_name}','{address1}','{address2}','{phone}','{email}',
                                                '{gender}','{date_of_birth}','{nationality}','{r_date}','{gpa}','{religion}')'''
            s=True
            cursor.execute(query)
            db.commit()
            st.success(f'Congratulation *{sname}*! You have successfully Registered')
            st.write('')
            col1,col2=st.columns((5,2))
            col1.info('You can Check your information From Check Information panel by using this code.You should save this code for further Uses.')
            col2.code(nid)
            st.warning("Please Store this code!!!")
        
def info():
    st.subheader('Information Panel')

    with st.form(key='info form'):
        col1,col2=st.columns((4,2))
        nid=col1.text_input('Your Code')
        col2.write('')
        col2.write('')
        Submit=col2.form_submit_button(label='Search')

    if Submit:
        if nid=='':
            st.warning('Please inseart data')
        else:
            st.success('Your data found')
            cursor.execute(f"select * from admission where nid='{nid}'")
            tables = cursor.fetchall()
            st.subheader('Result')
            st.write(tables)


def stat():
    st.subheader('Check Status')
    nid=st.text_input('Your Id')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select stat from admission where nid='{nid}'")
        table=cursor.fetchall()
        st.write(table)



def main():
    # col1,col2,col3=st.columns((1,5,1))
    st.title('Diploma in Data Science Admission Portal')
    st.subheader('International Islamic University Chittagong')
    st.error('Updated version Coming Soon!!!')
    # st.sidebar.write('Menu')
    selected=st.sidebar.selectbox('Menu',
                        ('Select...',
                        'Admin Panel',
                        'Registration Form',
                        'Check Information',
                        'Check Status'
                        ))
    if selected=='Admin Panel':
        admin()
    elif selected=='Registration Form':
        form()
    elif selected=='Check Information':
        info()
    elif selected=='Check Status':
        stat()
if __name__=='__main__':
    main()