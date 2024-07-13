class Attack:
    def __init__(self) -> None:
        self._zombies = []
        self._players = []
        self._our_cells = []

        self._zombie_coeff = {
            "normal": 1,
            "fast": 1,
            "bomber": 5,
            "liner": 4,
            "juggernaut": 1,
            "chaos_knights": 0.5
        }

        self._response = []

    def update(self, units, head):
        return self._attack(units, head)
    
    def _attack(self, units, head):
        # Новый запрос
        self._response.clear()

        # Достать базу, игроков и зомби
        self._bfs(units, head)
        self._zombies = (units.get("zombies", []) or []).copy()
        for zombie in self._zombies:
            zombie['our_cells'] = []
        self._players = (units.get("enemyBlocks", []) or []).copy()
        for player in self._players:
            player['our_cells'] = []

        # Найти достижимых противников и создать связи
        # между ними и клетакми базы
        self._check_enemies()

        # Задание приоритетов по уничтожению для зомби
        self._set_priority()

        # Нападение на зомби с приоритетом 2
        self._attack_zombie_priority_2()

        # Нападение остальными ячейками базы
        self._attack_other()

        # Очистка данных
        self._zombies.clear()
        self._players.clear()
        self._our_cells.clear()

        # Возвращаем запрос
        return self._response

    def _bfs(self, units, head):
        cells = units.get("base", []).copy() or []

        for cell in cells:
            cell['visited'] = False

        queue = [head]
        head['visited'] = True

        while queue:

            s = queue.pop(0)
            self._our_cells.append(s)

            for cell in cells:
                distance = abs(cell['x']  - s['x']) + abs(cell['y'] - s['y'])
                if distance <= 1 and not cell['visited']:
                    queue.append(cell)
                    cell['visited'] = True
            


    def _check_enemies(self):
        """
        Находит всех зомби и игроков в зоне видимости.
        Создаёт привязку к ячейке базы - противников
        и наоборот.
        """

        # Смотрим для каждой ячейки зомби и игроков в её области видимости 
        # Срез нужен, чтобы работало удаление (это python magic)
        for cell in self._our_cells[:]:   

            # Привязка клетки к зомби и игрокам
            cell["zombies"] = []
            cell["players"] = []

            # Ищем зомби и добавляем ссылки друг на друга
            for zombie in self._zombies:

                x_len = zombie["x"] - cell["x"]
                y_len = zombie["y"] - cell["y"]
                dist = (x_len ** 2 + y_len ** 2) ** (1/2)

                if dist <= cell["range"]:
                    cell["zombies"].append(zombie)
                    zombie["our_cells"].append(cell)

            for player in self._players:

                x_len = player["x"] - cell["x"]
                y_len = player["y"] - cell["y"]
                dist = (x_len ** 2 + y_len ** 2) ** (1/2)

                if dist <= cell["range"]:
                    cell["players"].append(player)
                    player["our_cells"].append(cell)

            # Если зомби рядом нет, то удаляем ячейку        
            if cell["zombies"] == [] and cell["players"] == []:
                self._our_cells.remove(cell)
    


    def _set_priority(self):
        """
        Задаёт приоритет зомби
        2 - зомби, которые нас атакуют в этом ходу
        1 - зомби, которые нас будут атаковать через ход
        0 - зомби нас не задевает
        """

        for zombie in self._zombies[:]:

            # Если не можем атаковать, то что ж...
            if zombie["our_cells"] == []:
                self._zombies.remove(zombie)
                continue
            
            self._set_priority_for_zombie(zombie)


    def _set_priority_for_zombie(self, zombie):
        # Разбираемся с хаосом
        # Без картинки не понять, что тут происходит
        # Да и с картинкой.. простой я сошёл с ума
        # даа... даа... тут хорошо...
        if zombie["type"] == "chaos_knight":
            for cell in zombie["our_cells"]:
                x_len = abs(zombie["x"] - cell["x"])
                y_len = abs(zombie["y"] - cell["y"])

                dist = x_len + y_len

                if x_len != 0 or y_len != 0:
                    if dist == 3:
                        zombie["priority"] = 2
                        return

                if dist == 6:
                    zombie["priority"] = 1
                    return

                if dist == 2:
                    zombie["priority"] = 1
                    return

                if dist == 4 and x_len != 2:
                    zombie["priority"] = 1
                    return
                    
                zombie["priority"] = 0
                return

        # Остальные зомби
        if zombie["direction"] == "right":
            for cell in zombie["our_cells"]:
                if zombie["y"] == cell["y"]:
                    if zombie["x"] <= cell["x"] <= zombie["x"] + zombie["speed"]:
                        if zombie["waitTurns"] == 1:
                            zombie["priority"] = 2 
                            return
            for cell in zombie["our_cells"]:
                if zombie["y"] == cell["y"]:
                    if zombie["x"] <= cell["x"] <= zombie["x"] + zombie["speed"]:
                        zombie["priority"] = 1 
                        return
                    if zombie["x"] <= cell["x"] <= zombie["x"] + 2 * zombie["speed"]:
                        zombie["priority"] = 1
                        return

        if zombie["direction"] == "left":
            for cell in zombie["our_cells"]:
                if zombie["y"] == cell["y"]:
                    if zombie["x"] - zombie["speed"] <= cell["x"] <= zombie["x"]:
                        if zombie["waitTurns"] == 1:
                            zombie["priority"] = 2 
                            return
            for cell in zombie["our_cells"]:
                if zombie["y"] == cell["y"]:
                    if zombie["x"] - zombie["speed"] <= cell["x"] <= zombie["x"]:
                        zombie["priority"] = 1 
                        return
                    if zombie["x"] - 2 * zombie["speed"] <= cell["x"] <= zombie["x"]:
                        zombie["priority"] = 1
                        return

        if zombie["direction"] == "up":
            for cell in zombie["our_cells"]:
                if zombie["x"] == cell["x"]:
                    if zombie["y"] <= cell["y"] <= zombie["y"] + zombie["speed"]:
                        if zombie["waitTurns"] == 1:
                            zombie["priority"] = 2 
                            return
            for cell in zombie["our_cells"]:
                if zombie["x"] == cell["x"]:
                    if zombie["y"] <= cell["y"] <= zombie["y"] + zombie["speed"]:
                        zombie["priority"] = 1 
                        return
                    if zombie["y"] <= cell["y"] <= zombie["y"] + 2 * zombie["speed"]:
                        zombie["priority"] = 1
                        return


        if zombie["direction"] == "down":
            for cell in zombie["our_cells"]:
                if zombie["x"] == cell["x"]:
                    if zombie["y"] - zombie["speed"] <= cell["y"] <= zombie["y"]:
                        if zombie["waitTurns"] == 1:
                            zombie["priority"] = 2 
                            return
            for cell in zombie["our_cells"]:
                if zombie["x"] == cell["x"]:
                    if zombie["y"] - zombie["speed"] <= cell["y"] <= zombie["y"]:
                        zombie["priority"] = 1 
                        return
                    if zombie["y"] - 2 * zombie["speed"] <= cell["y"] <= zombie["y"]:
                        zombie["priority"] = 1
                        return

        zombie["priority"] = 0


    def _attack_zombie_priority_2(self):
        zombies_prior_2 = list(filter(lambda z: z["priority"] == 2, self._zombies))

        for zombie in sorted(zombies_prior_2, 
                             key=lambda z: -self._zombie_coeff[z["type"]] * z["attack"]):

            self._attack_one_zombie_prior_2(zombie)
            self._zombies.remove(zombie)


    def _attack_one_zombie_prior_2(self, zombie):
        for cell in sorted(zombie["our_cells"], 
                           key=lambda cell: len(cell["zombies"]) + len(cell["players"])):

            # Создаём запрос 
            self._response.append({
                "blockId": cell["id"],
                "target": {
                    "x": zombie["x"],
                    "y": zombie["y"]
                    }
            })
            
            # Удаляем эту ячейку из других зомби
            for an_zombie in cell["zombies"]:
                an_zombie["our_cells"].remove(cell)

                # Если в зомби никто не целится, то удаляем его
                # как будто это не нужно, так как мы больше не итерируем по зомби
                # if len(an_zombie["our_cells"]) == 0:
                #     self._zombies.remove(an_zombie)
            # Можно ещё удалить ссылку на ячейку у игроков

            # Удаляем саму ячейку, больше ей стрелять не сможем
            self._our_cells.remove(cell)

            # Уменьшаем кол-во жизней
            zombie["health"] -= cell["attack"]

            if zombie["health"] <= 0:
                for cell in zombie["our_cells"]:
                    cell["zombies"].remove(zombie)
                return

    def _attack_other(self):
        for cell in sorted(self._our_cells, 
                           key=lambda cell: len(cell["zombies"]) + len(cell["players"])):
            
            # Сначала бьём зомби с приоритетом 1
            is_attacked = False
            if cell["zombies"] != []:
                for zombie in cell["zombies"]:
                    if zombie["priority"] == 1:
                        self._attack_one_enemy(cell, zombie, "zombies")
                        is_attacked = True
                        break
            if is_attacked:
                continue

            # Затем зомби с приоритетом 0
            is_attacked = False
            if cell["zombies"] != []:
                for zombie in cell["zombies"]:
                    if zombie["priority"] == 0:
                        self._attack_one_enemy(cell, zombie, "zombies")
                        is_attacked = True
                        break
            if is_attacked:
                continue
            # Потом бьём игроков
            if cell["players"] != []:
                self._attack_one_enemy(cell, cell["players"][0], "players")
                continue
            

            


                            
            
    def _attack_one_enemy(self, cell, enemy, type):
        # Создаём запрос 
        self._response.append({
            "blockId": cell["id"],
            "target": {
                "x": enemy["x"],
                "y": enemy["y"]
                }
        })

        # Отнимаем хп
        enemy["health"] -= cell["attack"]

        # Если враг умер, то очищаешь ячейки, которые могут по нему стрелять
        if enemy["health"] <= 0:
            for an_cells in enemy["our_cells"]:
                 an_cells[type].remove(enemy)

        else:   # Если нет, то очищаем только текущю ячейку
            cell[type].remove(enemy)
            enemy["our_cells"].remove(cell)

        





        

