#Allows for you to speak text through your default screen reader.
from accessible_output2 import outputs
def speak(text, interrupt=False):
	speaker = outputs.auto.Auto()
	speaker.speak(text, interrupt)