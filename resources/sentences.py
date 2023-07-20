def sentences():
	sentences = []
	with open("resources/sentences.txt", "r") as f:
		for line in f:
			sentences.append(line.strip())

	# return the sentence
	return sentences
