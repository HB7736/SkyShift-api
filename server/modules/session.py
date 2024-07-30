from os.path import exists
from os.path import join as pathjoin
from re import findall
from os import makedirs, symlink, getcwd, listdir
from uuid import uuid4
from shutil import rmtree
from modules.terraform import terraform_plan, terraform_apply, terraform_output, terraform_destroy

session_dir_name = "sessions/"
session_dir_available = 0

def get_session_dir():
    global session_dir_available
    if not session_dir_available:
        if not exists(session_dir_name):
            makedirs(session_dir_name)
        session_dir_available = 1
    return session_dir_name

def get_ips(content):
    try:
        match = findall(r'(?:[1-9]{1}[0-9]{1,2}\.){3}[0-9]{1,3}', content)
        return match if len(match)==2 else ""
    except Exception as e:
        return ""

def create_session(userid, script):
    # Create the main folder if it doesn't exist
    try:
        # Creating Session Directory if Doesn't exists
        session_dir = get_session_dir()
        userdir = pathjoin(session_dir,userid)

        if not exists(userdir):
            makedirs(userdir)

        # Generate a unique subfolder name using UUID
        session = str(uuid4())

        # Ensure the uniqueness of the subfolder name
        while exists(pathjoin(userdir, session)):
            session = str(uuid4())

        # Create the subfolder
        session_path = pathjoin(userdir, session)
        makedirs(session_path)
        symlink(pathjoin(getcwd(),".terraform"),pathjoin(getcwd(),session_path,".terraform"))
        symlink(pathjoin(getcwd(),".terraform.lock.hcl"),pathjoin(getcwd(),session_path,".terraform.lock.hcl"))
        # Write the file inside the subfolder
        with open(pathjoin(session_path, 'main.tf'), 'w') as file:
            file.write(script)
        return {"SessionID":session}
    except TypeError as te:
        return {"Error":"Error occur while creating session"} if "Path" in str(te) else {"Error":"Error occur while writing resources"}
    except Exception as e:
        return {"Error":"Unknown Error Occured","out":str(e)}

def list_sessions(userid):
    session_dir = get_session_dir()
    userdir = pathjoin(session_dir,userid)
    try:
        if exists(userdir):
            return {"sessions":listdir(userdir)}
        else:
            return {"sessions":[]}
    except Exception as e:
        return {"Error":str(e)}

def remove_session(userid,session_id):
    session_dir = get_session_dir()
    userdir = pathjoin(session_dir,userid)
    try:
        if exists(userdir):
            session = pathjoin(userdir,session_id)
            if exists(session):
                rmtree(session)
                return {"Info":"Session Removed Successfully"}
            else:
                return {"Error":"Session Doesn't Exists"}
        else:
            return {"Error":"User have no Session"}
    except Exception as e:
        return {"Error":"Unknown Error Occured","out":str(e)}

def remove_all_session(userid):
    session_dir = get_session_dir()
    userdir = pathjoin(session_dir,userid)
    try:
        if exists(userdir):
            sessions = list_sessions(userid=userid)
            if sessions.get("sessions"):
                for session in sessions["sessions"]:
                    remove_session(userid=userid,session_id=session)
            rmtree(userdir)
            return {"Info":"Sessions Removed Successfully"}
        else:
            return {"Error":"User have no Session"}
    except Exception as e:
        return {"Error":"Unknown Error Occured","out":str(e)}

def start_session(userid,session_id):
    session_dir = get_session_dir()
    session = pathjoin(session_dir,userid,session_id)
    try:
        if exists(session):
            result = terraform_plan(session_path=session)
            result = terraform_apply(session_path=session)
            if result.get("code"):
                if "public_ip" in result["Output"]:
                    IPs = get_ips(result["Output"])
                    if IPs:
                        result["private_ip"],result["public_ip"] = IPs
            return result
        else:
            return {"Error":"Session Doesn't Exists"}
    except Exception as e:
        return {"Error":"Unknown Error Occured","out":str(e)}

def session_info(userid,session_id):
    session_dir = get_session_dir()
    session = pathjoin(session_dir,userid,session_id)
    try:
        if exists(session):
            result = terraform_output(session_path=session)
            if result.get("code"):
                if "public_ip" in result["Output"]:
                    IPs = get_ips(result["Output"])
                    if IPs:
                        result["private_ip"],result["public_ip"] = IPs
            return result
        else:
            return {"Error":"Session Doesn't Exists"}
    except Exception as e:
        return {"Error":"Unknown Error Occured","out":str(e)}

def destroy_session(userid,session_id):
    session_dir = get_session_dir()
    session = pathjoin(session_dir,userid,session_id)
    try:
        if exists(session):
            return terraform_destroy(session_path=session)
        else:
            return {"Error":"Session Doesn't Exists"}
    except Exception as e:
        return {"Error":"Unknown Error Occured","out":str(e)}