#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 10:41:48 2021

@author: admin

This script automatically approves the evaluation requests pending approval in
CSIS

"""
#!/usr/bin/env python
# coding: utf-8


# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select 
from re import sub
from decimal import Decimal
import gspread
import gspread_formatting
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time

import tkinter as tk
from tkinter import simpledialog
from datetime import date 



# In[6]:


def login_to_csis(username, password):
    url = 'https://www.conceptsis.com/Login.aspx'
    driver.get(url)
    try:
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.NAME,"tbxUserName")))
        user_elem = driver.find_element_by_name("tbxUserName")
        user_elem.clear()
        user_elem.send_keys(username)
        pass_elem = driver.find_element_by_name("tbxPassword")
        pass_elem.clear()
        pass_elem.send_keys(password)
        button_elem = driver.find_element_by_name("btnSubmit")
        button_elem.click()
    except:
        print('Error: Site can not be loaded or The HTML name fields have changed in the ConceptSIS login interface.')
        return False

    return True


# In[8]:
def locate_approve_button():
    try:  
            WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.XPATH,"//*[@id='ctl00_ctl00_c_c_ctl00_rgRequest_ctl00__0']/td[11]/a")))
            link = driver.find_element_by_xpath("//*[@id='ctl00_ctl00_c_c_ctl00_rgRequest_ctl00__0']/td[11]/a")
    except: 
            return None
    return link        

# In[11]:
    
def process_request_type(req):
    product = driver.find_element_by_id('ctl00_ctl00_c_c_ctl00_rgRequest_ctl00_ctl02_ctl02_FilterTextBox_FormName')
    product.send_keys(req+'\n')
      
      # Make sure the page is refreshed before looking for the ID of first purchase request
    time.sleep(3)
      
    #link = True
    link=locate_approve_button()
       
    while  link!=None :  
    # Loop through all the purchase requests
              
          link.click()
          WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,"pm"))) 
          WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID,'ctl00_c_ctl00_btnApprove')))
          driver.find_element_by_id('ctl00_c_ctl00_btnApprove').click()
          time.sleep(3)
          driver.switch_to.default_content()
          link=locate_approve_button()
          if link==None:
              break;
              
    product = driver.find_element_by_id('ctl00_ctl00_c_c_ctl00_rgRequest_ctl00_ctl02_ctl02_FilterTextBox_FormName')
    product.clear()
  

# In[7]:

def approve_request():
    
   # Approve purchase request
    url = 'https://www.conceptsis.com/eForms/PageManager.aspx?uc=ProcessRequest'
    driver.get(url)
    
    req = "Purchase Request"
    while(len(req)):
        process_request_type(req)
        req = get_type(req)
    return

# In[12]:

def get_type(req):

    ROOT = tk.Tk()
    ROOT.withdraw()
    try:
        req_type = simpledialog.askstring(title="Request Type", prompt="Request Type to Process ie -\'Purchase Request\'", initialvalue=req)
    except:
        return ""
    return req_type


# In[12]:


def get_username():

    ROOT = tk.Tk()
    ROOT.withdraw()
    username = simpledialog.askstring(title="Knight's Rewards", prompt="ConceptSIS Username")
    
    return username


# In[13]:


def get_password():

    ROOT = tk.Tk()
    ROOT.withdraw()
    password = simpledialog.askstring(title="Knight's Rewards", prompt="ConceptSIS Password")
    
    return password


# In[14]:


def main(): 

    if not login_to_csis(username, password):
        return False        
    approve_request()
    

# In[15]:

# Get ConceptSIS username and password
username = get_username()
password = get_password()

# you can ask for the username or enter yours here so you don't have to enter it everytime
# make sure you don't share this file with anyone if you enter your password here
#username="XXXXX"
#password="XXXXX"

if(len(username)>0)and(len(password)>0):
    
    # Fire up the driver 
    driver = webdriver.Chrome('/Users/admin/applications/chromedriver')

    # Do everything
    main()
    
    # Close the driver
    driver.close()

else:
    print('Error: Username or Password not entered')



