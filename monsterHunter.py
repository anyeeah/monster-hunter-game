import random

#캐릭터 기본 설정
class Character:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name}은(는) {damage}의 피해를 입었습니다. 남은 체력: {self.health}")

    def attack_target(self, target):
        damage = random.randint(self.attack - 2, self.attack + 2)
        print(f"{self.name}이(가) {target.name}을(를) 공격하여 {damage}의 피해를 주었습니다!")
        target.take_damage(damage)
        return damage

#플레이어 설정 (기본 캐릭터 상속)
class Player(Character):
    def __init__(self, name, health, attack, inventory=None):
        super().__init__(name, health, attack)
        self.inventory = inventory if inventory is not None else set() 
        self.skills = (("강력한 공격", 15), ("방어로 전환", 5)) 

    def show_inventory(self):
        if not self.inventory:
            print("남은 아이템이 없습니다.")
        else:
            print("--- 인벤토리 ---")
            for item in self.inventory:
                print(f"- {item}")
            print("------------------")

    def use_item(self, item_name):
        if item_name in self.inventory:
            if item_name == "체력 물약⚗️": 
                self.health += 20
                print(f"체력 물약을 사용하여 체력이 20 회복되었습니다. 현재 체력: {self.health}")
                self.inventory.remove(item_name)
            else:
                print(f"{item_name}은(는 지금 사용할 수 없는 아이템입니다.")
        else:
            print(f"인벤토리에 {item_name}이(가) 없습니다.")

    def learn_skill(self, skill_name):
        print(f"{skill_name} 스킬을 사용합니다.")

# --- 3. 적 캐릭터 클래스 (Character 상속) ---
class Enemy(Character):
    def __init__(self, name, health, attack, loot_item=None):
        super().__init__(name, health, attack)
        self.loot_item = loot_item 

    def drop_item(self):
        if self.loot_item:
            print(f"{self.name}이(가) {self.loot_item}을(를) 드랍했습니다!")
            return self.loot_item
        return None

#몬스터 설정
class Goblin(Enemy):
    def __init__(self):
        super().__init__("초록 고블린", 30, 8, "낡은 동전")

class Orc(Enemy):
    def __init__(self):
        super().__init__("지하 세계 오크", 50, 12, "강철 조각")

class Dragon(Enemy):
    def __init__(self):
        super().__init__("전설의 드래곤", 100, 20, "용의 비늘")

# --- 5. 게임 로직 함수 ---
def get_player_name():
    while True:
        name = input("플레이어의 이름을 입력하세요: ").strip()
        if name:
            return name
        else:
            print("이름은 비워둘 수 없습니다. 다시 입력해주세요.")

def choose_action():
    while True:
        print("\n어떤 행동을 하시겠습니까?")
        print("1. 공격")
        print("2. 인벤토리 보기")
        print("3. 아이템 사용")
        print("4. 도망치기")
        choice = input("선택: ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        else:
            print("유효하지 않은 선택입니다. 1, 2, 3, 4 중 하나를 입력해주세요.")

def battle(player, enemy):
    print(f"\n--- {enemy.name}과의 전투 시작! ---")
    while player.is_alive() and enemy.is_alive():
        print(f"\n{player.name}의 체력: {player.health} | {enemy.name}의 체력: {enemy.health}")
        action = choose_action()

        if action == '1': # 공격
            player.attack_target(enemy)
            if not enemy.is_alive():
                print(f"{enemy.name}을(를) 물리쳤습니다!⚔️")
                dropped_item = enemy.drop_item()
                if dropped_item:
                    player.inventory.add(dropped_item) # 세트에 아이템 추가
                    print(f"{player.name}의 인벤토리에 {dropped_item}이(가) 추가되었습니다.")
                break # 전투 종료

            print(f"{enemy.name}이(가) {player.name}을(를) 공격합니다!")
            enemy.attack_target(player)
            if not player.is_alive():
                print(f"{player.name}이(가) 쓰러졌습니다⚰️ 게임 오버!")
                break # 전투 종료

        elif action == '2': # 인벤토리 보기
            player.show_inventory()

        elif action == '3': # 아이템 사용
            if not player.inventory:
                print("인벤토리가 비어있어 사용할 아이템이 없습니다.")
                continue

            print("사용할 아이템을 입력하세요 (예: 체력 물약):")
            player.show_inventory()
            item_to_use = input("아이템 이름: ").strip()
            player.use_item(item_to_use)
            # 아이템 사용 후 적 턴 진행 (밸런스를 위해)
            if enemy.is_alive():
                print(f"{enemy.name}이(가) {player.name}을(를) 공격합니다!")
                enemy.attack_target(player)
                if not player.is_alive():
                    print(f"{player.name}이(가) 쓰러졌습니다... 게임 오버!")
                    break

        elif action == '4': # 도망치기
            if random.random() < 0.5: # 50% 확률로 도망 성공
                print(f"{player.name}이(가) 성공적으로 도망쳤습니다!")
                return "escaped"
            else:
                print(f"{player.name}이(가) 도망치는데 실패했습니다!")
                # 도망 실패 시 적 턴 진행
                print(f"{enemy.name}이(가) {player.name}을(를) 공격합니다!")
                enemy.attack_target(player)
                if not player.is_alive():
                    print(f"{player.name}이(가) 쓰러졌습니다... 게임 오버!")
                    break
    return "battle_ended"

# --- 6. 메인 게임 루프 ---
def game_start():
    print("환영합니다! 몬스터 헌터에 오신 것을 환영합니다!")
    player_name = get_player_name()
    player = Player(player_name, 100, 15, {"체력 물약"}) # 시작 아이템으로 체력 물약 제공

    monsters = [Goblin(), Orc(), Dragon()]
    random.shuffle(monsters) # 몬스터 순서 무작위

    for i, monster in enumerate(monsters):
        print(f"\n--- 제 {i+1} 라운드 ---")
        print(f"앗! {monster.name}이(가) 나타났습니다!")
        result = battle(player, monster)

        if not player.is_alive():
            print("게임을 다시 시작하시겠습니까? (예/아니오)")
            restart_choice = input().strip().lower()
            if restart_choice == '예':
                game_start() # 게임 재시작
            else:
                print("게임을 종료합니다.")
            return # 게임 종료

        if result == "escaped":
            print("다음 모험을 위해 잠시 숨을 고릅니다...")
            continue # 다음 몬스터로 넘어감

    print("\n------------------------------------")
    print("모든 몬스터를 물리쳤습니다! 당신은 진정한 몬스터 헌터입니다!")
    print("------------------------------------")
    player.show_inventory()
    print("게임을 종료합니다.")

# 게임 시작 함수를 직접 호출
game_start()