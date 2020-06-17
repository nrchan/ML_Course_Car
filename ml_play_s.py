class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass

    def update(self, scene_info):
        """
        15 grid relative position
        |    |    |    |    |    |
        |  1 |  2 |  3 |  4 |  5 |
        |    |    |  8 |    |    |
        |  6 |  7 |  c |  9 | 10 |
        |    |    |    |    |    |
        | 11 | 12 | 13 | 14 | 15 |
        |    |    |    |    |    |
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            if(self.car_lane < 5): score = 1
            else: score = -1
            
            if self.car_pos[0] < 36: # left bound
                grid.add(2)
                grid.add(7)
                grid.add(12)
            if self.car_pos[0] < 106: # left bound
                grid.add(1)
                grid.add(6)
                grid.add(11)
            if self.car_pos[0] > 594: # right bound
                grid.add(4)
                grid.add(9)
                grid.add(14)
            if self.car_pos[0] > 524: # right bound
                grid.add(5)
                grid.add(10)
                grid.add(15)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 35 and x >= -35 :      
                        if y > 140 and y < 380:
                            grid.add(3)
                        if y > 0 and y < 190:
                            speed_ahead = car["velocity"]
                            grid.add(8) 
                        if y < 0 and y > -200:
                            grid.add(13)
                    if x > -80 and x < -20:
                        if y > 60 and y < 320:
                            grid.add(4)
                        if y <= -70 and y >= -200:
                            grid.add(14)
                        if y < 70 and y > -60:
                            grid.add(9)
                    if x > -155 and x <= -80 :
                        if y > 60 and y < 300:
                            grid.add(5)
                        if y <= -50 and y >= -200:
                            grid.add(15)
                        if y < 60 and y > -50:
                            grid.add(10)
                    if x < 80 and x > 20:
                        if y > 60 and y < 320:
                            grid.add(2)
                        if y <= -70 and y >= -200:
                            grid.add(12)
                        if y < 70 and y > -60:
                            grid.add(7)
                    if x < 155 and x >= 80 :
                        if y > 60 and y < 300:
                            grid.add(1)
                        if y <= -50 and y >= -200:
                            grid.add(11)
                        if y < 60 and y > -50:
                            grid.add(6)

            if (self.car_lane is 0): score += -10000
            if (self.car_lane is 8): score += 10000
            if(1 in grid) and (self.car_lane > 1): score += -10
            if(2 in grid) and (self.car_lane > 0): score += -1000
            if(6 in grid) and (self.car_lane > 1): score += -5000
            if(7 in grid) and (self.car_lane > 0): score += -10000
            if(11 in grid) and (self.car_lane > 1): score += -5
            if(12 in grid) and (self.car_lane > 0): score += -150
            if(4 in grid) and (self.car_lane < 8): score += 1000
            if(5 in grid) and (self.car_lane < 7): score += 10
            if(9 in grid) and (self.car_lane < 8): score += 10000
            if(10 in grid) and (self.car_lane < 7): score += 5000
            if(14 in grid) and (self.car_lane < 8): score += 150
            if(15 in grid) and (self.car_lane < 7): score += 5
            if(1 not in grid) and (self.car_lane > 1): score += 10
            if(2 not in grid) and (self.car_lane > 0): score += 1000
            if(6 not in grid) and (self.car_lane > 1): score += 5000
            if(7 not in grid) and (self.car_lane > 0): score += 10000
            if(11 not in grid) and (self.car_lane > 1): score += 5
            if(12 not in grid) and (self.car_lane > 0): score += 150
            if(4 not in grid) and (self.car_lane < 8): score += -1000
            if(5 not in grid) and (self.car_lane < 7): score += -10
            if(9 not in grid) and (self.car_lane < 8): score += -10000
            if(10 not in grid) and (self.car_lane < 7): score += -5000
            if(14 not in grid) and (self.car_lane < 8): score += -150
            if(15 not in grid) and (self.car_lane < 7): score += -5
            if(2 not in grid) and (7 not in grid) and (self.car_lane > 0): score += 10000
            if(1 not in grid) and (6 not in grid) and (7 not in grid) and (self.car_lane > 1): score += 5000
            if(4 not in grid) and (9 not in grid) and (self.car_lane < 8): score += -10000
            if(5 not in grid) and (10 not in grid) and (9 not in grid) and (self.car_lane < 7): score += -5000
            if(2 not in grid) and (7 not in grid) and (12 not in grid) and (self.car_lane > 0): score += 100000
            if(4 not in grid) and (9 not in grid) and (14 not in grid) and (self.car_lane > 1): score += 100000
            if(9 in grid) and score < 0: score = 0
            if(7 in grid) and score > 0: score = 0
            return move(grid= grid, speed_ahead = speed_ahead, score = score)
            
        def move(grid, speed_ahead, score):
            if self.player_no == 0:
                print(grid, score, end = "(s)")
            if len(grid) == 0:
                # Back to lane center
                if self.car_pos[0] > self.lanes[self.car_lane]:
                    print('sl')
                    return ["SPEED", "MOVE_LEFT"]
                elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                    print('sr')
                    return ["SPEED", "MOVE_RIGHT"]
                else :
                    print('s')
                    return ["SPEED"]
            else:
                if (8 in grid): # NEED to BRAKE
                    if(score < 0):
                        if self.car_vel < speed_ahead:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print('br')
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif(score > 0):
                        if self.car_vel < speed_ahead:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print('bl')
                            return ["BRAKE", "MOVE_LEFT"]
                    else:
                        if self.car_vel < speed_ahead:  # BRAKE
                            if self.car_pos[0] > self.lanes[self.car_lane]:
                                print('sl')
                                return ["SPEED", "MOVE_LEFT"]
                            elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                                print('sr')
                                return ["SPEED", "MOVE_RIGHT"]
                            else :
                                print('s')
                                return ["SPEED"]                            
                        else:
                            if self.car_pos[0] > self.lanes[self.car_lane]:
                                print('sl')
                                return ["BRAKE", "MOVE_LEFT"]
                            elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                                print('sr')
                                return ["BRAKE", "MOVE_RIGHT"]
                            else :
                                print('s')
                                return ["BRAKE"]
                else:
                    if (3 in grid): # Check forward
                        if(score < 0):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        elif(score > 0):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            if self.car_pos[0] > self.lanes[self.car_lane]:
                                print('sl')
                                return ["SPEED", "MOVE_LEFT"]
                            elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                                print('sr')
                                return ["SPEED", "MOVE_RIGHT"]
                            else :
                                print('s')
                                return ["SPEED"]
                    else:
                        # Back to lane center
                        if self.car_pos[0] > self.lanes[self.car_lane]:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else :
                            print('s')
                            return ["SPEED"]                
                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
