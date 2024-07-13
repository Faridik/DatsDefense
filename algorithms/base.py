import json
import os

class Base:
    def __init__(self, priority_building_file='dens5_0_0.txt') -> None:
        
        # Загрузка паттерна
        with open(os.path.join("algorithms", "build_patterns", priority_building_file)) as f:
            self._priority_building = json.load(f)   
        
        self._pattern_x = 0
        self._pattern_y = 0
        # Примерная длина, до которой можем достроиться
        self._curr_len_of_priority = 3


    def update(self, units, world, head):
        return self._update_with_pattern(units, world, head)
    
    def update_pattern(self, head, move):
        self._pattern_x = (self._pattern_x + move["x"] - head["x"]) % 6
        self._pattern_y = (self._pattern_y + move["y"] - head["y"]) % 6

        filename = f"dens5_{self._pattern_x}_{self._pattern_y}.txt"
        with open(os.path.join("algorithms", "build_patterns", filename)) as f:
            self._priority_building = json.load(f)  


    def _update_with_pattern(self, units, world, head):
        """
        Строит по возможности клетки баз, проходясь по 
        списку priority_building

        head - координаты головы
        """

        # Вычисляем кол-во золота
        gold = units['player']['gold']
        if gold == 0:
            return []
        
        # Теоретический максимум: предыдущий шаг + кол-во монет
        self._curr_len_of_priority += gold

        # Что может помешать
        our_base = units.get("base", []) or []
        zombies = units.get("zombies", []) or []
        an_player_bases = units.get("enemyBlocks", []) or []
        zposts = world.get("zpots", []) or []

        # Список для постройки
        to_build = []

        for i, next_coords in enumerate(self._priority_building):

            if i > self._curr_len_of_priority:
                break

            x = head['x'] + next_coords[0]
            y = head['y'] + next_coords[0]

            # Если здесь наша база
            can_be_build = True
            for base in our_base:
                if x == base['x'] and y == base['y']:
                    can_be_build = False
                    break
            if not can_be_build:
                continue
                

            # Можно ли тут построить
            can_be_build = False
            for base in our_base:
                distance = abs(base['x'] - x) + abs(base['y'] - y)
                if distance <= 1:
                    can_be_build = True
                    break
            if not can_be_build:
                continue

            # Если зомби
            can_be_build = True
            for zombie in zombies:
                if x == zombie['x'] and y == zombie['y']:
                    can_be_build = False
                    break
            if not can_be_build:
                continue

            # Если клетка базы игрока
            can_be_build = True
            for an_player_base in an_player_bases:
                if x >= an_player_base['x'] - 1 and x <= an_player_base['x'] + 1 and \
                        y >= an_player_base['y'] - 1 and y <= an_player_base['y'] + 1:
                    can_be_build = False
                    break
            if not can_be_build:
                continue

            # Блок базы нельзя ставить вплотную к клетке спота зомби или стены
            can_be_build = True
            for zpost in zposts:
                distance = abs(zpost['x'] - x) + abs(zpost['y'] - y)
                if distance <= 1:
                    can_be_build = False
                    break
            if not can_be_build:
                continue

            # Строим здесь
            to_build.append({'x': x, 'y': y})
            gold -= 1

            # Если золота нет
            if gold == 0:
                break

        # Обновления длины
        self._curr_len_of_priority = i

        return to_build