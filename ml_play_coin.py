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
        self.car_vel = 0
        self.car_pos = ()
        pass

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"]  != "ALIVE":
            return "RESET"

        self.car_pos = scene_info[self.player]
        Bcar = []
        Pcar =[]
        Coin = []
        near_coin_x = 0
        near_coin_y = 0
        for car in scene_info["cars_info"]:
            if car["id"] == self.player_no:
                self.car_vel = car["velocity"]
                self.car_pos=car["pos"]
                f1 = self.car_pos[1]-40
                f2 = self.car_pos[1]+40
                s1 = self.car_pos[0]-20
                s2 = self.car_pos[0]+20
            else:
                if car["id"] >= 100: Bcar.append(car["id"])
                if car["id"] < 100: Pcar.append(car["id"])
        print("my car position = ",self.car_pos,"my velocity = ",self.car_vel)
        if scene_info.__contains__("coins"):
            Coin.append(scene_info["coins"])
        if self.car_pos == () :
            print("SPEED")
            return ["SPEED"]
        print("Bcars = ", Bcar)
        print("Pcars = ", Pcar)
        print("Coin = ", Coin)
        near_coin = 1000000       
        if len(Coin[0]) != 0:
            for i in range(len(Coin[0])):
                coin_dis = (self.car_pos[0]-Coin[0][i][0]-10)**2+(self.car_pos[1]-Coin[0][i][1]-10)**2
                if coin_dis < near_coin:
                    near_coin = coin_dis
                    near_coin_x = Coin[0][i][0]+10
                    near_coin_y = Coin[0][i][1]+10
            print("near coin x and y =", near_coin_x,near_coin_y)

        m = 9
        max_dis = 1000
        left_banner = 0
        right_banner = 0
        front_banner = 0
        vel_diff_mid = 0
        vel_diff_left = 0
        vel_diff_right = 0
        lane_pos = []
        lane_dis = []
        lane_ctr =[]
        buffer = 25
        banner_buffer = 80
        for i in range(m):
            lane_pos.append(i*70+35)
            lane_dis.append(max_dis)
            lane_ctr.append(lane_pos[i]-self.car_pos[0])
        left_lane = 0
        right_lane = 0
        mid_lane = 0
        for i in range(m):
            if abs(lane_ctr[i]) <= 2:
                left_lane = i
                mid_lane = i+1
                right_lane = i+2

        n = len(Pcar)
        k = 0
        too_fast = 0
        too_close_f = 0
        too_close_s = 0
        too_close_r = 0
        if n != 0:
            for i in range(n):
                for car in scene_info["cars_info"]:
                    if car["id"] == Pcar[i]:
                        Pcar_pos = car["pos"]
                        Pcar_vel = car["velocity"]
                        if Pcar_pos[1] > self.car_pos[1]: k=k+1
                        if abs(self.car_pos[0]-Pcar_pos[0]) < 70 and self.car_pos[1]-Pcar_pos[1] < 120 and self.car_pos[1]-Pcar_pos[1] > 0 and self.car_vel-Pcar_vel >= 3:
                            too_close_f = 1
                        if abs(self.car_pos[1]-Pcar_pos[1]) < 80 and self.car_pos[0]-Pcar_pos[0] < 70 and self.car_pos[0]-Pcar_pos[0] > 0 : too_close_s = 1
                        if abs(self.car_pos[1]-Pcar_pos[1]) < 80 and Pcar_pos[0]-self.car_pos[0] < 70 and Pcar_pos[0]-self.car_pos[0] > 0 : too_close_r = 1
                    if k == n and self.car_vel > 13: too_fast = 1
        
        if mid_lane != 0:
            n=len(Bcar)
            if n != 0:
                for i in range(n):
                    for car in scene_info["cars_info"]:
                        if car["id"] == Bcar[i]:
                            Bcar_vel = car["velocity"]
                            Bcar_pos = car["pos"]
                            trans_pos = Bcar_pos[0]
                            if abs(self.car_pos[0]-Bcar_pos[0]) < 70 and self.car_pos[1]-Bcar_pos[1] < 140 and self.car_pos[1]-Bcar_pos[1] > 0 and self.car_vel-Bcar_vel >= 3 :
                                front_banner = 1
                            for j in range(m):
                                if Bcar_pos[0] >= j*70+20 and  Bcar_pos[0] <= (j+1)*70-20: trans_pos = j*70+35
                            print(car["id"], trans_pos, Bcar_pos, Bcar_vel, f1)
                            # Find the minimun distance in front of my car
                            if trans_pos == self.car_pos[0] and self.car_pos[1]-Bcar_pos[1] > 0:
                                print("the car ", car["id"], "is the same lane and front of my car ",self.player_no)
                                if self.car_pos[1]-Bcar_pos[1] < lane_dis[mid_lane-1]:
                                    lane_dis[mid_lane-1] = f1-Bcar_pos[1]-40
                                    vel_diff_mid = self.car_vel-Bcar_vel
                            # Find the minimun distance in left-lane and right-lane front of my car and banner conditions
                            if left_lane < m and left_lane > 0:
                                left_car_pos = left_lane*70-35
                                if trans_pos == left_car_pos and self.car_pos[1]-Bcar_pos[1] > 0:
                                    print("the car ", car["id"], "is the left lane and front of my car",self.player_no)
                                    if self.car_pos[1]-Bcar_pos[1] < lane_dis[left_lane-1]:
                                        lane_dis[left_lane-1] = f1-Bcar_pos[1]-40
                                elif trans_pos == left_car_pos and abs(self.car_pos[1]-Bcar_pos[1]) <  banner_buffer:
                                    left_banner = 1
                            if right_lane < m+1 and right_lane > 1:
                                right_car_pos = right_lane*70-35
                                if trans_pos == right_car_pos and self.car_pos[1]-Bcar_pos[1] > 0:
                                    print("the car ", car["id"], "is the right lane and front of my car",self.player_no)
                                    if self.car_pos[1]-Bcar_pos[1] < lane_dis[right_lane-1]:
                                        lane_dis[right_lane-1] = f1-Bcar_pos[1]-40
                                elif trans_pos == right_car_pos and abs(self.car_pos[1]-Bcar_pos[1]) <  banner_buffer:
                                    right_banner = 1
            else:
                print("SPEED")
                return ["SPEED"]                   
            print("lane_ctr= ", lane_ctr)
            print("lane_dis =", lane_dis)
            print("near coin distance =", near_coin)
            if near_coin != 1000000 and abs(self.car_pos[0]-near_coin_x) < 180 and self.car_pos[1]-near_coin_y < 240 and self.car_pos[1]-near_coin_y > -50:
                chase_coin = 1
                coin_dx = self.car_pos[0]-near_coin_x
                coin_dy = self.car_pos[1]-near_coin_y
            else:
                chase_coin = 0

            if front_banner == 1: return ["BRAKE"] 
            if lane_dis[mid_lane-1] <120 and vel_diff_mid > 11 :  return ["BRAKE"]
            if too_fast == 1 or too_close_f == 1: return ["BRAKE"]
            if too_close_s == 1 and right_banner == 0: return ["SPEED","MOVE_RIGHT"]
            if too_close_r == 1 and left_banner == 0: return ["SPEED","MOVE_LEFT"]
        
            if left_lane != 0 and right_lane != m+1 :
                if chase_coin == 1:
                    if coin_dx  ==  0 and front_banner == 0 : return ["SPEED"]
                    elif coin_dx  >  0 and left_banner == 0 and lane_dis[left_lane-1] > 80+buffer:  return ["MOVE_LEFT"]
                    elif coin_dx  <  0 and right_banner == 0 and lane_dis[right_lane-1] > 80+buffer :  return ["MOVE_RIGHT"]
                #elif lane_dis[mid_lane-1] == max_dis: return ["SPEED"]
                elif left_banner == 0 and lane_dis[left_lane-1] > lane_dis[mid_lane-1]+40 and lane_dis[left_lane-1] >= lane_dis[right_lane-1] : return ["SPEED","MOVE_LEFT"]
                elif right_banner == 0 and lane_dis[right_lane-1] > lane_dis[mid_lane-1]+40 and lane_dis[right_lane-1] > lane_dis[left_lane-1] : return ["SPEED","MOVE_RIGHT"]
                elif lane_dis[mid_lane-1] > 80+buffer: return ["SPEED"]
                else: return ["BRAKE"]
                
            elif left_lane == 0:
                if chase_coin == 1:
                    if coin_dx  ==  0 and front_banner == 0: return ["SPEED"]
                    elif coin_dx  <  0 and right_banner == 0:  return ["SPEED","MOVE_RIGHT"]
                #elif lane_dis[mid_lane-1] == max_dis: return ["SPEED"]
                elif lane_dis[mid_lane-1] > 80+buffer and right_banner == 0 and lane_dis[right_lane-1]  > lane_dis[mid_lane-1]+40 : return ["SPEED","MOVE_RIGHT"]
                elif lane_dis[mid_lane-1] > 80+buffer: return ["SPEED"]
                else: return ["BRAKE"]

            elif right_lane == m+1:
                if chase_coin == 1:
                    if coin_dx  ==  0 and front_banner == 0: return ["SPEED"]
                    elif coin_dx  >  0 and left_banner == 0:  return ["SPEED","MOVE_LEFT"]
                #elif lane_dis[mid_lane-1] == max_dis: return ["SPEED"]
                elif lane_dis[mid_lane-1] > 80+buffer and left_banner == 0 and lane_dis[left_lane-1] > lane_dis[mid_lane-1]+40: return ["SPEED","MOVE_LEFT"]
                elif lane_dis[mid_lane-1] > 80+buffer: return ["SPEED"]
                else: return ["BRAKE"]

        else: # my car is not on the center of each lane
            if self.car_pos[0] < 35:
                left_lane = 1
                right_lane = 2
            elif self.car_pos[0] > m*70-35:
                left_lane = m-1
                right_lane = m
            else:
                for i in range(m-1):
                    if lane_ctr[i]*lane_ctr[i+1] < 0:
                        left_lane = i+1
                        right_lane = i+2

            print("left_lane = ", left_lane,"right_lane = ", right_lane)
            print("lane_ctr= ", lane_ctr)
            print("lane_dis =", lane_dis)           

            n=len(Bcar)
            if n != 0:
                for i in range(n):
                    for car in scene_info["cars_info"]:
                        if car["id"] == Bcar[i]:
                            Bcar_vel = car["velocity"]
                            Bcar_pos = car["pos"]
                            trans_pos =Bcar_pos[0]
                            if abs(self.car_pos[0]-Bcar_pos[0]) < 70 and self.car_pos[1]-Bcar_pos[1] < 140 and self.car_pos[1]-Bcar_pos[1] > 0 and self.car_vel-Bcar_vel >= 3 :
                                front_banner = 1
                            for j in range(m):
                                if Bcar_pos[0] >= j*70+20 and  Bcar_pos[0] <= (j+1)*70-20: trans_pos = j*70+35                 
                            print(car["id"], trans_pos, Bcar_pos, Bcar_vel, f1)
                            # Find the minimun distance in left lane of my car
                            if trans_pos == left_lane*70-35 and self.car_pos[1]-Bcar_pos[1] > 0:
                                print("the car ", car["id"], "is the left lane and front of my car",self.player_no)
                                if self.car_pos[1]-Bcar_pos[1] < lane_dis[left_lane-1]:
                                    lane_dis[left_lane-1] = f1-Bcar_pos[1]-40
                                    vel_diff_left = self.car_vel-Bcar_vel
                            elif trans_pos ==  left_lane*70-35 and abs(self.car_pos[1]-Bcar_pos[1]) <  banner_buffer:
                                left_banner = 1
                            # Find the minimun distance in right-lane of my car
                            if trans_pos == right_lane*70-35 and self.car_pos[1]-Bcar_pos[1] > 0:
                                print("the car ", car["id"], "is the right lane and front of my car",self.player_no)
                                if self.car_pos[1]-Bcar_pos[1] < lane_dis[right_lane-1]:
                                    lane_dis[right_lane-1] = f1-Bcar_pos[1]-40
                                    vel_diff_right = self.car_vel-Bcar_vel
                            elif trans_pos == right_lane*70-35 and abs(self.car_pos[1]-Bcar_pos[1]) <  banner_buffer:
                                right_banner = 1
            else:
                print("SPEED")
                return ["SPEED"]
            print("near coin =", near_coin)
            if near_coin != 1000000 and abs(near_coin_x-self.car_pos[0]) < 210 and self.car_pos[1]-near_coin_y < 180 and self.car_pos[1]-near_coin_y > -40:
                chase_coin = 1
                coin_dx = self.car_pos[0]-near_coin_x
                coin_dy = self.car_pos[1]-near_coin_y                
            else:
                chase_coin = 0            

            if front_banner == 1: return ["BRAKE"]
            if lane_dis[left_lane-1] <120 or lane_dis[right_lane-1] <120:
                if vel_diff_left > 11 or vel_diff_right > 11:
                    return ["BRAKE"]
            if too_fast == 1 or too_close_f == 1: return ["BRAKE"]
            if too_close_s == 1 and right_banner == 0: return ["SPEED","MOVE_RIGHT"]
            if too_close_r == 1 and left_banner == 0: return ["SPEED","MOVE_LEFT"]
        
            if self.car_pos[0] < 35 : return ["MOVE_RIGHT"]
            elif self.car_pos[0] > m*70-35 : return ["MOVE_LEFT"]
            elif chase_coin == 1:
                if coin_dx  >  0 and left_banner == 0 and lane_dis[left_lane-1] > 80+buffer :  return ["SPEED","MOVE_LEFT"]
                elif coin_dx  <  0 and right_banner == 0 and lane_dis[right_lane-1] > 80+buffer:  return ["SPEED","MOVE_RIGHT"]
                print("lane_dis left right",lane_dis[left_lane-1] , lane_dis[right_lane-1])
            elif lane_dis[left_lane-1] == max_dis and left_banner == 0 and self.car_pos[0] > 35 : return ["SPEED","MOVE_LEFT"]
            elif lane_dis[right_lane-1] == max_dis and right_banner == 0 and self.car_pos[0] < 385: return ["SPEED","MOVE_RIGHT"]
            elif lane_dis[right_lane-1] >= lane_dis[left_lane-1] and right_banner == 0 and lane_dis[right_lane-1] > 80+buffer:
                print("SPEED and MOVE_RIGHT")
                return ["SPEED","MOVE_RIGHT"]
            elif lane_dis[right_lane-1] <= lane_dis[left_lane-1] and left_banner == 0 and lane_dis[left_lane-1] > 80+buffer:
                print("SPEED and MOVE_LEFT")
                return ["SPEED","MOVE_LEFT"]
            elif lane_dis[right_lane-1] < 80+buffer or lane_dis[left_lane-1] < 80+buffer :
                print("BRAKE")
                return ["BRAKE"]
            else:
                print("SPEED")
                return ["SPEED"]                

    def reset(self):
        """
        Reset the status
        """
        pass
