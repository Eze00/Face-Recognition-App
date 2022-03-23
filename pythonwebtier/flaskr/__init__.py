import os
import io
import PIL.Image as Image
import boto3


from flask import Flask, redirect, url_for, request


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)

	# a simple page that says hello
	@app.route('/',methods = ['POST','GET'])
	def deal_with_requests():

		session = boto3.session.Session()
		client = session.client('sqs',aws_access_key_id="AKIA6GV5JSRZYYIWNCN4", aws_secret_access_key="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",region_name='us-east-1')
		request_url = "https://sqs.us-east-1.amazonaws.com/976428307571/inQueue"
		response_url = "https://sqs.us-east-1.amazonaws.com/976428307571/outQueue"

		if request.method == 'POST':
			image_bytes = request.files['myfile']
			file_name = image_bytes.filename
			stream = image_bytes.stream
			image_data = stream.read() # byte values of the image
			image = Image.open(io.BytesIO(image_data))
			pix = list(image.getdata())
			pixel_string = f'{file_name} {image.size[0]} {image.size[1]}'
			# print(pix[0])
			for p in pix:
				pixel_string+= f' {p[0]},{p[1]},{p[2]}'
			
			client.send_message(QueueUrl=request_url,MessageBody=pixel_string,DelaySeconds=0)


			messagesBody = ''
			while(messagesBody == ''):
				messages = client.receive_message(QueueUrl=response_url,MaxNumberOfMessages=1)
				if not messages.get('Messages') ==  None and file_name in messages['Messages'][0]['Body']:
					messagesBody = messages['Messages'][0]['Body']
					client.delete_message(QueueUrl=response_url,ReceiptHandle=messages['Messages'][0]['ReceiptHandle'])
				elif not messages.get('Messages') ==  None:
					client.change_message_visibility(QueueUrl=response_url,ReceiptHandle=messages['Messages'][0]['ReceiptHandle'],VisibilityTimeout=1)

			
			return messagesBody.split(' ')[0]


	return app