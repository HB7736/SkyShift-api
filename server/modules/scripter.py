from modules.terraform import provider
from modules.aws_scripter import generate_aws_resources

scripting_modules = {"aws":generate_aws_resources}

def generate_script(resources,command=""):
    script = ""
    try:
        infrastructures = resources.get("infrastructure")
        if infrastructures:
            for infrastructure in infrastructures:
                scripter_mod = scripting_modules.get(infrastructure.get("provider"))
                if scripter_mod:
                    prov = provider(infrastructure["provider"]).get("output")
                    if prov:
                        script+=prov
                        script+=str(scripter_mod(infrastructure,command))+"\n"
            return {"script":script}
        return {"Error":"Infrastructure not provided"}
    except Exception as e:
        return {"Error":str(e)}

# resources = {"infrastructure":[{"provider":"aws","ec2":[{"name":"Instance 1","ami_id":"ami-12345678","instance_type":"t2.micro"},{"name":"Instance 2","ami_id":"ami-12345678","instance_type":"t2.micro"}],"vpc":[]},{"provider":"azure"}]}
# print(generate_script(resources=resources,command="echo Hello").get("script"))