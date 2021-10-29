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
import yaml
 
st.set_page_config(
    page_title="Admission Form",
    page_icon=":sunny:",
    # layout="wide",
    initial_sidebar_state="expanded",
)
# database localhost connection
# @st.cache()



with open('credintials.yml', 'r') as f:
    credintials = yaml.load(f, Loader=yaml.FullLoader)
    db_credintials = credintials['db']
    system_pass = credintials['system_pass']['admin']
    # email_sender = credintials['email_sender']


def get_database_connection():
    db = mysql.connect(host = db_credintials['host'],
                      user = db_credintials['user'],
                      passwd = db_credintials['passwd'],
                      database = db_credintials['database'],
                      auth_plugin= db_credintials['auth_plugin'])
    cursor = db.cursor()

    return cursor, db
# def get_database_connection():
#     db = mysql.connect(host = "remotemysql.com",
#                       user = "ivei3muPgO",
#                       passwd = "hyVJXcs55s",
#                       database = "ivei3muPgO",
#                       auth_plugin='mysql_native_password')
#     cursor = db.cursor()
 
#     return cursor, db
 
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
#                                               religion varchar(255),
#                                               stat varchar(45)''')
# cursor.execute("Select * from admission")
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
            st.subheader(f'Result Found : {size}')
            # st.write(tables)
            j=1
            for i in tables:
                # st.write(i)
                test=st.expander(f'Student {j}',True)
                with test:
                    j+=1
                    col1,col2=st.columns((2,3))
                    col1.write('Name')
                    col2.write(i[1])
                    col1.write("Father's Name")
                    col2.write(i[2])
                    col1.write("Mother's Name")
                    col2.write(i[3])
                    col1.write('Gender')
                    col2.write(i[8])
                    col1.write('Contact No.')
                    col2.write(i[6])
                    col1.write('Email')
                    col2.write(i[7])
                    col1.write('Present Address')
                    col2.write(i[4])
                    col1.write('Permanent Address')
                    col2.write(i[5])
                    col1.write('Date of Birth')
                    col2.write(i[9])
                    col1.write('Nationality')
                    col2.write(i[10])
                    col1.write('GPA')
                    col2.write(i[12])
                    col1.write('Religion')
                    col2.write(i[13])
                    Accept=st.button('Accept',key=i[0])
                    if Accept:
                        st.write('Accepted')
                        cursor.execute(f"Update admission set stat='Accepted' where nid='{i[0]}'")
                        db.commit()
                    Reject=st.button('Reject',key=i[0])
                    if Reject:
                        st.write('Rejected')
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
            col1.info('You can Check your information From Check Information panel by using this code.You should save this code for further Uses.You can Check your status from Check status menu.')
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
            for i in tables:
                # st.write(i)
                test=st.expander(f'Your Details',True)
                with test:
                    col1,col2=st.columns((2,3))
                    col1.write('ID')
                    col2.write(i[0])
                    col1.write('Name')
                    col2.write(i[1])
                    col1.write("Father's Name")
                    col2.write(i[2])
                    col1.write("Mother's Name")
                    col2.write(i[3])
                    col1.write('Gender')
                    col2.write(i[8])
                    col1.write('Contact No.')
                    col2.write(i[6])
                    col1.write('Email')
                    col2.write(i[7])
                    col1.write('Present Address')
                    col2.write(i[4])
                    col1.write('Permanent Address')
                    col2.write(i[5])
                    col1.write('Date of Birth')
                    col2.write(i[9])
                    col1.write('Nationality')
                    col2.write(i[10])
                    col1.write('GPA')
                    col2.write(i[12])
                    col1.write('Religion')
                    col2.write(i[13])
                    col1.write('Registered Date:')
                    col2.write(i[11])
            # st.write(tables)


def stat():
    st.subheader('Check Status')
    nid=st.text_input('Your Id')
    submit=st.button('Search',key='sub')
    if submit:
        cursor.execute(f"Select sname,stat from admission where nid='{nid}'")
        table=cursor.fetchall()
        with st.expander("",True):
            for i in table:
                col1,col2=st.columns((2,3))
                col1.write('Name')
                col2.write(i[0])
                col1.write("Status")
                if i[1]=='In Progress':
                    col2.warning(i[1])
                elif i[1]=='Accepted':
                    col2.success(i[1])
                    st.balloons()
                else:
                    col2.error(i[1])



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