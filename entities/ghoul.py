from typing import Dict
from entities.main_character import MainCharacter


class GhoulInteraction:
    """Encapsulates the ghoul dialogue/interaction.

    The interaction is stateful per-node. The caller should pass a mutable
    dict to hold state across multiple visits (e.g. visited_state[node_id]).
    """

    def interact(self, player: MainCharacter, state: Dict) -> None:
        # Ensure state keys exist
        state.setdefault("consecutive_asks", 0)
        state.setdefault("revealed", False)

        while True:
            print()
            print("A ghoul hangs above. What do you do?")
            print("1) Ask 'what is for sale?'")
            print("2) Say hello")
            print("3) Leave")
            choice = input("(1/2/3) > ").strip()
            if choice == "1":
                state["consecutive_asks"] += 1
                print("You ask: 'What is for sale?'")
                if state["consecutive_asks"] >= 3 and not state["revealed"]:
                    print("The ghoul finally speaks: 'Fine. I have a fire extinguisher for sale.'")
                    state["revealed"] = True
                elif not state["revealed"]:
                    print("The ghoul remains silent.")
            elif choice == "2":
                print("You say hello. The ghoul stares.")
                state["consecutive_asks"] = 0
            elif choice == "3":
                print("You step away from the ghoul.")
                break
            else:
                print("Choose 1, 2 or 3.")

            # if revealed, allow buying
            if state.get("revealed"):
                print("Do you want to buy the fire extinguisher for 20 gold? (y/n)")
                buy = input("> ").strip().lower()
                if buy == "y":
                    if player.gold >= 20:
                        player.add_gold(-20)
                        player.add_item("fire_extinguisher", 1)
                        print("You bought the fire extinguisher.")
                        print("Inventory:", player.inventory())
                    else:
                        print("You don't have enough gold.")
                    # After attempting to buy (or refusing), end dialogue
                    break
