import boto3
import photos

import clipboard
t = clipboard.get()

def pick_image():
	
	a = photos.pick_asset()
	i = a.get_ui_image()
	b = i.to_jpeg()
	
	return rekognize_text(b)

def rekognize_text(b):
	
	k = boto3.client('rekognition', region_name='us-east-1')
	
	print('starting...')
	
	res = k.detect_text(Image=dict(Bytes=b))
	text = [r['DetectedText'] for r in res['TextDetections']]
	
	print('done.')
	
	return text 
	
c = boto3.client('comprehend')

comprehend = lambda func, key: func(Text=t, LanguageCode = 'en')

def get_comprehend(func,key,t):
	
	res = comprehend(func, key)
	return [e['Text'] for e in res[key]]
	
get_entities = lambda t: get_comprehend(
	c.detect_entities,'Entities',t)
		
get_key_phrases = lambda t: get_comprehend(
	c.detect_key_phrases,'KeyPhrases',t)
	
get_sentiment = lambda t: comprehend(
	c.detect_sentiment,t)

	
