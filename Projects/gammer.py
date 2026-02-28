import random
import time

class Entity:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

class Player(Entity):
    def __init__(self, name):
        super().__init__(name, health=100, attack=15)
        self.gold = 20
        self.potions = 2
        self.xp = 0

    def heal(self):
        if self.potions > 0:
            amount = 30
            self.health = min(self.max_health, self.health + amount)
            self.potions -= 1
            print(f"✨ You drank a potion! Health: {self.health}/{self.max_health}")
        else:
            print("❌ Out of potions!")

class Enemy(Entity):
    def __init__(self, name, health, attack, gold_drop):
        super().__init__(name, health, attack)
        self.gold_drop = gold_drop

def combat(player, enemy):
    print(f"\n⚔️ A wild {enemy.name} appeared!")
    
    while enemy.is_alive() and player.is_alive():
        print(f"\n{player.name}: {player.health} HP | {enemy.name}: {enemy.health} HP")
        action = input("Do you (A)ttack or (H)eal? ").lower()

        if action == 'a':
            damage = random.randint(player.attack - 5, player.attack + 5)
            enemy.health -= damage
            print(f"💥 You hit the {enemy.name} for {damage} damage!")
        elif action == 'h':
            player.heal()
        else:
            print("Invalid choice! You stumbled.")

        if enemy.is_alive():
            e_damage = random.randint(enemy.attack - 2, enemy.attack + 2)
            player.health -= e_damage
            print(f"🩸 The {enemy.name} deals {e_damage} damage to you!")
        
        time.sleep(0.5)

    if player.is_alive():
        print(f"✅ You defeated the {enemy.name}!")
        print(f"💰 You found {enemy.gold_drop} gold.")
        player.gold += enemy.gold_drop
        player.xp += 20
        return True
    else:
        print("💀 Game Over... You perished in the dungeon.")
        return False

def shop(player):
    print("\n🏪 Welcome to the Shop!")
    print(f"Gold: {player.gold} | Potions: {player.potions}")
    choice = input("Buy a Potion for 15 Gold? (y/n): ").lower()
    if choice == 'y':
        if player.gold >= 15:
            player.gold -= 15
            player.potions += 1
            print("🧪 Potion added to inventory!")
        else:
            print("Insufficient gold!")

def main():
    print("--- WELCOME TO THE PYTHON DUNGEON ---")
    name = input("Enter your hero's name: ")
    player = Player(name)

    enemies = [
        Enemy("Slime", 30, 5, 10),
        Enemy("Goblin", 50, 10, 25),
        Enemy("Orc", 80, 15, 50),
        Enemy("Dragon", 150, 25, 200)
    ]

    for enemy in enemies:
        if not combat(player, enemy):
            break
        
        print(f"\n--- Progress: {player.xp} XP ---")
        shop_choice = input("Visit the shop before the next floor? (y/n): ")
        if shop_choice == 'y':
            shop(player)

    if player.is_alive():
        print("\n🏆 Congratulations! You conquered the dungeon!")

if __name__ == "__main__":
    main()