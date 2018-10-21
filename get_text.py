import boto3
import photos

def rekognize_text():

	a = photos.pick_asset()
	i = a.get_ui_image()
	b = i.to_jpeg()
	
	k = boto3.client('rekognition', region_name='us-east-1')
	
	print('starting...')
	
	res = k.detect_text(Image=dict(Bytes=b))
	text = [r['DetectedText'] for r in res['TextDetections']]
	
	print('done.')
	
	return text 
