from world.map import load_tree_from_yaml
from entities.main_character import MainCharacter
from entities.ghoul import GhoulInteraction


def run():
	try:
		root = load_tree_from_yaml("data/map.yaml")
	except FileNotFoundError:
		print("data/map.yaml not found. Create the map file at data/map.yaml")
		return
	except Exception as e:
		print("Failed to load map:", e)
		return

	node = root
	player = MainCharacter()
	visited = set()
	# per-node state (by id) for things like consecutive asks
	visited_state = {}
	print("Starting game. Type a direction name (e.g. 'straight', 'left', 'right') or 'q' to quit.")
	while True:
		print()
		print(node.description)
		if node.encounter:
			print(f"You encounter: {node.encounter}")
			# handle simple encounters
			nid = id(node)
			if node.encounter == "pot_of_gold" and nid not in visited:
				print("You found a pot of gold! You get 50 gold.")
				player.add_gold(50)
				visited.add(nid)
				print("Inventory:", player.inventory())
			elif node.encounter == "fire":
				# if player has a fire extinguisher, consume it and win
				if player.has_item("fire_extinguisher"):
					player.remove_item("fire_extinguisher")
					print("You use the fire extinguisher to put out the flames. You survive and win!")
					break
				else:
					print("The flames scorch you. This is the end.")
			elif node.encounter == "ghoul":
				# use a GhoulInteraction instance for dialogue; keep per-node state
				gh = GhoulInteraction()
				state = visited_state.setdefault(nid, {"consecutive_asks": 0, "revealed": False})
				gh.interact(player, state)
		if node.end:
			print("This node ends the game. Exiting.")
			break

		exits = list(node.children.keys())
		print("Exits:", ", ".join(exits) if exits else "(none)")
		choice = input("> ").strip().lower()
		if choice == "q":
			print("Quitting.")
			break
		# inventory commands
		if choice in ("i", "inventory"):
			print("Inventory:", player.inventory())
			continue
		if choice == "gold":
			print("Gold:", player.gold)
			continue
		if choice.startswith("take "):
			# take <item> (qty optional: 'take x 2')
			parts = choice.split()
			if len(parts) >= 2:
				item = parts[1]
				qty = int(parts[2]) if len(parts) >= 3 and parts[2].isdigit() else 1
				# check node items
				node_items = getattr(node, "items", {})
				avail = node_items.get(item, 0)
				if avail <= 0:
					print("There's no", item, "here to take.")
				else:
					take_qty = min(qty, avail)
					player.add_item(item, take_qty)
					node_items[item] = avail - take_qty
					if node_items[item] <= 0:
						del node_items[item]
					print(f"You take {take_qty} {item}.")
					print("Inventory:", player.inventory())
				continue
		if choice in node.children:
			node = node.children[choice]
		else:
			print("No exit that way.")


if __name__ == '__main__':
	run()
