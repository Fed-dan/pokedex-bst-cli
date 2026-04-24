import csv

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):

    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input.")

def get_poke_dict_by_id(poke_id):
    if 0 < poke_id < 136:
        for pokemon in HOENN_DATA:
            if pokemon["ID"] == poke_id:
                return pokemon
            
    print("ID ", poke_id, " not found in Honen data.")
    return None

def get_poke_dict_by_name(name):
    for pokemon in HOENN_DATA:
        if pokemon["Name"] == name:
            return pokemon
    
    return None

def display_pokemon_list(poke_list):
    if not poke_list: print("There are no Pokemons in this Pokedex that match the criteria.")
    for pokemon in poke_list:
            evolve = "FALSE"
            if pokemon["Can Evolve"]: evolve = "TRUE"
            print(f"ID: {pokemon['ID']}, Name: {pokemon['Name']}, Type: {pokemon['Type']}, "
                  f"HP: {pokemon['HP']}, Attack: {pokemon['Attack']}, Can Evolve: {evolve}")
        


########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon=None):
    if first_pokemon: pokedex = [first_pokemon]
    else: pokedex = []

    node = {"owner": owner_name, "pokedex": pokedex, "left": None, "right": None}

    return node
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """

def insert_owner_bst(root, new_node):
    if not root:
        return new_node
    if new_node["owner"] < root["owner"]:  
        root["left"] = insert_owner_bst(root["left"], new_node)
    else:
        root["right"] = insert_owner_bst(root["right"], new_node)

    return root

    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
def find_owner_bst(root, owner_name):

    
    if root is None:
        return None
    
    lower_name = owner_name.lower()
    root_lower = root["owner"].lower()

    if root_lower == lower_name: 
        return root
    elif root_lower > lower_name:
        return find_owner_bst(root["left"], owner_name)
    else:
        return find_owner_bst(root["right"], owner_name)

    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    

def min_node(node):
    while (node["left"]):
        node = node["left"]
    return node
    """
    Return the leftmost node in a BST subtree.
    """
    
def delete_owner_bst(root, owner_name):
    lower_name = owner_name.lower()
    root_lower = root["owner"].lower()

    if root == None: return None

    if root_lower == lower_name:
        if not root["left"] and not root["right"]:
            return None
        
        elif not root["left"] and root["right"]:
            return root["right"]
        
        elif root["left"] and not root["right"]:
            return root["left"]
        
        else:
            temp = min_node(root["right"])

            root["owner"] = temp["owner"]
            root["pokedex"] = temp["pokedex"]

            root["right"] = delete_owner_bst(root["right"], temp["owner"])

    elif root["owner"] > owner_name:
        root["left"] = delete_owner_bst(root["left"], owner_name)
    else:
        root["right"] = delete_owner_bst(root["right"], owner_name)
        
    return root
    """
    Remove a node from the BST by owner_name. Return updated root.
    """


########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    list = []
    list.append(root)

    while list:
        temp = list.pop(0)
        print(f"Owner: {temp['owner']}")
        display_pokemon_list(temp["pokedex"])

        if temp["left"]:
            list.append(temp["left"])
        if temp["right"]:
            list.append(temp["right"])
        


    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    

def pre_order(root):
    if root == None: return

    print(f"Owner: {root['owner']}")
    display_pokemon_list(root["pokedex"])

    pre_order(root["left"])
    pre_order(root["right"])


    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    

def in_order(root):
    if root == None: return

    in_order(root["left"])

    print(f"Owner: {root['owner']}")
    display_pokemon_list(root["pokedex"])

    in_order(root["right"])
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    

def post_order(root):
    if root == None: return

    post_order(root["left"])
    post_order(root["right"])

    print(f"Owner: {root['owner']}")
    display_pokemon_list(root["pokedex"])
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    id = read_int_safe("Enter Pokemon ID to add: ")
    new_pokemon = get_poke_dict_by_id(id)
    if not new_pokemon: 

        return

    pokedex = owner_node["pokedex"]
    for pokemon in pokedex:
        if pokemon["Name"] == new_pokemon["Name"]:
            print("Pokemon already in the list. No changes made.")
            return
    print(f"Pokemon {new_pokemon['Name']} (ID {id}) added to {owner_node['owner']}'s Pokedex.")
    owner_node["pokedex"].append(new_pokemon)

    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    


def release_pokemon_by_name(owner_node):
    name = input("Enter Pokemon Name to release: ")
    pokemon__to_delete = get_poke_dict_by_name(name)
    if not pokemon__to_delete in owner_node["pokedex"]: 
        print(f"No Pokemon named '{name}' in {owner_node['owner']}'s Pokedex.")
        return

    temp = []
    for pokemon in owner_node["pokedex"]:
        if pokemon["Name"] != name:
            temp.append(pokemon)
    owner_node["pokedex"] = temp
    
    print(f"Releasing {name} from {owner_node['owner']}.")
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    

def evolve_pokemon_by_name(owner_node):
    name = input("Enter Pokemon Name to evolve: ")
    pokemon__to_evovle = get_poke_dict_by_name(name)

    if  pokemon__to_evovle not in owner_node["pokedex"] or not pokemon__to_evovle: 
        print(f"No Pokemon named '{name}' in {owner_node['owner']}'s Pokedex.")
        return
    
    if pokemon__to_evovle["Can Evolve"] == "FALSE":
        print(f"{name} cannot evolve.")
        return
    
    temp = []
    for pokemon in owner_node["pokedex"]:
        if pokemon["Name"] != name:
            temp.append(pokemon)
    owner_node["pokedex"] = temp

    evolve_pokemon = get_poke_dict_by_id(pokemon__to_evovle['ID']+1)


    print(f"Pokemon evolved from {name} (ID {pokemon__to_evovle['ID']}) to {evolve_pokemon['Name']} (ID {evolve_pokemon['ID']}).")

    if (evolve_pokemon in owner_node['pokedex']):
        print(f"{pokemon__to_evovle['Name']} was already present; releasing it immediately.")
        return

    owner_node["pokedex"].append(evolve_pokemon)

    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    if not root:  
        return arr

    arr.append(root)

    if root.get("left"): 
        gather_all_owners(root["left"], arr)

    if root.get("right"):  
        gather_all_owners(root["right"], arr)

    return arr

def sort_owners_by_num_pokemon():
    list = gather_all_owners(ownerRoot, [])
    if not list:
        print("No owners at all.")
        return

    print("=== The Owners we have, sorted by number of Pokemons ===")
    
    sorted = False
    while(not sorted):
          sorted = True
          for i in range(len(list)-1):
                if len(list[i]["pokedex"]) > len(list[i+1]["pokedex"]):
                  list[i], list[i+1] = list[i+1], list[i]
                  sorted = False
                if len(list[i]["pokedex"]) == len(list[i+1]["pokedex"]):
                  if (list[i]["owner"].lower() > list[i+1]["owner"].lower()):
                    list[i], list[i+1] = list[i+1], list[i]
                    sorted = False


              

    for owner in list:
        print(f"Owner: {owner['owner']} (has {len(owner['pokedex'])} Pokemon)")


    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    


########################
# 6) Print All
########################

def print_all_owners():
    if not ownerRoot:
        print("No owners in the BST.")
        return
    

    print("""1) BFS
