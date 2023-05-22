# Tasks stack 'n track (WIP)

Create simple tasks or "stackable" tasks, scroll through them or drag & drop them in the temporary workbench (lost if you refresh or quit the page). If you drag & drop multiple stackable tasks, their properties will sum up.

Check the "done" checkbox to keep track of what you've done, or delete existing tasks.

Editing an existing task can currently only be done directly in the corresponding json file.

You can also get the json data you need from other sources if you can find it and don't want to handle data creation yourself.

# Requirements

* npm, Node.js
* React.js
* Flask
* bs4 (to be removed, no longer used)

# Getting Started
* Clone this repository.
* Navigate to the project directory.
* Install the necessary packages.
* Create a `DATABASE` folder inside the `backend/db` folder. Then create any sub-folder in it : it can be the name of a game you're playing, a fitness goal, any global kind of goal.
* Run the Flask server (`backend/main.py`).
* Run the React application (`frontend/`).
* Start creating items and name their category. A button will appear for each category you've created if you wish to filter by category. It can be a kind of game quest, a cooking recipe category, a kind of house chores...

# Examples of using the stackable elements

## Cooking Example:
Suppose you're planning a dinner party and you're going to **cook multiple dishes**, each with their own set of ingredients. You could use stackables to create a grocery list by stacking your recipes in the workbench. This would calculate the **total quantity of each ingredient you'll need for your shopping trip**. Here is how it might look:

```
Recipe: "Lasagna"
Key: "Lasagna Noodles (grams)", Value: "200"
Key: "Ground Beef (lbs)", Value: "2"
Key: "Ricotta Cheese (oz)", Value: "15"
...
Recipe: "Caesar Salad"
Key: "Romaine Lettuce (head)", Value: "1"
Key: "Parmesan Cheese (cup)", Value: "0.5"
...
```

Then you can stack these recipes and Stackable will calculate the total for each ingredient. For example, if another recipe also requires "Parmesan Cheese", you can stack it on the existing element in the workbench, and the quantities will be updated.

## Video Game Armor Upgrade Example:
If you're planning to **upgrade multiple pieces of armor** in your RPG, each with their own material requirements, you could use stackables to determine the total amount of each material you'll need. Here is how it might look:

```
Armor Upgrade: "Dragonplate Armor"
Key: "Dragon Bones", Value: "5"
Key: "Dragon Scales", Value: "3"
Key: "Ebony Ingots", Value: "2"
...
Armor Upgrade: "Ebony Armor"
Key: "Ebony Ingots", Value: "5"
Key: "Leather Strips", Value: "4"
...
```

You can stack these armor upgrades in the workbench and the total for each material will be displayed in a single element, making it easy to see what you'll need to gather for your upgrades.

This way, stackables can help you aggregate materials or ingredients across multiple items or projects, streamlining your planning and preparation process. You could also use it to sum up required number of days or hours for several goals, to calculate calory intakes...
