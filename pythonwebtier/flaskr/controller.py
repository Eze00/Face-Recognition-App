import os
import io
import boto3


def EC2count():
	client = boto3.client('ec2',aws_access_key_id="AKIA6GV5JSRZYYIWNCN4", aws_secret_access_key="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",region_name='us-east-1')
	ec2json = client.describe_instances(Filters=[{'Name':'instance-state-name','Values':['running','pending']}])
	for r in ec2json['Reservations']:
		instance = r['Instances']
		for i in instance:
			ids_list.append(i['InstanceId'])

	ids_list.pop("i-0671556683630e5f1")

	return len(ids_list)

def createInstance():
	user_data = '''#!/bin/bash java -jar /home/ec2-user/AppTier.jar'''
	ec2 = boto3.client("ec2", "us-east-1", aws_access_key_id="AKIA6GV5JSRZYYIWNCN4", aws_secret_access_key="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")

	try:
		create = ec2.run_instances(
	        InstanceType="t2.micro",
	        MaxCount=1,
	        MinCount=1,
	        ImageId="aami-063f260d812ad0232",
	    	UserData=user_data)
	except Exception as e:
	    print(e)

def stopInstances():
	ids_list= []
	client = boto3.client('ec2',aws_access_key_id="AKIA6GV5JSRZYYIWNCN4", aws_secret_access_key="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",region_name='us-east-1')
	ec2json = client.describe_instances(Filters=[{'Name':'instance-state-name','Values':['running']}])
	for r in ec2json['Reservations']:
		instance = r['Instances']
		for i in instance:
			ids_list.append(i['InstanceId'])

	ids_list.pop("i-0671556683630e5f1")
	
	for ec2ID in instance_id:
		ec2.stop_instances(ec2ID)


## MAIN ##

sqs = boto3.resource('sqs', aws_access_key_id="AKIA6GV5JSRZYYIWNCN4", aws_secret_access_key="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", region_name="us-east-1")
queue = sqs.get_queue_by_name(QueueName='inQueue')

while(True):
	if (int(queue.attributes.get('ApproximateNumberOfMessages')) > 0 and EC2count() <= 20):
		createInstance()
	if (int(queue.attributes.get('ApproximateNumberOfMessages')) == 0 and int(queue.attributes.get('ApproximateNumberOfMessagesNotVisible')) == 0):
		stopInstances()
	