2) Pre-Order
3) In-Order
4) Post-Order""")
    choice = read_int_safe("Your choice: ")
    print()

    if not 0<choice<5: 
        print("Invalid choice.")
        return
    
    if choice == 1: bfs_traversal(ownerRoot)
    if choice == 2: pre_order(ownerRoot)
    if choice == 3: in_order(ownerRoot)
    if choice == 4: post_order(ownerRoot)

    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    

# def bfs_print(node):     
#     bfs_traversal(node)

# def pre_order_print(node):
#     pre_order(node)

#     """
#     Helper to print data in pre-order.
#     """
#     pass

# def in_order_print(node):
#     in_order(node)
#     """
#     Helper to print data in in-order.
#     """
#     pass

# def post_order_print(node):
#     post_order(node)
#     """
#     Helper to print data in post-order.
#     """
#     pass


########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    choice = -1

    while choice!=7:
        print("-- Display Filter Menu --")
        print("""
        1. Only a certain Type
        2. Only Evolvable
        3. Only Attack above __
        4. Only HP above __
        5. Only names starting with letter(s)
        6. All of them!
        7. Back
        """)
        choice = read_int_safe("Your choice: ")

        if choice==1: 
            type = input("Which Type? (e.g. GRASS, WATER): ") 
            
            temp = []
            for pokemon in owner_node["pokedex"]:
                if pokemon["Type"] == type:
                    temp.append(pokemon)
            display_pokemon_list(temp)
        elif choice==2: 
            
            temp = []
            for pokemon in owner_node["pokedex"]:
                if pokemon["Can Evolve"] == "TRUE":
                    temp.append(pokemon)
            display_pokemon_list(temp)    
        elif choice==3: 
            Attack = read_int_safe("Enter Attack threshold: ")

            temp = []
            for pokemon in owner_node["pokedex"]:
                if pokemon["Attack"] > Attack:
                    temp.append(pokemon)
            display_pokemon_list(temp)   

        elif choice==4: 
            HP = read_int_safe("Enter Attack threshold: ")

            temp = []
            for pokemon in owner_node["pokedex"]:
                if pokemon["HP"] > HP:
                    temp.append(pokemon)
            display_pokemon_list(temp)  

        elif choice==5: 
            letter = input("Starting letter(s): ")   

            temp = []
            for pokemon in owner_node["pokedex"]:
                if pokemon["Name"][:len(letter)] == letter:
                    temp.append(pokemon)
            display_pokemon_list(temp)  
        elif choice==6: display_pokemon_list(owner_node["pokedex"])    
        elif choice==7: 
            print("Back to Pokedex Menu.")
            return
        else: print("Invalid choice.")



