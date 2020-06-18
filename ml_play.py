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
                    if x <= 40 and x >= -40 :      
                        if y > 140 and y < 380:
                            grid.add(3)
                        if y > 0 and y < 190:
                            speed_ahead = car["velocity"]
                            grid.add(8) 
                        if y < 0 and y > -200:
                            grid.add(13)
                    if x > -80 and x < -30:
                        if y > 60 and y < 250:
                            grid.add(4)
                        if y <= -70 and y >= -200:
                            grid.add(14)
                        if y < 70 and y > -60:
                            grid.add(9)
                    if x > -155 and x <= -80 :
                        if y > 60 and y < 250:
                            grid.add(5)
                        if y <= -50 and y >= -200:
                            grid.add(15)
                        if y < 60 and y > -50:
                            grid.add(10)
                    if x < 80 and x > 30:
                        if y > 60 and y < 250:
                            grid.add(2)
                        if y <= -70 and y >= -200:
                            grid.add(12)
                        if y < 70 and y > -60:
                            grid.add(7)
                    if x < 155 and x >= 80 :
                        if y > 60 and y < 250:
                            grid.add(1)
                        if y <= -50 and y >= -200:
                            grid.add(11)
                        if y < 60 and y > -50:
                            grid.add(6)

            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead):
            if self.player_no == 0:
                print(grid, end = "(r)")
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
                    if (4 not in grid) and (5 not in grid) and (9 not in grid) and (10 not in grid) and ((7 in grid) or (2 in grid) or (6 in grid) or (1 in grid)): # turn right
                        if self.car_vel < speed_ahead:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print('br')
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif (1 not in grid) and (2 not in grid) and (7 not in grid) and (6 not in grid) and ((9 in grid) or (4 in grid) or (10 in grid) or (5 in grid)): # turn left
                        if self.car_vel < speed_ahead:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print('bl')
                            return ["BRAKE", "MOVE_LEFT"]
                    elif (2 in grid) and (7 in grid) and (9 not in grid) and (4 not in grid): # turn right
                        if self.car_vel < speed_ahead:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print('br')
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif (4 in grid) and (9 in grid) and (7 not in grid) and (2 not in grid): # turn left
                        if self.car_vel < speed_ahead:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print('bl')
                            return ["BRAKE", "MOVE_LEFT"]
                    elif (2 in grid) and (7 in grid) and (9 not in grid): # turn right
                        if self.car_vel < speed_ahead:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print('br')
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif (4 in grid) and (9 in grid) and (7 not in grid): # turn left
                        if self.car_vel < speed_ahead:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print('bl')
                            return ["BRAKE", "MOVE_LEFT"]
                    elif (7 in grid) and (9 not in grid) and (4 not in grid): # turn right
                        if self.car_vel < speed_ahead:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print('br')
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif (9 in grid) and (7 not in grid) and (2 not in grid): # turn left
                        if self.car_vel < speed_ahead:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print('bl')
                            return ["BRAKE", "MOVE_LEFT"]
                    elif (2 in grid) and (7 in grid) and (4 in grid) and (5 not in grid): # turn right
                        if self.car_vel < speed_ahead:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print('br')
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif (4 in grid) and (9 in grid) and (2 in grid) and (1 not in grid): # turn left
                        if self.car_vel < speed_ahead:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print('bl')
                            return ["BRAKE", "MOVE_LEFT"]
                    elif (7 in grid) and (4 in grid) and (5 not in grid): # turn right
                        if self.car_vel < speed_ahead:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print('br')
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif (9 in grid) and (2 in grid) and (1 not in grid): # turn left
                        if self.car_vel < speed_ahead:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print('bl')
                            return ["BRAKE", "MOVE_LEFT"]
                    elif (9 not in grid) and (10 not in grid) and (14 not in grid): # turn right
                        if self.car_vel < speed_ahead:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print('br')
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif (7 not in grid) and (6 not in grid)and (12 not in grid): # turn left 
                        if self.car_vel < speed_ahead:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print('bl')
                            return ["BRAKE", "MOVE_LEFT"]
                    elif (9 not in grid) and (4 not in grid): # turn right
                        if self.car_vel < speed_ahead:
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        else:
                            print('br')
                            return ["BRAKE", "MOVE_RIGHT"]
                    elif (7 not in grid) and (2 not in grid): # turn left
                        if self.car_vel < speed_ahead:
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        else:
                            print('bl')
                            return ["BRAKE", "MOVE_LEFT"]
                    else:
                        if self.car_vel < speed_ahead:  # BRAKE
                            print('s')
                            return ["SPEED"]                            
                        else:
                            print('b')
                            return ["BRAKE"]
                else:
                    if (3 in grid): # Check forward
                        if (self.car_pos[0] < 35 ):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (5 in grid) and (10 in grid) and (15 in grid) and (4 not in grid) and (9 not in grid) and (14 not in grid) and (2 in grid) and (7 in grid) and (12 in grid) and (1 in grid) and (6 in grid) and (11 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 in grid) and (6 in grid) and (11 in grid) and (2 not in grid) and (7 not in grid) and (12 not in grid) and (4 in grid) and (9 in grid) and (14 in grid) and (5 in grid) and (10 in grid) and (15 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (5 in grid) and (10 in grid) and (15 in grid) and (4 not in grid) and (9 not in grid) and (14 not in grid) and (2 in grid) and (7 in grid) and (12 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 in grid) and (6 in grid) and (11 in grid) and (2 not in grid) and (7 not in grid) and (12 not in grid) and (4 in grid) and (9 in grid) and (14 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (4 not in grid) and (9 not in grid) and (14 not in grid) and (2 in grid) and (7 in grid) and (12 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (2 not in grid) and (7 not in grid) and (12 not in grid) and (4 in grid) and (9 in grid) and (14 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (4 not in grid) and (9 not in grid) and (14 not in grid) and (2 in grid) and (7 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (2 not in grid) and (7 not in grid) and (12 not in grid) and (4 in grid) and (9 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]

                        if (2 in grid) and (7 in grid) and (12 in grid) and (4 in grid) and (5 not in grid) and (9 not in grid) and (10 not in grid): # turn right
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 in grid) and (9 in grid) and (14 in grid) and (2 in grid) and (1 not in grid) and (6 not in grid) and (7 not in grid): # turn left
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (2 in grid) and (7 in grid) and (4 in grid) and (5 not in grid) and (9 not in grid) and (10 not in grid): # turn right
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 in grid) and (9 in grid) and (2 in grid) and (1 not in grid) and (6 not in grid) and (7 not in grid): # turn left
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (2 in grid) and (7 in grid) and (4 in grid) and (5 not in grid) and (9 not in grid): # turn right
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 in grid) and (9 in grid) and (2 in grid) and (1 not in grid) and(7 not in grid): # turn left
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]

                        if (5 not in grid) and (10 not in grid) and (15 not in grid) and (4 not in grid) and (9 not in grid) and (14 not in grid) and (2 in grid) and (7 in grid) and (12 in grid) and (1 in grid) and (6 in grid) and (11 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (6 not in grid) and (11 not in grid) and (2 not in grid) and (7 not in grid) and (12 not in grid) and (4 in grid) and (9 in grid) and (14 in grid) and (5 in grid) and (10 in grid) and (15 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (5 not in grid) and (10 not in grid) and (4 not in grid) and (9 not in grid) and (2 in grid) and (7 in grid) and (12 in grid) and (1 in grid) and (6 in grid) and (11 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (6 not in grid) and (2 not in grid) and (7 not in grid) and (4 in grid) and (9 in grid) and (14 in grid) and (5 in grid) and (10 in grid) and (15 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (5 not in grid) and (10 not in grid) and (4 not in grid) and (9 not in grid) and (2 in grid) and (7 in grid) and (1 in grid) and (6 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (6 not in grid) and (2 not in grid) and (7 not in grid) and (4 in grid) and (9 in grid) and (5 in grid) and (10 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (5 not in grid) and (4 not in grid) and (9 not in grid) and (2 in grid) and (7 in grid) and (1 in grid) and (6 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (1 not in grid) and (2 not in grid) and (7 not in grid) and (4 in grid) and (9 in grid) and (5 in grid) and (10 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (4 not in grid) and (9 not in grid) and (2 in grid) and (7 in grid) and (1 in grid) and (6 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (2 not in grid) and (7 not in grid) and (4 in grid) and (9 in grid) and (5 in grid) and (10 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (4 not in grid) and (9 not in grid) and ((2 in grid) or (1 in grid)) and ((7 in grid) or (6 in grid)):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (2 not in grid) and (7 not in grid) and ((4 in grid) or (5 in grid)) and ((9 in grid) or (10 in grid)):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (4 not in grid) and (9 not in grid) and ((2 in grid) or (1 in grid)):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (2 not in grid) and (7 not in grid) and ((4 in grid) or (5 in grid)):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (4 not in grid) and (9 not in grid) and ((7 in grid) or (6 in grid)):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (2 not in grid) and (7 not in grid) and ((9 in grid) or (10 in grid)):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]

                        if (2 in grid) and (7 in grid) and (12 in grid) and (4 in grid) and (5 not in grid) and (9 not in grid) and (10 not in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 in grid) and (9 in grid) and (14 in grid) and (2 in grid) and (1 not in grid) and (6 not in grid) and (7 not in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (4 in grid) and (5 not in grid) and (9 not in grid) and (10 not in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (2 in grid) and (1 not in grid) and (6 not in grid) and (7 not in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]

                        if (1 in grid) and (4 in grid) and (9 in grid) and (2 not in grid) and (7 not in grid): # turn left
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (2 in grid) and (5 in grid) and (7 in grid) and (4 not in grid) and (9 not in grid): # turn right
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 in grid) and (9 in grid) and (7 not in grid) and (12 not in grid): # turn left 
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (2 in grid) and (7 in grid) and (9 not in grid) and (14 not in grid): # turn right
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (4 in grid) and (7 not in grid) and (12 not in grid): # turn left 
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (2 in grid) and (9 not in grid) and (14 not in grid): # turn right
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (2 not in grid) and (7 not in grid): # turn left 
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
                        if (4 not in grid) and (9 not in grid): # turn right
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (7 not in grid) and (12 not in grid): # turn left 
                            print('l')
                            return ["MOVE_LEFT"]
                        if (9 not in grid) and (14 not in grid): # turn right
                            print('r')
                            return ["MOVE_RIGHT"]
                        else :
                            print('s')
                            return ["SPEED"]
                    else:
                        if (4 not in grid) and (9 not in grid) and (14 in grid):
                            print('sr')
                            return ["SPEED", "MOVE_RIGHT"]
                        if (2 not in grid) and (7 not in grid) and (12 in grid):
                            print('sl')
                            return ["SPEED", "MOVE_LEFT"]
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
