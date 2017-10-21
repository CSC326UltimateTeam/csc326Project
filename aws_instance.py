aws_access_key_id = 'XXXXXXXXX'
aws_secret_access_key = 'XXXXXXXXXXX'
region='us-east-1'

import boto.ec2

#create the connection to the AWS platform
connection = boto.ec2.connect_to_region('us-east-1',aws_access_key_id=aws_access_key_id,
                                        aws_secret_access_key =aws_secret_access_key)

#create a permission called permission.pem
ssh_key_pair =  connection.create_key_pair('permission')
#save this permission under the permissions derectory, not committed
ssh_key_pair.save("permissions")

#create a sucurity group called csc326-group5, as specified in the handout
csc_security_group= connection.create_security_group(name ='csc326-group5', description='used for csc326 lab')

#authorize some access of this group, so we could ssh and browes the instance later on
csc_security_group.authorize(ip_protocol='ICMP', from_port=-1, to_port=-1, cidr_ip='0.0.0.0/0')
csc_security_group.authorize(ip_protocol='TCP', from_port=22, to_port=22, cidr_ip='0.0.0.0/0')
csc_security_group.authorize(ip_protocol='TCP', from_port=80, to_port=80, cidr_ip='0.0.0.0/0')

#print the id for futher reference
print csc_security_group.id

#create the instance with the parameters we set up, and some addtional options
aws_instance = connection.run_instances('ami-8caa1ce4', min_count=1, max_count=1,
              key_name='permission', security_groups=['csc326-group5'],
              addressing_type=None, instance_type='t1.micro', placement=None,
              kernel_id=None, ramdisk_id=None, monitoring_enabled=True, subnet_id=None,
              block_device_map=None, disable_api_termination=False, instance_initiated_shutdown_behavior=None,
              private_ip_address=None, placement_group=None, client_token=None, security_group_ids=[csc_security_group.id],
              additional_info={"description" :"Created by Nix, Exclusively for CSC326"}, instance_profile_name=None, instance_profile_arn=None, tenancy=None,
              ebs_optimized=False, network_interfaces=None)

#now we need to assign a static ip to the instance 
instances = connection.get_only_instances()

#go through the instances running under this key pair
for instance in instances:
  #if the instance is running
    if instance.state_code ==16:
        #create an elastic address
        elastic_addr = connection.allocate_address()
        print ("the attached elastic address for the instance is " + str(elastic_addr.public_ip))
        
        #associate this address with the running instance
        elastic_addr.associate(instance.id)
        print ("instance: " + str(instance.id) +" successfully attached elastic ip address")
        if instance.root_device_type != 'ebs':
            raise TypeError("Instance root deivce type must be ebs")
        
  #now the instance is running with a elastic ip address, so next time you run it, it won't change the ip address
