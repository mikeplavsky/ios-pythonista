import boto3
import photos

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

def comprehend(func): 
	
	import clipboard
	copied = clipboard.get()
	
	t = copied[:4700]
	
	return func(Text=t, LanguageCode = 'en')

def get_comprehend(func,key):
	
	res = comprehend(func)
	print(
		'\n'.join(
			[e['Text'] for e in res[key]]))
	
get_entities = lambda: get_comprehend(
	c.detect_entities,'Entities')
		
get_key_phrases = lambda: get_comprehend(
	c.detect_key_phrases,'KeyPhrases')
	
get_sentiment = lambda: comprehend(
	c.detect_sentiment)['SentimentScore']

	
