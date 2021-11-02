import torch

model = torch.hub.load('./YOLO/', 'custom', path='./YOLO/weights.pt', source='local')
# define the yolo model, weights & threshold settings need to be adjusted further


def detect_image(img_dir):
	results = model(img_dir)
	crops = results.display(crop=True)
	detected_ingredients = []
	# get results

	for item in crops:  # return unduplicated list of ingredients detected
		ingredient_name = item['label'].split()[0]
		if ingredient_name not in detected_ingredients:
			detected_ingredients.append(ingredient_name)

	print(', '.join(detected_ingredients) + ' is detected')

	return detected_ingredients
