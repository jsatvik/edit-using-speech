import re
import nltk
import time
import speech_recognition as sr
import webcolors
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageColor
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from word2number import w2n

nltk.download("stopwords")
nltk.download('punkt')
nltk.download('wordnet')

r = sr.Recognizer()

image = Image.open("C:\\Users\\91773\\Pictures\\catfortesting.jpg")  # Replace with the path to your image
image.show()

stop_words = set(stopwords.words('english'))

stop_flag = False

while not stop_flag:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)

        print("Say anything: ")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("Recognized Text:", text)
        except sr.UnknownValueError:
            print("Sorry, could not recognize")
            continue

    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

    # Rotate function
    rotate_synonyms = set()
    for syn in wordnet.synsets("rotate"):
        for lemma in syn.lemmas():
            rotate_synonyms.add(lemma.name().lower())

    # Check if any of the rotate synonyms are in the filtered sentence
    if any(word in rotate_synonyms for word in filtered_sentence):
        degrees = None
        direction = None
        for word in filtered_sentence:
            if word.isdigit():
                degrees = int(word)
            if "right" in word:
                direction = "right"
            elif "left" in word:
                direction = "left"
        if degrees is None:
            print("No degree specified")
        else:
            if direction == "right":
                degrees = 360 - degrees
            image = image.rotate(degrees)
            print("Image rotated by", degrees, "degrees to the", direction)
            image.show()
            image.save("altered_image.jpg")  # Save the altered image

    # Blur function
    elif "blur" in filtered_sentence:
        blur_radius = None
        for word in filtered_sentence:
            if word.isdigit():
                blur_radius = int(word)
                break
            try:
                blur_radius = w2n.word_to_num(word)
                break
            except ValueError:
                pass
        if blur_radius is not None:
            image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            print("Image blurred with a radius of", blur_radius)
            image.show()
            image.save("altered_image.jpg")  # Save the altered image
        else:
            print("No blur radius specified")

    # Grayscale function
    elif "grayscale" in filtered_sentence:
        image = ImageOps.grayscale(image)
        print("Image converted to grayscale")
        image.show()
        image.save("altered_image.jpg")  # Save the altered image

    # Brightness function
    elif "brightness" in filtered_sentence:
        brightness_level = None
        for word in filtered_sentence:
            if word.isdigit():
                brightness_level = int(word)
                break
            try:
                brightness_level = w2n.word_to_num(word)
                break
            except ValueError:
                pass
        if brightness_level is not None:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_level / 10)
            print("Image brightness enhanced to level", brightness_level)
            image.show()
            image.save("altered_image.jpg")  # Save the altered image
        else:
            print("No brightness level specified")

    # Contrast function
    elif "contrast" in filtered_sentence:
        contrast_level = None
        for word in filtered_sentence:
            if word.isdigit():
                contrast_level = int(word)
                break
            try:
                contrast_level = w2n.word_to_num(word)
                break
            except ValueError:
                pass
        if contrast_level is not None:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast_level / 10)
            print("Image contrast enhanced to level", contrast_level)
            image.show()
            image.save("altered_image.jpg")  # Save the altered image
        else:
            print("No contrast level specified")

    # Sharpen function
    elif "sharpen" in filtered_sentence:
        image = image.filter(ImageFilter.SHARPEN)
        print("Image sharpened")
        image.show()
        image.save("altered_image.jpg")  # Save the altered image

    # Colorize function
    elif any(keyword in filtered_sentence for keyword in ["color", "colour"]):
        color_name = None
        for word in filtered_sentence:
            if word.isalpha():
                color_name = word.lower()
                break
        if color_name:
            try:
                color_rgb = webcolors.name_to_rgb(color_name)
                image = ImageOps.colorize(image.convert("L"), color_rgb, "#000000")
                print("Image colored with", color_name)
                image.show()
                image.save("altered_image.jpg")  # Save the altered image
            except ValueError:
                print("Invalid color name specified")
        else:
            print("No color name specified")
    
    # Enhance sharpness function
    elif "enhance sharpness" in filtered_sentence:
        sharpness_level = None
        for word in filtered_sentence:
            if word.isdigit():
                sharpness_level = int(word)
                break
            try:
                sharpness_level = w2n.word_to_num(word)
                break
            except ValueError:
                pass
        if sharpness_level is not None:
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(sharpness_level / 10)
            print("Image sharpness enhanced to level", sharpness_level)
            image.show()
            image.save("altered_image.jpg")  # Save the altered image
        else:
            print("No sharpness level specified")

    # Resize with aspect ratio function
    elif "resize with aspect ratio" in filtered_sentence:
        new_width = None
        for word in filtered_sentence:
            if word.isdigit():
                new_width = int(word)
                break
            try:
                new_width = w2n.word_to_num(word)
                break
            except ValueError:
                pass
        if new_width is not None:
            width_percent = (new_width / float(image.size[0]))
            new_height = int((float(image.size[1]) * float(width_percent)))
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
            print("Image resized with new width:", new_width)
            image.show()
            image.save("altered_image.jpg")  # Save the altered image
        else:
            print("No new width specified")

    stop = input("Would you like to stop editing? (Y/N) ")
    time.sleep(5)
    if stop.lower() == "y":
        stop_flag = True
