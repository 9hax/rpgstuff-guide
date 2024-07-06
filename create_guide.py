# This Script creates a complete guide to the RPGStuff Minecraft Plugin by 420kekscope.
# Written with love by lyheart

import json
import traceback
import sys
import math
from glob import glob

def run():
    parse_recipes()
    create_recipe_snippets()
    build_page()
    #publish()


recipe_list = []

recipe_snippets = []

def parse_recipes():
    # Error checking? We.. don't do that here.

    try:
        with open("recipes.json", 'r') as recipefile:
            recipes = json.loads(recipefile.read())
    except:
        print("There was an error loading the recipe file. Please check the error output, fix the recipes.json file and try again.")
        print(traceback.format_exc())
        exit(1)
    
    known_items = []

    known_items.extend(recipes.keys())
    for recipe in recipes.keys():
        # We'll be looking for all items so we can check for assets later.
        if type(recipes[recipe]) == str:
            continue
        else:
            for item in recipes[recipe][0]:
                if item not in known_items:
                    known_items.append(item)
    
    # Check if all assets exist
    check_assets(known_items)

    unify_recipe_list(recipes)
    

def unify_recipe_list(recipes):
    # Translate the recipe list into a unified format.
    for recipe in recipes.keys():
        new_recipe = {}
        new_recipe["title"] = recipe
        # Simple Description
        if type(recipes[recipe]) == str:
            new_recipe["description"] = recipes[recipe]
            new_recipe["recipe"] = None
        else:
            flat_recipe = recipes[recipe]
            new_recipe["recipe"] = expand_recipe(flat_recipe[0], flat_recipe[1])
            if len(flat_recipe) > 2:
                new_recipe["description"] = flat_recipe[2]
        recipe_list.append(new_recipe)


def expand_recipe(materials: list, slots: str):
    slots = [int(x) if x != " " else "air" for x in list(slots)]
    sublist_size = int(math.sqrt(len(slots)))
    for slot in range(0, len(slots)):
        slots[slot] = materials[slots[slot]] if slots[slot] != "air" else "air"
    slots = [slots[i:i + sublist_size] for i in range(0, len(slots), sublist_size)]
    # print(slots)
    return slots


def check_assets(known_items: list):
    # Check for existence of assets

    item_assets = glob("itemassets/*")
    item_assets = list(item_assets)

    # Print the glob of all known items for debug purposes.
    # print(item_assets)

    assetPrefix = "itemassets/"
    if sys.platform == "win32": assetPrefix = "itemassets\\"
    for item in list(known_items):
        assetPath = assetPrefix + item + ".png"
        if assetPath not in item_assets:
            print(f"WARNING! Missing asset {assetPath} for item {item}!")
    

def create_recipe_snippets():
    for item in recipe_list:
        if not item['recipe']:
            snippet = str(descriptionTemplate)
        else:
            snippet = ''''''
            for row in item['recipe']:
                snippet = snippet + '''<span class="mcui-row">'''
                for slot in row:
                    if slot == 'air':
                        snippet = snippet + '''<span class="invslot"> </span>'''
                    else:
                        slothtml = str(slotTemplate)
                        slothtml = slothtml.replace("ITEMID", slot.lower().replace(" ",""))
                        slothtml = slothtml.replace("ITEM", slot)
                        snippet = snippet + slothtml
                snippet = snippet + '</span>'
            snippet = recipeTemplate.replace("RECIPE", snippet)
        snippet = snippet.replace("TITLEID", item['title'].lower().replace(" ", ""))
        snippet = snippet.replace("TITLE", item['title'])
        if 'description' in item.keys():
            # print("Found description")
            snippet = snippet.replace("DESCRIPTION", item['description'])
        else:
            snippet = snippet.replace("DESCRIPTION", "")
        recipe_snippets.append(snippet)
    # print(recipe_snippets)


def build_page():
    fileContent = str(startTemplate)
    for snippet in recipe_snippets:
        fileContent += snippet
    fileContent += str(endTemplate)
    with open("index.html", "w") as guidefile:
        guidefile.write(fileContent)


descriptionTemplate = '''
    <div id="TITLEID">
      <span class="mcui mcui-Crafting_Table pixel-image">
        TITLE<br />
        <div class="description">DESCRIPTION</div><br />
        <span class="mcui-output">
          <span class="invslot invslot-large">
            <span class="invslot-item invslot-item-image">
              <a href="#TITLEID" title="TITLE" class="minetext">
                <img
                  src="itemassets/TITLE.png"
                  width="32"
                  height="32"
                />
              </a>
              <!--<span class="invslot-stacksize">1</span>-->
            </span>
          </span>
        </span>
      </span>
    </div>'''


recipeTemplate = '''
    <div id="TITLEID">
      <span class="mcui mcui-Crafting_Table pixel-image">
        TITLE<br />
        <div class="description">DESCRIPTION</div><br>
        <span class="mcui-input">
          RECIPE
        </span>
        <span class="mcui-arrow"><br /></span>
        <span class="mcui-output">
          <span class="invslot invslot-large">
            <span class="invslot-item invslot-item-image">
              <a href="#TITLEID" title="TITLE" class="minetext">
                <img
                  src="itemassets/TITLE.png"
                  width="32"
                  height="32"
                />
              </a>
              <!--<span class="invslot-stacksize">1</span>-->
            </span>
          </span>
        </span>
      </span>
    </div>'''

slotTemplate = '''<span class="invslot"><span class="invslot-item invslot-image-item"><a href="#ITEMID" title="ITEM" class="minetext"><img src="itemassets/ITEM.png" width="32" height="32" /></a></span></span>'''


startTemplate = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>RPGStuff Crafting recipe overview</title>
    <link rel="stylesheet" href="css/main.css" />
  </head>

  <body>
    <center><h1> RPGStuff Crafting and Item Guide - by 9hax </h1></center><br>
    <div id="minetip-tooltip" style="display: none">
      <span class="minetip-title" id="minetip-text">Minecraft Tip</span>
    </div>
    <div class="collection">'''

endTemplate = '''</div></body>
  <script src="css/minetip.js" defer></script>
</html>
'''


if __name__ == "__main__":
    run()