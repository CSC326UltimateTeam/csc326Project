def deployment_aws():

    import os
    import time
    print("Installing dependencies...")
    os.system("python -m pip install boto")
    os.system("python -m pip install paramiko")
    import boto.ec2
    import paramiko

    print("\nplease make sure your access file is stored in the same directory with name supplied below,\nfirst line is the aws_access_key_id and second line is the aws_secret_access_key\n" )

    filename=raw_input("aws key file name>>")

    with open(filename) as f:
        mylist = f.read().splitlines()

    try:
        aws_access_key_id = mylist[0]
        aws_secret_access_key=mylist[1]
        region = 'us-east-1'
        #create the connection to the AWS platform
        connection = boto.ec2.connect_to_region(region,aws_access_key_id=aws_access_key_id,
                                                aws_secret_access_key =aws_secret_access_key)
        f.close()
    except Exception as er:
        print("there is an error in your keyfile, error: ")
        print(er)
        exit(-1)


    #create a permission called group5_permission.pem

    connection.delete_key_pair('group5_permission')
    ssh_key_pair =  connection.create_key_pair('group5_permission')
    #save this permission under the permissions derectory, not committed
    ssh_key_pair.save("permissions")
    print("\ncreated a permission file for your instance, saved in the 'permissions' directory")


    #create a sucurity group called csc326-group5, as specified in the handout
    connection.delete_security_group('csc326group5')
    csc_security_group= connection.create_security_group(name ='csc326group5', description='used for csc326 lab')

    #authorize some access of this group, so we could ssh and browes the instance later on
    csc_security_group.authorize(ip_protocol='ICMP', from_port=-1, to_port=-1, cidr_ip='0.0.0.0/0')
    csc_security_group.authorize(ip_protocol='TCP', from_port=22, to_port=22, cidr_ip='0.0.0.0/0')
    csc_security_group.authorize(ip_protocol='TCP', from_port=80, to_port=80, cidr_ip='0.0.0.0/0')

    #print the id for futher reference
    print "created a security group for your instance with id: ", csc_security_group.id

    print("creating instance...")
    #create the instance with the parameters we set up, and some addtional options
    aws_instance = connection.run_instances('ami-8caa1ce4', min_count=1, max_count=1,
                  key_name='group5_permission', security_groups=['csc326group5'],
                  addressing_type=None, instance_type='t1.micro', placement=None,
                  kernel_id=None, ramdisk_id=None, monitoring_enabled=True, subnet_id=None,
                  block_device_map=None, disable_api_termination=False, instance_initiated_shutdown_behavior=None,
                  private_ip_address=None, placement_group=None, client_token=None, security_group_ids=[csc_security_group.id],
                  additional_info={"description" :"Created by Nix, Exclusively for CSC326"}, instance_profile_name=None, instance_profile_arn=None, tenancy=None,
                  ebs_optimized=False, network_interfaces=None)

    #now we need to assign a static ip to the instance
    running_instance=aws_instance.instances[0]
    while running_instance.state_code!=16:
        print ". ",
        time.sleep(2)
        running_instance.update()
    print("\nDone!")

    print("setting up server on instance, this may take a while...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    while True:
        try:

            client.connect(running_instance.ip_address, username='ubuntu',
                           key_filename='permissions/group5_permission.pem')
            break
        except Exception as er:
            time.sleep(5)
            continue

    print("Installing tools for the system")
    stdin, stdout, stderr = client.exec_command("sudo apt-get install git -y")
    exit_status = stdout.channel.recv_exit_status()  # Blocking call
    if exit_status == 0:
        print("Done!\n")
    else:
        print("Error", exit_status)


    print("Downloading project files...")
    #stdin, stdout, stderr = client.exec_command("git clone https://github.com/CSC326UltimateTeam/csc326Project.git")
    os.system('scp -i permissions/group5_permission.pem ../csc326Project ubuntu@{}:~/'.format(running_instance.ip_address))
    exit_status = stdout.channel.recv_exit_status()  # Blocking call
    if exit_status == 0:
        print("Done!\n")
    else:
        print("Error", exit_status)

    print("Installing dependencies")
    stdin, stdout, stderr = client.exec_command("sudo python ~/csc326Project/setup.py")
    exit_status = stdout.channel.recv_exit_status()  # Blocking call
    if exit_status == 0:
        print("Done!\n")
    else:
        print("Error", exit_status)

    print("initializing server")
    transport = client.get_transport()
    channel = transport.open_session()
    channel.exec_command('sudo python ~/csc326Project/srv.py > /dev/null 2>&1 &')

    print("\nServer is successfully running")
    print "instance ID: ", running_instance.id
    print "ip:          ", running_instance.ip_address
    print "public DNS:  ", running_instance.public_dns_name
    print "Port:         80"
    print("Thank you for choosing group 5 as your service provider!")



if __name__ == '__main__':

    deployment_aws()
