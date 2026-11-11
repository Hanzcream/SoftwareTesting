from sqlite3 import connect

database:str = "db/school.db"

def getprocess(sql:str,vals:list)->list:
    print(sql)
    conn:any = None
    cursor:any = None
    data:list = []
    try:
        conn = connect(database)
        cursor = conn.cursor()
        cursor.execute(sql,vals)
        data=cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    return data
        
        
def postprocess(sql:str,vals:list)->bool:
    print(sql)
    conn:any = None
    cursor:any = None
    try:
        conn = connect(database)
        cursor = conn.cursor()
        cursor.execute(sql,vals)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    return True if cursor.rowcount>0 else False   
        
def getall(table:str)->list:
    sql:str = f"SELECT * FROM `{table}`"
    return getprocess(sql,[])
    
def getrecord(table:str,**kwargs)->list:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    flds:list = []
    [flds.append("`"+key+"`=?") for key in keys]
    fld:str = " AND ".join(flds)
    sql:str = f"SELECT * FROM `{table}` WHERE {fld}"
    return getprocess(sql,vals)
    
def deleterecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    [flds.append("`"+key+"`=?") for key in keys]
    fld:str = " AND ".join(flds)
    sql:str = f"DELETE FROM `{table}` WHERE {fld}"
    return postprocess(sql,vals)
    
def addrecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    #insert into `student`(`idno`,`name`,`course`) values(?,?,?)
    q:list = ['?']*len(keys)
    qmarks:str = ",".join(q)
    flds:str = "`,`".join(keys)
    sql:str = f"INSERT INTO `{table}`(`{flds}`) VALUES({ qmarks})"
    return postprocess(sql,vals)
    
def updaterecord(table:str,**kwargs)->bool:
    keys:list = list(kwargs.keys())
    vals:list = list(kwargs.values())
    #update `students` SET `lastname`=?,`firstname`=? WHERE `idno`='1000'
    flds:list = []
    newvals:list = []
    for i in range(1,len(keys)):
        flds.append("`"+keys[i]+"`=?")
        newvals.append(vals[i])
    fld:str = ",".join(flds)
    sql:str = f"UPDATE `{table}` SET {fld} WHERE `{keys[0]}`='{vals[0]}'"
    return postprocess(sql,newvals)
    
#print(updaterecord('students',idno='1006',lastname='oda',firstname='mako',course='bscs',level='3'))
print(getall('students'))