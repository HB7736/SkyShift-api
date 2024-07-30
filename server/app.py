from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from re import match
from modules.aws_instance import aws_ec2_instance
from modules import skyshift_github, session
from modules.project import get_supported_languages
from modules.scripter import generate_script
from modules.jenkins import create_node, get_node_secret, remove_node, create_job, trigger_build, get_job_output
from modules.fields import username_field, repo_name_field, branch_name_field, session_id_field, desc_field, path_field, port_field

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/github/list_repos', methods=['POST'])
@cross_origin()
def list_repos():
    try:
        data = request.json  # Access JSON data from POST request

        if "username" in data:
            if match(username_field, data["username"]):
                return jsonify(skyshift_github.get_user_repositories_info(owner=data["username"]))
            else:
                return jsonify({"Error": "Invalid Username Format"})
        else:
            return jsonify({"Error": "No username provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/github/repo_info', methods=['POST'])
@cross_origin()
def repo_info():
    try:
        data = request.json  # Access JSON data from POST request

        if "username" in data:
            if not match(username_field, data["username"]):
                return jsonify({"Error": "Invalid Username Format"})
            if "repo_name" in data:
                if not match(repo_name_field, data["repo_name"]):
                    return jsonify({"Error": "Invalid Repository Name Format"})
                if "branch_name" in data:
                    if not match(branch_name_field, data["branch_name"]):
                        return jsonify({"Error": "Invalid Branch Name Format"})
                    # Getting Repo Info
                    return jsonify(skyshift_github.get_repo_info(owner=data["username"],repo_name=data["repo_name"],branch_name=data["branch_name"]))
                else:
                    return jsonify({"Error": "No Branch Name Provided"})
            else:
                return jsonify({"Error": "No Repository Name Provided"})
        else:
            return jsonify({"Error": "No Username Provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/project/supported_languages', methods=['GET'])
@cross_origin()
def supported_languages():
    try:
        return jsonify(get_supported_languages())
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/user/create_session', methods=['POST'])
@cross_origin()
def create_user_session():
    try:
        data = request.json  # Access JSON data from POST request

        if "username" in data:
            if not match(username_field, data["username"]):
                return jsonify({"Error": "Invalid Username Format"})
            if "script" in data:
                if not type(data["script"])==str:
                    return jsonify({"Error":"Invalid Script Parameter"})
                return jsonify(session.create_session(userid=data["username"],script=data["script"]))
            else:
                return jsonify({"Error": "No Script Provided"})
        else:
            return jsonify({"Error": "No Username Provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/user/list_sessions', methods=['POST'])
@cross_origin()
def list_user_sessions():
    try:
        data = request.json  # Access JSON data from POST request

        if "username" in data:
            if not match(username_field, data["username"]):
                return jsonify({"Error": "Invalid Username Format"})
            return jsonify(session.list_sessions(userid=data["username"]))
        else:
            return jsonify({"Error": "No Username Provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/user/remove_session', methods=['POST'])
@cross_origin()
def remove_user_session():
    try:
        data = request.json  # Access JSON data from POST request

        if "username" in data:
            if not match(username_field, data["username"]):
                return jsonify({"Error": "Invalid Username Format"})
            if "session_id" in data:
                if not match(session_id_field,data["session_id"]):
                    return jsonify({"Error":"Invalid Session ID Format"})
                return jsonify(session.remove_session(userid=data["username"],session_id=data["session_id"]))
            else:
                return jsonify({"Error": "No Session ID Provided"})
        else:
            return jsonify({"Error": "No Username Provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/user/remove_all_sessions', methods=['POST'])
@cross_origin()
def remove_user_dir():
    try:
        data = request.json  # Access JSON data from POST request

        if "username" in data:
            if not match(username_field, data["username"]):
                return jsonify({"Error": "Invalid Username Format"})
            return jsonify(session.remove_all_session(userid=data["username"]))
        else:
            return jsonify({"Error": "No Username Provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/user/start_session', methods=['POST'])
@cross_origin()
def start_user_session():
    try:
        data = request.json  # Access JSON data from POST request

        if "username" in data:
            if not match(username_field, data["username"]):
                return jsonify({"Error": "Invalid Username Format"})
            if "session_id" in data:
                if not match(session_id_field,data["session_id"]):
                    return jsonify({"Error":"Invalid Session ID Format"})
                return jsonify(session.start_session(userid=data["username"],session_id=data["session_id"]))
            else:
                return jsonify({"Error": "No Session ID Provided"})
        else:
            return jsonify({"Error": "No Username Provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/user/session_info', methods=['POST'])
@cross_origin()
def get_user_session_info():
    try:
        data = request.json  # Access JSON data from POST request

        if "username" in data:
            if not match(username_field, data["username"]):
                return jsonify({"Error": "Invalid Username Format"})
            if "session_id" in data:
                if not match(session_id_field,data["session_id"]):
                    return jsonify({"Error":"Invalid Session ID Format"})
                return jsonify(session.session_info(userid=data["username"],session_id=data["session_id"]))
            else:
                return jsonify({"Error": "No Session ID Provided"})
        else:
            return jsonify({"Error": "No Username Provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/user/destroy_session', methods=['POST'])
@cross_origin()
def destroy_user_session():
    try:
        data = request.json  # Access JSON data from POST request

        if "username" in data:
            if not match(username_field, data["username"]):
                return jsonify({"Error": "Invalid Username Format"})
            if "session_id" in data:
                if not match(session_id_field,data["session_id"]):
                    return jsonify({"Error":"Invalid Session ID Format"})
                return jsonify(session.destroy_session(userid=data["username"],session_id=data["session_id"]))
            else:
                return jsonify({"Error": "No Session ID Provided"})
        else:
            return jsonify({"Error": "No Username Provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/terraform/generate_script', methods=['POST'])
@cross_origin()
def generate_terraform_script():
    try:
        data = request.json  # Access JSON data from POST request

        if "infrastructure" in data:
            if data["infrastructure"]:
                command = data["command"] if data.get("command") else ''
                return jsonify(generate_script(resources=data,command=command))
            return jsonify({"Error": "Infrastructure is Empty"})
        else:
            return jsonify({"Error": "No Infrastructure Provided"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/jenkins/create_node', methods=['POST'])
@cross_origin()
def create_jenkins_node():
    try:
        data = request.json  # Access JSON data from POST request

        if "name" in data:
            if not match(username_field,data["name"]):
                return jsonify({"Error": "Node Name Format Invalid!"})
            if "label" in data:
                if not match(username_field,data["label"]):
                    return jsonify({"Error": "Node Name Format Invalid!"})
                if "description" in data:
                    if not match(desc_field,data["description"]):
                        return jsonify({"Error": "Node Description Should Only Contain Alphabets, Number, Underscore, Full-Stop, and Spaces!"})
                    if "remoteFS" in data:
                        if not match(path_field,data["remoteFS"]):
                            return jsonify({"Error": "Node RemoteFS Format Not Accepted!"})
                        return jsonify(create_node(name=data["name"],label=data["label"],desc=data["description"],remoteFS=data["remoteFS"]))
                    return jsonify({"Error": "Node Workdir Not Specified!"})
                return jsonify({"Error": "Node Description Not Provided!"})
            return jsonify({"Error": "Node Label Not Provided!"})
        else:
            return jsonify({"Error": "Node Name Not Provided!"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/jenkins/get_node_secret', methods=['POST'])
@cross_origin()
def get_jenkins_node_secret():
    try:
        data = request.json  # Access JSON data from POST request

        if "name" in data:
            if not match(username_field,data["name"]):
                return jsonify({"Error": "Node Name Format Invalid!"})
            return jsonify(get_node_secret(name=data["name"]))
        else:
            return jsonify({"Error": "Node Name Not Provided!"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/jenkins/delete_node', methods=['POST'])
@cross_origin()
def remove_jenkins_node():
    try:
        data = request.json  # Access JSON data from POST request

        if "name" in data:
            if not match(username_field,data["name"]):
                return jsonify({"Error": "Node Name Format Invalid!"})
            return jsonify(remove_node(name=data["name"]))
        else:
            return jsonify({"Error": "Node Name Not Provided!"})
    except Exception as e:
        return jsonify({"Error": str(e)})

@app.route('/jenkins/create_job', methods=['POST'])
@cross_origin()
def create_jenkins_job():
    try:
        build_steps = request.json.get('build_steps', [])
        job_name = request.json.get('job_name')
        node_label = request.json.get('node_label')
        if not build_steps or not job_name:
            return jsonify({'Error': 'build_steps and job_name are required parameters'}), 400
        return jsonify(create_job(job_name=job_name,node_label=node_label,build_steps=build_steps))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@app.route('/jenkins/trigger_build', methods=['POST'])
@cross_origin()
def trigger_jenkins_build():
    try:
        job_name = request.json.get('job_name')
        if not job_name:
            return jsonify({'Error': 'job_name is a required parameter'}), 400
        return jsonify(trigger_build(job_name=job_name))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@app.route('/jenkins/build_output', methods=['POST'])
@cross_origin()
def get_build_output():
    try:
        job_name = request.json.get('job_name')
        if not job_name:
            return jsonify({'Error': 'job_name is a required parameter'}), 400
        return jsonify(get_job_output(job_name=job_name))
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@app.route('/generate_terraform_code/aws_instance',methods=['POST'])
@cross_origin()
def generate_aws_instance_script():
    # Extract data from request
    data= request.json
    region=data.get('region')
    label=data.get('label')
    name=data.get('name')
    inbound_rules=data.get('inbound_rules')
    outbound_rules=data.get('outbound_rules')
    ami=data.get('ami')
    instance_type=data.get('instance_type')
    keypair=data.get('keypair')
    jenkins_node_name = data.get('jenkins_node_name')
    jenkins_node_label = data.get('jenkins_node_label')
    jenkins_node_desc = data.get('jenkins_node_desc')
    jenkins_node_fs = data.get('jenkins_node_fs')

    # Validation
    if not all([label, region, name, inbound_rules, outbound_rules, ami, instance_type, keypair, jenkins_node_name, jenkins_node_label]):
        return jsonify({'status': False, 'message': 'All fields are required.'})
    if not jenkins_node_desc:
        jenkins_node_desc = ""
    if not jenkins_node_fs:
        jenkins_node_fs = "./"

    for rule in inbound_rules + outbound_rules:
        if not all([rule.get('from_port'), rule.get('to_port'), rule.get('protocol'), rule.get('cidr_blocks')]):
            return jsonify({'status': False, 'message': 'Invalid rule format.'})

        if not match(port_field,str(rule.get('from_port'))) or not match(port_field,str(rule.get('to_port'))):
            return jsonify({'status': False, 'message': 'Invalid port number.'})

    # If all validations pass, return success status
    response = aws_ec2_instance(region=region,label=label,name=name,inbound_rules=inbound_rules,outbound_rules=outbound_rules,ami=ami,instance_type=instance_type,keypair=keypair,jenkins_node_name=jenkins_node_name,jenkins_node_label=jenkins_node_label,jenkins_node_desc=jenkins_node_desc,jenkins_node_fs=jenkins_node_fs)
    return jsonify({'status': True,"response":response})

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
