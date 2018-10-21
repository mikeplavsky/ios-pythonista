import appex
from PIL import Image
import io
from get_text import rekognize_text
import clipboard

def main():
	
	if not appex.is_running_extension():
		img = Image.open('test:Mandrill')
	else:
		img = appex.get_image()
	if not img:
		print('No input image found')
		return 
		
	arr = io.BytesIO()
	img.save(arr, format='JPEG')
	
	text = rekognize_text(arr.getvalue())
	res = '\n'.join(text)	
	
	clipboard.set(res)
	
	print(res)

if __name__ == '__main__':
	main()
