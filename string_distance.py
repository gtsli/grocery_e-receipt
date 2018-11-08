from fuzzywuzzy import fuzz
from fuzzywuzzy import process

dictionary = []
dictionary.append("apple")
dictionary.append("orange")
dictionary.append("banana")


def find_closest_string(string):
	print(dictionary)
	print(string)
	closest_string = dictionary[0]
	closest_ratio = fuzz.ratio(string, closest_string)	
	for word in dictionary:
		distance = fuzz.ratio(string, word)
		print("word: " + word + " distance: " + str(distance))
		if distance > closest_ratio:
			closest_ratio = distance
			closest_string = word
	return closest_string

def main():
  closest_string = find_closest_string("appl")
  print("closest string: " + closest_string)
  
if __name__== "__main__":
  main()

