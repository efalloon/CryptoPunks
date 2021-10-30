"""
Created By Euan Traynor, 2021
View Euan's Github repo: https://github.com/efalloon/CryptoPunks
Ensure that the below following libraries are installed...
"""

import os
import bisect
import random
from PIL import Image, ImageOps

glassesDict = {'1': 50, '2': 10, '3': 15, '4': 75, '5': 90, '6': 65, '7': 5, '8': 5, '9': 25, '10': 1}
hairsDict = {'2': 15, '3': 20, '4': 30, '5': 30, '6': 15, '7': 65, '8': 55, '9': 25, '10': 5}
beardsDict = {'1': 90, '2': 5, '3': 20, '4': 30, '6': 15, '7': 65, '8': 10, '9': 5, '10': 1}
hatsDict = {'1': 80, '2': 50, '3': 40, '4': 20, '5': 70, '6': 20, '7': 5, '8': 5, '9': 15, '10': 5}
accessoriesDict = {'1': 5, '2': 75, '4': 25, '5': 10}
typesDict = {'person': 75, 'ape': 25, 'alien': 5, 'zombie': 35}

class WeightedTuple(object):
    def __init__(self, items):
        self.indexes = []
        self.items = []
        next_index = 0
        for key in sorted(items.keys()):
            val = items[key]
            self.indexes.append(next_index)
            self.items.append(key)
            next_index += val
        self.len = next_index

    def __getitem__(self, n):
        if n < 0:
            n = self.len + n
        if n < 0 or n >= self.len:
            raise IndexError

        idx = bisect.bisect_right(self.indexes, n)
        return self.items[idx-1]

    def __len__(self):
        return int(self.len)

def tint_image(src, color="#FFFFFF"):
    src.load()
    r, g, b, alpha = src.split()
    gray = ImageOps.grayscale(src)
    result = ImageOps.colorize(gray, (0, 0, 0, 0), color) 
    result.putalpha(alpha)
    return result

def generate_color():
    color = '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))
    return color

def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    return "#" + "".join([hex(int(i))[2:] for i in new_rgb_int])

