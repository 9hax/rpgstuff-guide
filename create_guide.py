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
            snippet = ''
            materials = " ".join([*set(m.replace('_', ' ') for r in item['recipe'] for m in r)])
            size = "3x3" if len(item['recipe']) == 3 else "2x2"
            for row in item['recipe']:
                snippet = snippet
                for slot in row:
                    if slot == 'air':
                        snippet = snippet + '<div class="invslot"></div>'
                    else:
                        slothtml = str(slotTemplate)
                        slothtml = slothtml.replace("ITEMID", slot.lower().replace(" ",""))
                        slothtml = slothtml.replace("ITEMNAME", slot.replace('_', ' ').title())
                        slothtml = slothtml.replace("ITEM", slot)
                        snippet = snippet + slothtml
                snippet = snippet
            snippet = recipeTemplate.replace("RECIPE", snippet)
            snippet = snippet.replace("SIZE", size)
            snippet = snippet.replace("MATERIALS", materials)

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
    <article id="TITLEID" class="recipe" data-search="TITLE">
      <h2>TITLE</h2>
      <p class="recipe-description">DESCRIPTION</p>
      <div class="mcui">
        <div class="mcui-output">
          <div class="invslot invslot-large">
            <a href="#TITLEID" title="TITLE" class="invslot-image minetext">
                <img
                  src="itemassets/TITLE.png"
                  width="32"
                  height="32"
                />
            </a>
            <span class="invslot-text"></span>
          </div>
      </div>
    </article>'''


recipeTemplate = '''
    <article id="TITLEID" class="recipe" data-search="TITLE MATERIALS">
      <h2>TITLE</h2>
      <p class="recipe-description">DESCRIPTION</p>
      <div class="mcui">
        <div class="mcui-input input-SIZE">
          RECIPE
        </div>
        <div class="mcui-arrow"><span class="arr"></span></div>
        <div class="mcui-output">
          <div class="invslot">
            <a href="#TITLEID" title="TITLE" class="invslot-image minetext">
                <img
                  src="itemassets/TITLE.png"
                  width="32"
                  height="32"
                />
            </a>
            <span class="invslot-text"></span>
          </div>
      </div>
    </article>'''

slotTemplate = '''<div class="invslot"><a href="#ITEMID" title="ITEMNAME" class="invslot-image minetext"><img src="itemassets/ITEM.png" width="32" height="32" /></a><span class="invslot-text"></span></div>'''


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
    <h1>RPGStuff Crafting and Item Guide - by <a href="https://9h.ax">9hax</a></h1>
    <div class="search">
        <input id="search-form" class="search-input" placeholder="Enter something to search...">
    </div>
    <div id="minetip-tooltip" style="display: none">
      <span class="minetip-title" id="minetip-text">Minecraft Tip</span>
    </div>
    <div class="collection">'''

endTemplate = '''</div></body>
  <script src="css/minetip.js" defer></script>
  <script src="css/search.js" defer></script>
</html>
'''


if __name__ == "__main__":
    run()