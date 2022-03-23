package applicationtier;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import javax.imageio.ImageIO;

import com.amazonaws.AmazonServiceException;
import com.amazonaws.SdkClientException;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.sqs.AmazonSQS;
import com.amazonaws.services.sqs.AmazonSQSClientBuilder;
import com.amazonaws.services.sqs.model.ChangeMessageVisibilityRequest;
import com.amazonaws.services.sqs.model.GetQueueAttributesRequest;
import com.amazonaws.services.sqs.model.GetQueueAttributesResult;
import com.amazonaws.services.sqs.model.Message;
import com.amazonaws.services.sqs.model.SendMessageRequest;
import com.amazonaws.util.EC2MetadataUtils;
import com.amazonaws.services.ec2.AmazonEC2;
import com.amazonaws.services.ec2.AmazonEC2ClientBuilder;
import com.amazonaws.services.ec2.model.StopInstancesRequest;

public class AppTierMain {
private static final String QUEUE_NAME = "testQueue" + new Date().getTime();
    
    private static final BasicAWSCredentials awsCreds = new BasicAWSCredentials("AKIA6GV5JSRZYYIWNCN4", "8OmKaoj9/edBkkUZPPbSyUfP3hd6In/qKznLTvWR");

    private static final String requestQueueUrl = "https://sqs.us-east-1.amazonaws.com/976428307571/inQueue";
    private static final String responseQueueUrl = "https://sqs.us-east-1.amazonaws.com/976428307571/outQueue";
    
    private static final String inputBucket = "inbucket001";
    
    private static final String outputBucket = "outbucket001";
    
    public static void main(String[] args) throws InterruptedException
    {
    	
    	
    	while (true) {getMessage();}        
        
    }
    
    
    private static void getMessage() throws InterruptedException {
    	
        AmazonSQS sqs = AmazonSQSClientBuilder.standard().withCredentials(new AWSStaticCredentialsProvider(awsCreds)).withRegion(Regions.US_EAST_1).build();
        
        //Get messages
        List<Message> messages = sqs.receiveMessage(requestQueueUrl).getMessages();
        
        while(messages.size()>0) {
	        String pixelString = messages.get(0).getBody();
	        
	        //Return other messages to the request queue
	        for(int i = 1; i < messages.size();i++) {
	        	sqs.changeMessageVisibility(requestQueueUrl, messages.get(i).getReceiptHandle(), 0);
	        }
	        
	        //Get image name, width, height
	        String[] pixelStrings = pixelString.split(" ");
	        String filename = pixelStrings[0];
	        int width = Integer.valueOf(pixelStrings[1]);
	        int height = Integer.valueOf(pixelStrings[2]);
	        
	        //Get integer pixel values
	        int pixels[] = new int[pixelStrings.length-3];
	        for(int i = 3; i < pixelStrings.length;i++) {
	        	String colorValues[] = pixelStrings[i].split(",");
	        	Color c = new Color(Integer.valueOf(colorValues[0]),Integer.valueOf(colorValues[1]),Integer.valueOf(colorValues[2]));//,Integer.valueOf(colorValues[3]));
	        	int rgb = Integer.valueOf(colorValues[0]);
	        	rgb = (rgb << 8) + Integer.valueOf(colorValues[1]); 
	        	rgb = (rgb << 8) + Integer.valueOf(colorValues[2]);
	        	
	        	pixels[i-3] = rgb;
	        	
	        }
	        
	        
	        BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
	        image.setRGB(0, 0, width, height, pixels, 0, 64);
	        try {
	        	//Get actual image file
	        	String filepath = "/home/ec2-user/"+filename;
	        	File f = new File(filepath); 
				ImageIO.write(image,"png", f);
				f.createNewFile();
				
		        AmazonS3 s3 = AmazonS3ClientBuilder.standard().withCredentials(new AWSStaticCredentialsProvider(awsCreds)).withRegion(Regions.US_EAST_1).build();
		        s3.putObject(inputBucket, filename, f);
				
		        //Get classification result
				Process p = Runtime.getRuntime().exec("python3 /home/ec2-user/face_recognition.py "+filepath);
				String output = (new BufferedReader(new InputStreamReader(p.getInputStream()))).readLine();
				

		        s3.putObject(outputBucket, filename.replaceAll(".jpg", ""), output);
	
		        String finalOutput = output+" "+filename;
				System.out.println(finalOutput);
				
				//Send output to response queue
				sqs.sendMessage(responseQueueUrl, finalOutput);
				
			} catch (IOException e) {
				e.printStackTrace();
			}
	       
	        //Delete message and get more messages
	        sqs.deleteMessage(requestQueueUrl, messages.get(0).getReceiptHandle());
	        messages = sqs.receiveMessage(requestQueueUrl).getMessages();
        }
        
        
        
    }

}