########################
# 8) Sub-menu & Main menu
########################

def existing_pokedex():

    if not ownerRoot:
        print("No owners at all.")
        return
    
    owner_name = input("Owner name: ")
    
    owner_node = find_owner_bst(ownerRoot, owner_name)
    if not owner_node:
        print(f"Owner '{owner_name}' not found.")
        return
    
    while True:
        print(f"""-- {owner_name.lower()}'s Pokedex Menu --
1. Add Pokemon
2. Display Pokedex
3. Release Pokemon
4. Evolve Pokemon
5. Back to Main""")
        choice = read_int_safe("Your choice: ")

        if choice == 1:
            add_pokemon_to_owner(owner_node)
        elif choice == 2:
            display_filter_sub_menu(owner_node)
        elif choice == 3:
            release_pokemon_by_name(owner_node)
        elif choice == 4:
            evolve_pokemon_by_name(owner_node)
        elif choice == 5:
            print("Returning to the main menu.")
            return
        else:
            print("Invalid choice.")



    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """
    pass

def main_menu():
    global ownerRoot

    print("""=== Main Menu ===
1. New Pokedex
2. Existing Pokedex
3. Delete a Pokedex
4. Display owners by number of Pokemon
5. Print All
6. Exit""")
    option = read_int_safe("Your choice: ")
    
    while option != 6:
        if option == 1: 
            owner_name = input("Owner name: ")
            if not owner_name:
                pass
            elif find_owner_bst(ownerRoot,owner_name):
                print(f"Owner '{owner_name}' already exists. No new Pokedex created.")
                option=-1
                continue
            print("Choose your starter Pokemon:")
            print("1) Treecko")
            print("2) Torchic")
            print("3) Mudkip")

            starter_choice = read_int_safe("Your choice: ")

            if starter_choice == 1:
                starter_pokemon = get_poke_dict_by_name("Treecko")
            elif starter_choice == 2:
                starter_pokemon = get_poke_dict_by_name("Torchic")
            elif starter_choice == 3:
                starter_pokemon = get_poke_dict_by_name("Mudkip")
            else:
                print("Invalid. No new Pokedex created.")
                option = -1
                continue

            owner_node = create_owner_node(owner_name, starter_pokemon)            
            ownerRoot = insert_owner_bst(ownerRoot, owner_node)

            print(f"New Pokedex created for {owner_name} with starter {starter_pokemon['Name']}.")

        elif option == 2: existing_pokedex()
        elif option == 3: 

            if not ownerRoot:
                print("No owners to delete.")
                
            else:
                name_to_delete = input("Enter owner to delete:")  
                owner_node_to_delete = find_owner_bst(ownerRoot, name_to_delete)

                if not owner_node_to_delete:
                    print(f"Owner '{name_to_delete}' not found.")
                else:

                    ownerRoot = delete_owner_bst(ownerRoot, name_to_delete)
                    print(f"Deleting {name_to_delete}'s entire Pokedex...")
                    print("Pokedex deleted.")
        elif option == 4: sort_owners_by_num_pokemon()

        elif option == 5: print_all_owners()

        else:
            print("Invalid choice.")

        
        print("""=== Main Menu ===
1. New Pokedex
2. Existing Pokedex
3. Delete a Pokedex
4. Display owners by number of Pokemon
5. Print All
6. Exit""")
        option = read_int_safe("Your choice: ")

    return

def main():
    main_menu()
    """
    Entry point: calls main_menu().
    """
    pass

if __name__ == "__main__":

    main()
