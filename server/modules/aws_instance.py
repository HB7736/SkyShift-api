import json
from .variables import JENKINS_URL, API_URL, AWS_ACCESS_KEY, AWS_SECRET_KEY

def aws_ec2_instance(region,label,name,inbound_rules,outbound_rules,ami,instance_type,keypair,jenkins_node_name,jenkins_node_label,jenkins_node_desc,jenkins_node_fs):
    tf_config = f'''
    #--------- Provider ---------
    provider "aws" {{
    region = "{region}"
    access_key = "{AWS_ACCESS_KEY}"
    secret_key = "{AWS_SECRET_KEY}"
    }}

    //--------- Security Group ---------
    resource "aws_security_group" "{name}-sg" {{
    name = "{name}"
    description = "This is security group for {label}"
    tags = {{
          Name = "{label}"
        }}
    }}
    '''
    
    # --------- Ingress Rules ---------
    
    # Ingress Rules
    for index, rule in enumerate(inbound_rules):
        tf_config += f'''
        // Ingress Rule {index + 1}
        resource "aws_security_group_rule" "{name}-sg-ingress-{index}" {{
          type              = "ingress"
          from_port         = {rule['from_port']}
          to_port           = {rule['to_port']}
          protocol          = "{rule['protocol']}"
          cidr_blocks       = {json.dumps(rule['cidr_blocks'])}
          security_group_id = aws_security_group.{name}-sg.id
        }}
        '''    

    # Egress Rules
    for index, rule in enumerate(outbound_rules):
        tf_config += f'''
        // Egress Rule {index + 1}
        resource "aws_security_group_rule" "{name}-sg-egress-{index}" {{
          type              = "egress"
          from_port         = {rule['from_port']}
          to_port           = {rule['to_port']}
          protocol          = "{rule['protocol']}"
          cidr_blocks       = {json.dumps(rule['cidr_blocks'])}
          security_group_id = aws_security_group.{name}-sg.id
        }}
        '''
    
    # EC2 Instance
    tf_config += f'''
    resource "aws_instance" "{name}-ec2" {{
    ami           = "{ami}"
    instance_type = "{instance_type}"
    key_name      = "{keypair}"
    security_groups = ["{name}"]
    user_data     = <<-EOF
#!/bin/bash
sudo -i
cd /home
apt update -y
apt install jq curl default-jre -y
curl -sO {JENKINS_URL}/jnlpJars/agent.jar
export nodename={jenkins_node_name}$(shuf -i 100000-999999 -n 1)
curl -X POST -H "Content-Type: application/json" -d "\u007B\\"name\\":\\"$(echo $nodename)\\",\\"label\\":\\"{jenkins_node_label}\\",\\"description\\":\\"{jenkins_node_desc}\\",\\"remoteFS\\":\\"{jenkins_node_fs}\\"\u007D" {API_URL}/jenkins/create_node
export nodesecret=$(curl -X POST -H "Content-Type: application/json" -d "\u007B\\"name\\":\\"$(echo $nodename)\\"\u007D" {API_URL}/jenkins/get_node_secret | jq '.secret')
history -c
java -jar agent.jar -url {JENKINS_URL} -secret $(echo $nodesecret | tr -d '"') -name $(echo $nodename) -workDir "{jenkins_node_fs}"
EOF

    tags = {{
        Name = "{label}"
    }}
    }}
    '''

    ## Output Parameters
    tf_config+=f'''
    data "aws_instance" "{name}-ec2-data" {{
      instance_id = aws_instance.{name}-ec2.id
    }}
    
    output "instance_info" {{
      value = {{
        instance_id      = aws_instance.{name}-ec2.id
        public_ip        = data.aws_instance.{name}-ec2-data.public_ip
        private_ip       = data.aws_instance.{name}-ec2-data.private_ip
      }}
    }}'''


    return tf_config
