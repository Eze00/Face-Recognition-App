#Project1

Ezedine Kargougou, Tanner Greenhagen, Mark Pop

WebTier URL: http://44.193.255.131:8081/
Request Queue: inQueue	https://sqs.us-east-1.amazonaws.com/976428307571/inQueue
Response Queue: outQueue https://sqs.us-east-1.amazonaws.com/976428307571/outQueue
Input Bucket: inbucket001
Output Bucket: outbucket001


# Running commands:
Create jar: mvn clean compile assembly:single

flask run -p 8081 --with-threads

python3 multithread_workload_generator_verify_results_updated.py --num_request 50 --url 'http://44.193.255.131:8081/' --image_folder 'images/'

python3 controller.py &
export FLASK_APP=flaskr
export FLASK_ENV=production
flask run -p 8081 --host=0.0.0.0 --with-threads
