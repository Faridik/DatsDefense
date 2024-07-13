import api
import algorithms
import time

TURN_TIME = 2

class Bot:
    def __init__(self) -> None:
        self._Base = algorithms.Base()
        self._Attack = algorithms.Attack()
        self._world = {}
        self._units = {}
        self._head = {}

    @property
    def gold(self):
        """Узнать количество голды."""
        if "player" in self._units:
            return self._units["player"]["gold"]
        return 0

    @property
    def health(self):
        """Фулл хп."""
        hp = 0
        for cell in self._units.get("base", []) or []:
            hp += cell["health"]
        return hp

    @property
    def size(self):
        """Размер базы."""
        return len(self._units.get("base", []) or [])

    @property
    def turn(self):
        """Узнать текущий ход."""
        if "turn" in self._units:
            return self._units["turn"]
        return 0
    
    @property
    def turn_ends_in_ms(self):
        """Сколько осталось до конца хода."""
        if "turn" in self._units:
            return self._units["turnEndsInMs"]
        return TURN_TIME
    
    def refresh(self):
        """Запросить данные с сервера."""
        if len(self._world.keys()) == 0 or "error" in self._world:
            self._world = api.world()
        self._units = api.units()
        # Выполняется поиск головы.
        if len(self._head.keys()) == 0:
            for cell in self._units.get("base", []) or []:
                if "isHead" in cell:
                    self._head = cell

    def base(self):
        """Возвращает команду для построения базы."""
        try:
            return self._Base.update(units=self._units, world=self._world, head=self._head)
        except:
            return None

    def attack(self):
        """Возвращает команду для атаки."""
        try:
            return self._Attack.update(units=self._units)
        except:
            return None
        
    def move(self):
        """Возвращает команду для перемещения базы."""
        try:
            return algorithms.move()
        except:
            return None

    def commit(self, *, attack=None, build=None, move_base=None):
        """Совершить действие до конца хода."""
        request_data = {}
        if attack:
            request_data["attack"] = attack
        if build:
            request_data["build"] = build
        if move_base:
            request_data["moveBase"] = move_base
        api.command(request_data)

    def print_status(self):
        print(f"[ {self.turn} ] ❤️  = {self.health}, 🪙  = {self.gold}, 🏠  = {self.size}")

    def go(self):
        while True:
            self.refresh()
            start = time.monotonic()

            build = self.base()
            attack = self.attack()
            move = self.move()
            self.commit(attack=attack, build=build, move_base=move)
            self.print_status()
            
            end = time.monotonic() - start
            sleep_time = (self.turn_ends_in_ms - end) % TURN_TIME
            print(f"∟ timing: {end:.3}s, {sleep_time=:.3}s")
            time.sleep(sleep_time)