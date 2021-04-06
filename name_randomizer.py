#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import re
import random
import string
import requests
import os
import sqlite3

# In[2]:


def random_string(word):
        termination=random.choice(range(1,len(word)))
        rand_string=word[:termination]
        return(rand_string)

def pass_maker():
    special_characters='!@#$%&'
    chars=random.choices(string.ascii_letters,k=16)
    num=random.choice([1,2,3,4])
    [chars.append(x) for x in random.choices(string.digits,k=num)]
    num=random.choice([1,2,3,4])
    [chars.append(x) for x in random.choices(special_characters,k=num)]
    random.shuffle(chars)
    return(''.join(chars))

def table_maker(db,table_name,value_list):
    curs=db.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS "+table_name+" (id integer PRIMARY KEY,"+table_name+" text)")
    for x in set(value_list):
        #print(x)
        y=list(set(value_list)).index(x)+1
        project=(y,x)
        curs.execute('INSERT INTO '+table_name+'(id, '+table_name+') VALUES(?,?)',project)
        database.commit()

if "fake_id.db" in os.listdir():
    dic={}
    database=sqlite3.connect("fake_id.db")
    curs=database.cursor()
    for table in curs.execute('SELECT name from sqlite_master where type= "table"').fetchall():
        curs.execute('SELECT * FROM {}'.format(table[0]))
        rows = curs.fetchall()
        dic.update({table[0].split('_')[0]:[row[1] for row in rows]})
    database.close()
    print(dic)
        
else:
    print('no stored file found, parsing ssa.gov and mongabay.com for names')
    import requests
    raw_first_names=requests.get('https://www.ssa.gov/oact/babynames/decades/names2010s.html','utf-8')
    first_names=[x.lower() for x in re.findall(r'(?<=<td >).*?(?=</td>)',raw_first_names.text)]

    raw_last_names=requests.get('https://names.mongabay.com/most_common_surnames.htm')
    last_names=[x.lower() for x in re.findall(r'(?<=<tr><td>)[a-zA-Z]{2,20}(?=</td><)',raw_last_names.text)]    

    raw_domains=requests.get('https://github.com/mailcheck/mailcheck/wiki/List-of-Popular-Domains',allow_redirects=False)
    email_domain=[x.lower() for x in re.findall(r'(?<=>")[a-zA-Z].*?\.[a-zA-Z\.].*?(?="<)',raw_domains.text)]    

    #creates db if it doesnt exist
    database=sqlite3.connect("fake_id.db")
    curs=database.cursor()
   
    
    #makes the tables
    curs.execute("CREATE TABLE IF NOT EXISTS first_names (id integer PRIMARY KEY,first_names text)")
    curs.execute("CREATE TABLE IF NOT EXISTS last_names (id integer PRIMARY KEY,last_names text)")
    curs.execute("CREATE TABLE IF NOT EXISTS email_domain (id integer PRIMARY KEY,email_domain text)")
    #saves changes
    database.commit()
    
    dic={'first':first_names,
         'last':last_names,
         'email':email_domain}
    table_maker(database,'first_names',first_names)
    table_maker(database,'last_names',last_names)
    table_maker(database,'email_domain',email_domain)
    database.close()

# In[10]:


class identity:
    
    def __init__(self):

        self.first=random.choice(dic['first']).lower()
        
        self.last=random.choice(dic['last']).lower()
        
        self.email=random.choice(dic['email']).lower()
        
        self.random_digits=str(random.random())[2:random.choice([6,8])]
        
        self.varibles=[random_string(x) for x in [self.first,self.last,self.random_digits]]
        [self.varibles.append(x) for x in ['.','.','.'][:random.choice([0,1,2,])]]
        random.shuffle(self.varibles)
        #print(self.varibles)
        while ('.' in self.varibles[0] or '.' in self.varibles[-1] or '..' in ''.join(self.varibles)) == True:
            #print(''.join(self.varibles))
            random.shuffle(self.varibles)
            #print(self.varibles)
        self.passwd=pass_maker()
        
        self.random_email=''.join(self.varibles)+'@'+self.email
        
        self.info='\nfirst name: '+self.first+"\nlast  name: "+self.last+'\n\temail: '+self.random_email+'\n\t\tpassword:'+self.passwd+'\n'
        
        r = requests.get("https://thispersondoesnotexist.com/image", headers={'User-Agent': 'My User Agent 1.0'}).content
        with open('static/image.jpg','wb') as f:
            f.write(r)

