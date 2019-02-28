import boto3  

regions = [ 'us-east-1','us-east-2','us-west-1','us-west-2','eu-central-1']
boto3.setup_default_session(profile_name='myprofile')
for region in regions:
    print region
    ec2 = boto3.resource('ec2', region)
    for instance in ec2.instances.all():
        volumetags = []
        instancetags = [ tag for tag in instance.tags if not tag['Key'].startswith('aws:')] 
        for volume in instance.volumes.all():
            for instancetag in instancetags:
                if volume.tags is None or not any(instancetag == tag for tag in volume.tags):  
                    volume.create_tags(DryRun=False, Tags=[instancetag])
                    print 'adding tag ', instancetag
