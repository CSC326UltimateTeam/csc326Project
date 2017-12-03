def terminate_aws():
    import os
    import time
    print("Installing dependencies...")
    os.system("python -m pip install boto")
    import boto.ec2

    print("\nplease make sure your access file is stored in the same directory \
    with name supplied below,\nfirst line is the aws_access_key_id and second line is the aws_secret_access_key\n")

    filename = raw_input("aws key file name>>")

    with open(filename) as f:
        mylist = f.read().splitlines()

    try:
        aws_access_key_id = mylist[0]
        aws_secret_access_key = mylist[1]
        region = 'us-east-1'
        # create the connection to the AWS platform
        connection = boto.ec2.connect_to_region(region, aws_access_key_id=aws_access_key_id,
                                                aws_secret_access_key=aws_secret_access_key)
        f.close()
    except Exception as er:
        print("there is an error in your keyfile, error: ")
        print(er)
        exit(-1)
    print("Connection established")
    instanceID = raw_input("instance id to shut down>>")

    for instance in connection.get_only_instances():
        if instance.id==instanceID:

            if instance.state_code!=48: #not terminated
                try:
                    instance.terminate()
                    print "terminating ",
                    while instance.state_code!=48:
                        print".",
                        time.sleep(2)
                        instance.update()
                    print("\ninstance {} successfully terminated".format(instanceID))
                    exit(0)
                except Exception as er:
                    print "termination unsuccessful: "
                    print er
                    exit(-1)
            else:
                print("instance already terminated")
                exit(0)

    print("not instance matches the id provided")
    exit(-2)

if __name__=="__main__":
    terminate_aws()
