from re import search, findall
import requests
import json
from jenkinsapi.jenkins import Jenkins
from .variables import JENKINS_URL, USERNAME, PASSWORD

jenkins = Jenkins(JENKINS_URL, username=USERNAME, password=PASSWORD)

session = requests.Session()
session.auth = (USERNAME, PASSWORD)

def create_node(name,label,desc="",remoteFS="~/"):
    try:
        session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        data = {
            'name': name,
            'type': 'hudson.slaves.DumbSlave$DescriptorImpl',
            'json': json.dumps({
                'name': name,
                'nodeDescription': desc,
                'numExecutors': 1,
                'remoteFS': remoteFS,
                'labelString': label,
                'mode': 'NORMAL',
                'type': 'hudson.slaves.DumbSlave$DescriptorImpl',
                'retentionStrategy': {'stapler-class': 'hudson.slaves.RetentionStrategy$Always'},
                'nodeProperties': {'stapler-class-bag': 'true'}
            })
        }

        response = session.post(f'{JENKINS_URL}/computer/doCreateItem', data=data)
        if response.status_code == 200:
            return {"code":1,"status":"Node Successfully Created"}
        elif response.status_code == 400:
            return {"code":0,"Error":"Node Already Exists"}
        else:
            return {"code":2,"Error":f"Failed to Create node{response.status_code}"}
    except Exception as e:
        return {"code":0,"Error":str(e)}

def extract_secret(content):
    match = search(r'(?<=secret )[a-f0-9]+', content)
    return {"code":1,"secret":match.group(0)} if match else {"code":0}

def extract_crumb(content):
    match = search(r'(?<=data-crumb-value\W{2})[a-f0-9]+', content)
    return match.group(0) if match else ""

def extract_parameter(content):
    match = search(r'(?<=help-sibling\W\W)[0-9a-zA-Z-]+', content)
    return match.group(0) if match else ""

def extract_job_consoles(content):
    match = findall(r'/job/[a-zA-Z0-9-]+/[0-9]*/console', content)
    return match if match else ""

def get_node_secret(name):
    try:
        response = session.get(f'{JENKINS_URL}/manage/computer/{name}/')
        if response.status_code == 200:
            return extract_secret(response.content.decode('utf-8'))
        elif response.status_code == 404:
            return {"code":0,"Error":"Specified Node Does not Exists!"}
        else:
            return {"code":0,"Error":"Network Error Occured"}
    except Exception as e:
        return {"code":0,"Error":str(e)}

def remove_node(name):
    try:
        response = session.post(f'{JENKINS_URL}/computer/{name}/doDelete')
        if response.status_code == 200:
            return {"code":1,"status":"Node Successfully Deleted"}
        elif response.status_code == 404:
            return {"code":0,"Error":"Specified Node Does not Exists!"}
        else:
            return {"code":0,"Error":"Network Error Occured"}
    except Exception as e:
        return {"code":0,"Error":str(e)}

def create_job(job_name,node_label,build_steps):
    try:
        if jenkins.has_job(job_name):
            return {'Error': f'Job {job_name} already exists'}, 400
        if not node_label:
            node_label = ""
        # Create XML configuration for the job
        job_config = """
            <project>
                <actions/>
                <description>Job created via API</description>
                <keepDependencies>true</keepDependencies>
                <properties>
                    <hudson.model.ParametersDefinitionProperty>
                        <parameterDefinitions>
                            <org.jvnet.jenkins.plugins.nodelabelparameter.LabelParameterDefinition>
                            <string>org.jvnet.jenkins.plugins.nodelabelparameter.LabelParameterDefinition</string>
                            <name>{node_label}</name>
                            <defaultValue>{node_label}</defaultValue>
                            <allNodesMatchingLabel>1</allNodesMatchingLabel>
                            <triggerIfResult>allCases</triggerIfResult>
                            <description></description>
                            </org.jvnet.jenkins.plugins.nodelabelparameter.LabelParameterDefinition>
                        </parameterDefinitions>
                    </hudson.model.ParametersDefinitionProperty>
                </properties>
                <scm class="hudson.scm.NullSCM"/>
                <builders>
                    {build_steps}
                </builders>
                <publishers/>
                <buildWrappers/>
            </project>
        """.format(build_steps='<hudson.tasks.Shell>\n<command>'+"\n".join([step for step in build_steps])+'</command>\n</hudson.tasks.Shell>\n',node_label=node_label)
        jenkins.create_job(job_name, job_config)
        return {'message': f'Job {job_name} created successfully'}, 200

    except Exception as e:
        return ({'message': f'Job {job_name} created successfully'}, 200) if str(e)==f"'{job_name}'" else ({'Error': "Job may already exists..."}, 500)

# def trigger_build(job_name):
#     try:
#         job = jenkins.has_job(job_name)
#         jenkins.build_job(job_name)
#         # if not job:
#         #     return {'Error': f'Job {job_name} does not exist'}
#         # jenkins.build_job(job_name)
#         return {'message': f'Build triggered for job {job_name}'}
#     except Exception as e:
#         return {'Error': f'Job {job_name} does not exist'}

def get_job_output(job_name):
    try:
        response = session.get(f'{JENKINS_URL}/job/{job_name}/')
        if response.status_code == 200:
            consoles = extract_job_consoles(response.content.decode('utf-8'))
            results = []
            if consoles:
                for console in consoles:
                    response = session.get(f'{JENKINS_URL}{console}')
                    if response.status_code == 200:
                        output = response.content.decode('utf-8')
                        start =  output.find(f"[{job_name}] $")
                        if start>-1:
                            start+=52+len(job_name)
                            end = output.rfind("</pre>")
                            if end:
                                results.append(output[start:end])
                                break
            return {"code":1,"results":results}
        elif response.status_code == 404:
            return {"code":0,"Error":"Job Does not Exists"}
        else:
            return {"code":0,"Error":"Unknown Error Occured","status":response.status_code}
    except Exception as e:
        return {"code":0,"Error":str(e)}

def trigger_build(job_name):
    try:
        response = session.get(f'{JENKINS_URL}/job/{job_name}/build?delay=0')
        crumb = extract_crumb(response.content.decode('utf-8'))
        parameter = extract_parameter(response.content.decode('utf-8'))
        if response.status_code == 405:
            if crumb:
                session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
                data = {
                    "name": f"{parameter}",
                    "value": f"{parameter}",
                    "statusCode": 303,
                    "redirectTo": ".",
                    "json": json.dumps({
                        "parameter":{
                            "name":f"{parameter}",
                            "value":f"{parameter}"
                        },
                        "statusCode":"303",
                        "redirectTo":"."
                        })
                    }
                response = session.post(f'{JENKINS_URL}/job/{job_name}/build?delay=0', data=data)
                if response.status_code == 200:
                    return {"code":1,"status":"Build Successfully Triggered"}
                else:
                    return {"code":0,"Error":f"Failed to Trigger Job {response.status_code}","content":str(response.content)}
            else:
                return {"code":0,"Error":"Crumb not available"}
        elif response.status_code == 404:
            return {"code":0,"Error":"Job Does not Exists"}
        else:
            return {"code":0,"Error":"Unknown Error Occured","status":response.status_code}
    except Exception as e:
        return {'Error': f'Job {job_name} does not exist'}

