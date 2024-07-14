import api
import algorithms
import time
import traceback
from functools import wraps


TURN_TIME = 2

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper

class Bot:
    def __init__(self) -> None:
        self._Base = algorithms.Base()
        self._Attack = algorithms.Attack()
        self._world = {}
        self._units = {}
        self._head = {}
        self._stop_move = 9999
        self._to_cirl = 9999

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
    
    @timeit
    def refresh(self):
        """Запросить данные с сервера."""
        self._world = api.world()
        self._units = api.units()
        with open('props.txt') as f:
            self._stop_move, self._to_cirl = map(int,f.read().split())
        # Выполняется поиск головы.
        if self.turn > self._to_cirl:
            self._Base.update_pattern_to_circle()

        for cell in self._units.get("base", []) or []:
            if "isHead" in cell:
                self._head = cell

    @timeit
    def base(self):
        """Возвращает команду для построения базы."""
        try:
            return self._Base.update(units=self._units, world=self._world, head=self._head)
        except Exception as e:
            print("FAILED TO BUILD:", e)
            traceback.print_exception(e)
            return None

    @timeit
    def attack(self):
        """Возвращает команду для атаки."""
        try:
            return self._Attack.update(units=self._units, head=self._head)
        except Exception as e:
            print("FAILED TO ATTACK:", e)
            traceback.print_exception(e)
            return None
    @timeit
    def move(self):
        """Возвращает команду для перемещения базы."""
        if (self.turn > self._stop_move):
            # Явно запретим, чтобы не ломать сетку.
            return None

        try:
            return algorithms.move(self._units, self._world, self._head)
        except Exception as e:
            print("FAILED TO MOVE:", e)
            traceback.print_exception(e)
            return None

    def calibrate(self, move_base=None):
        """Откалибровать базу, если вдруг поменялся центр."""
        if move_base is None:
            return
        try:
            self._Base.update_pattern(head=self._head, move=move_base)
        except Exception as e:
            traceback.print_exception(e)
            print("FAILED TO CALIBRATE:", e)
        # self._head["x"] = move_base["x"]
        # self._head["y"] = move_base["y"]

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


    def print_status(self, attack, build):
        head_coords = f"({self._head.get('x')}, {self._head.get('y')})"
        attack_log = ""
        build_log = ""
        if attack:
            attack_log = f"⚔️  = {len(attack)}, "
        if build:
            build_log = f"🛠️  = {len(build)}"
        print(f"[ {self.turn} ] ❤️  = {self.health}, 🪙  = {self.gold}, 🏠  = {self.size}, {attack_log}{build_log} | {head_coords}")

    def go(self):
        while True:
            self.refresh()
            start = time.perf_counter()

            build = self.base()
            attack = self.attack()
            move = self.move()
            self.commit(attack=attack, build=build, move_base=move)
            self.calibrate(move_base=move)
            self.print_status(attack=attack, build=build)

            end = time.perf_counter() - start
            sleep_time = (self.turn_ends_in_ms - end) % TURN_TIME
            print(f"---> timing: {end:.3}s, {sleep_time=:.3}s")
            time.sleep(sleep_time)