from re import match
from subprocess import run, CalledProcessError
from os.path import exists
from .variables import AWS_ACCESS_KEY, AWS_SECRET_KEY

providers = {"aws":
f"""
provider "aws" {{
  region     = "ap-south-1"
  access_key = "{AWS_ACCESS_KEY}"
  secret_key = "{AWS_SECRET_KEY}"
}}
""",

}

def get_all_providers():
    all_providers = ""
    for prov in providers.keys():
        all_providers+=providers[prov]
    return all_providers

terraform_available = 0

def terraform_init():
    global terraform_available
    if not terraform_available:
        if not exists("..terraform/"):
            try:
                with open("main.tf","w") as init_file:
                    init_file.write(get_all_providers())
                result = run(["terraform", "init"], capture_output=True, text=True, check=True)
                terraform_available = 1
            except Exception as e:
                print(e)
        else:
            terraform_available = 1
    return terraform_available

def terraform_plan(session_path):
    try:
        if(terraform_init()):
            # result = run(["terraform", "init"], capture_output=True, text=True, check=True, cwd=session_path)
            result = run(["terraform", "plan"], capture_output=True, text=True, check=True, cwd=session_path)
            return {"code":1,"Output":result.stdout}
        else:
            return {"Error":"Terraform Init Failed"}
    except CalledProcessError as e:
        return {"Error": e}
    except Exception as e:
        return {"Error": e}

def terraform_apply(session_path):
    try:
        if(terraform_init()):
            result = run(["terraform", "apply", "-auto-approve"], capture_output=True, text=True, check=True, cwd=session_path)
            return {"code":1,"Output":result.stdout}
        else:
            return {"Error":"Terraform Init Failed"}
    except CalledProcessError as e:
        return {"Error": str(e)}
    except Exception as e:
        return {"Error": str(e)}

def terraform_output(session_path):
    try:
        if(terraform_init()):
            result = run(["terraform", "output"], capture_output=True, text=True, check=True, cwd=session_path)
            return {"code":1,"Output":result.stdout}
        else:
            return {"Error":"Terraform Init Failed"}
    except CalledProcessError as e:
        return {"Error": str(e)}
    except Exception as e:
        return {"Error": str(e)}

def terraform_destroy(session_path):
    try:
        if(terraform_init()):
            result = run(["terraform", "destroy", "-auto-approve"], capture_output=True, text=True, check=True, cwd=session_path)
            return {"code":1,"Output":result.stdout}
        else:
            return {"Error":"Terraform Init Failed"}
    except CalledProcessError as e:
        return {"Error": str(e)}
    except Exception as e:
        return {"Error": str(e)}

def provider(provider="aws"):
    return {"output":providers[provider]} if provider in providers else {"Error":"Cloud Provider not supported"}

# def ec2(Instance_Name="test",AMI_ID="ami-0a7cf821b91bcccbc",Instance_Type="t2.micro",commands=""):
#     if not match(r'[a-zA-Z0-9][a-zA-Z0-9_-]*[a-zA-Z0-9]',Instance_Name):
#         return {"Error":"Instance Name Disallowed"}
#     if not match(r'ami-[0-9a-fA-F]{8,}',AMI_ID):
#         return {"Error":"Invalid Format for AMI ID"}
#     if match(r'[a-z0-9][.][a-z0-9]',Instance_Type):
#         return {"Error":"Invalid Format for Instance Type"}
#     resource = {"output":f"""
# resource "aws_instance" "{Instance_Name}" {{
#     ami           = "{AMI_ID}"
#     instance_type = "{Instance_Type}"
#     user_data = <<-EOF
# #!/bin/bash
# {commands}
# EOF
# }}
# """}
#     return resource
