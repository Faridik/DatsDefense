import json
import os

class Base:
    def __init__(self, priority_building_file='dens5.txt') -> None:
        
        # Загрузка паттерна
        with open(os.path.join("algorithms", "build_patterns", priority_building_file)) as f:
            self._priority_building = json.load(f)   
        
        # Примерная длина, до которой можем достроиться
        self._curr_len_of_priority = 3


    def update(self, units, world, head):
        return self._update_with_pattern(units, world, head)

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
            for base in our_base:
                if x == base['x'] and y == base['y']:
                    continue

            # Можно ли тут построить
            can_be_build = False
            for base in our_base:
                if x >= base['x'] - 1 and x <= base['x'] + 1 and \
                    y >= base['y'] - 1 and y <= base['y'] + 1:
                    can_be_build = True
                    continue
            if not can_be_build:
                continue

            # Если зомби
            for zombie in zombies:
                if x == zombie['x'] and y == zombie['y']:
                    continue

            # Если клетка базы игрока
            for an_player_base in an_player_bases:
                if x >= an_player_base['x'] - 1 and x <= an_player_base['x'] + 1 and \
                        y >= an_player_base['y'] - 1 and y <= an_player_base['y'] + 1:
                    continue

            # Блок базы нельзя ставить вплотную к клетке спота зомби или стены
            for zpost in zposts:
                distance = abs(zpost['x'] - x) + abs(zpost['y'] - y)
                if distance <= 1:
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