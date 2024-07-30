from re import match

ec2_properties = {
    "ami_id": lambda value: f'ami = "{value}"' if match(r'^ami-[a-fA-F0-9]{8}$',value) else 'ami = "ami-0a1b648e2cd533174"',
    "instance_type": lambda value: f'instance_type = "{value}"' if  match(r'^[a-z][1-9]+\.[a-z0-9]+$',value) else 'instance_type = "t2.micro"',
    # "tags": lambda value: f'tags = {{\n{', '.join([f'\"{k}\" = \"{v}\"' for k, v in value.items()])}\n}}' if isinstance(value, dict) else None
}

def generate_aws_resources(resources,command=""):
    script=""
    instances = resources.get("ec2")
    if instances:
        for instance in instances:
            script+=generate_ec2_instance(resource=instance,command=command)+"\n"
    vpcs = resources.get("vpc")
    if vpcs:
        for vpc in vpcs:
            script+=generate_vpc(resource=instance)+"\n"
    return script

def generate_ec2_instance(resource,command=""):
    script = ""
    if(resource.get("name") and  resource.get("ami_id") and resource.get("instance_type")):
        instance_name = resource.get("name")
        if match(r'^[a-zA-Z0-9_ -]{0,50}$',instance_name):
            script+=f'\nresource "aws_instance" "{instance_name}"'+'{'
            # attributes = resource.keys()
            # attributes.remove("name")
            for attribute in resource.keys():
                liner = ec2_properties.get(attribute)
                if liner:
                    line = liner(resource[attribute])
                    if line:
                        script+='\n'+line
            script+=f'\nuser_data = <<-EOF\n#!/bin/bash\n{command}\nEOF' if command else ''
            script+='\n}'
    return script

def generate_vpc(resource):
    script = ""
    return script