def generatePerson():
    rareCount = 0

    skinTones = ["#c58c85", "#ecbcb4", "#d1a3a4", "#a1665e", "#503335", "#592f2a", "#ffdbac", "#f1c27d", "#e0ac69", "#c68642", "#8d5524", "#ECC6A9", "#593010"]
    glasses = WeightedTuple(glassesDict)
    hairs = WeightedTuple(hairsDict)
    beards = WeightedTuple(beardsDict)
    hats = WeightedTuple(hatsDict)
    accessories = WeightedTuple(accessoriesDict)
    types = WeightedTuple(typesDict)
    species = random.choice(types)

    background = Image.open("./parts/area_51.png")
    background = tint_image(background, "#7122DB") #generate_color()) #color_variant(generate_color(), 0.5))
    background.putalpha(0)

    skinTone = random.choice(skinTones)

    if species == "ape":
        skin = Image.open("./parts/skin_2.png")
        outline = Image.open("./parts/outline_2.png")
        eyebrows = Image.open("./parts/eyebrows_2.png")
        nose = Image.open("./parts/nose_1.png")
    elif species == "alien":
        skin = Image.open("./parts/skin_3.png")
        outline = Image.open("./parts/outline_3.png")
        eyebrows = Image.open("./parts/eyebrows_3.png")
        nose = Image.open("./parts/nose_3.png")
    elif species == "zombie":
        skin = Image.open("./parts/skin_4.png")
        outline = Image.open("./parts/outline_1.png")
        eyebrows = Image.open("./parts/eyebrows_4.png")
        nose = Image.open("./parts/nose_1.png")
    else:
        skin = Image.open("./parts/skin_1.png")
        skin = tint_image(skin, skinTone)
        outline = Image.open("./parts/outline_1.png")
        eyebrows = Image.open("./parts/eyebrows_1.png")
        eyebrows = tint_image(eyebrows, color_variant(skinTone, random.uniform(0.3, 0.75)))
        nose = Image.open("./parts/nose_1.png")
    
    hair = Image.open(f"./parts/hairs/hair_{random.choice(hairs)}.png")
    if random.choice(WeightedTuple({'colourful': 50, 'normal': 50})) == "colourful":
        hair = tint_image(hair, generate_color())
    else:
        hair = tint_image(hair, color_variant(skinTone, random.uniform(0.3, 0.75)))
    
    glassesType = random.choice(glasses)
    glasses = Image.open(f"./parts/glasses/glasses_{glassesType}.png")
    eyes = Image.open("./parts/eyes_1.png")
    hatType = random.choice(hats)
    hat = Image.open(f"./parts/hats/hat_{hatType}.png")

    beard = Image.open(f"./parts/beards/beard_{random.choice(beards)}.png")
    beard = tint_image(beard, color_variant(skinTone, random.uniform(0.3, 0.75)))
    mouth = Image.open("./parts/mouth_1.png")

    background.paste(skin, (0, 0), skin)
    background.paste(outline, (0, 0), outline)
    background.paste(eyes, (0, 0), eyes)
    background.paste(eyebrows, (0, 0), eyebrows)
    if species != "ape":
        if random.choice(WeightedTuple({'true': 70, 'false': 30})) == "true" and species != "alien":
            background.paste(beard, (0, 0), beard)
        background.paste(nose, (0, 0), nose)
        background.paste(mouth, (0, 0), mouth)

    if random.choice(WeightedTuple({'true': 50, 'false': 50})) == "true":
        background.paste(glasses, (0, 0), glasses)

    # if species != "zombie":
    if random.choice(WeightedTuple({'hat': 50, 'hair': 50})) == "hat" or species == "ape" or species == "alien":
        background.paste(hat, (0, 0), hat)
    else:
        if species == "person" or species == "alien":
            if random.choice(WeightedTuple({'true': 80, 'false': 20})) == "true":
                background.paste(hair, (0, 0), hair)
            else:
                if species != "zombie":
                    hairShine = Image.open(f"./parts/hairs/hair_1.png")
                    background.paste(hairShine, (0, 0), hairShine)
    
    if species == "zombie":
        drool = Image.open("./parts/accessories/accessory_3.png")
        background.paste(drool, (0, 0), drool)
    
    accessoryType = random.choice(accessories)
    if random.choice(WeightedTuple({'true': 25, 'false': 75})) == "true":
        accessory = Image.open(f"./parts/accessories/accessory_{accessoryType}.png")
        background.paste(accessory, (0, 0), accessory)

    if typesDict[species] <= 5:
        rareCount += 1
    if glassesDict[glassesType] <= 5:
        rareCount += 1
    if hatsDict[hatType] <= 5:
        rareCount += 1
    if accessoriesDict[accessoryType] <= 5:
        rareCount += 1
    
    # rareCount = 1

    backgroundColour = Image.open("./parts/area_51.png")
    if rareCount == 0:
        backgroundColour = tint_image(backgroundColour, "#7122DB")
    elif rareCount == 1:
        backgroundColour = tint_image(backgroundColour, "#b25dba")
    elif rareCount == 2 or rareCount == 3:
        backgroundColour = tint_image(backgroundColour, "#4eb5b2")
    elif rareCount == 4:
        backgroundColour = tint_image(backgroundColour, "#e67665")

    backgroundColour.paste(background, (0, 0), background)

    # background = tint_image(background, "#a3f6ff")
    # for sword in range(0.0000001,0.9999999):
    #     if sword == float(0.0720416):
    #         background = tint_image(background, "#a2a2d0")

    return backgroundColour

    # return background

# os.system('clear')
count = int(input("Generate how many?: "))
for i in range(0, count):
    generatePerson().save(f'people/cryptopunk_{i}.png',"PNG")

# # resize the image
# size = (480,480)
# background = background.resize(size,Image.ANTIALIAS)
