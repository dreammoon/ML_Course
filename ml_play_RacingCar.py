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
        for car in scene_info["cars_info"]:
            if car["id"] == self.player_no:
                self.car_vel = car["velocity"]
                self.car_pos=car["pos"]
                f1 = self.car_pos[1]-40
                f2 = self.car_pos[1]+40
                s1 = self.car_pos[0]-20
                s2 = self.car_pos[0]+20
            else:
                Bcar.append(car["id"])
        print("my car position = ",self.car_pos,"my velocity = ",self.car_vel)
        if self.car_pos == () :
            print("SPEED")
            return ["SPEED"]
        print("Bcars = ", Bcar)
        
        m = 9
        max_dis = 1000
        left_banner = 0
        right_banner = 0
        vel_diff_mid = 0
        vel_diff_left = 0
        vel_diff_right = 0
        lane_pos = []
        lane_dis = []
        lane_ctr =[]
        buffer = 25
        banner_buffer = 60
        for i in range(m):
            lane_pos.append(i*70+35)
            lane_dis.append(max_dis)
            lane_ctr.append(lane_pos[i]-self.car_pos[0])
        left_lane = 0
        right_lane = 0
        mid_lane = 0
        for i in range(m):
            if lane_ctr[i] == 0:
                left_lane = i
                mid_lane = i+1
                right_lane = i+2
        
        if mid_lane != 0:
            n=len(Bcar)
            if n != 0:
                for i in range(n):
                    for car in scene_info["cars_info"]:
                        if car["id"] == Bcar[i]:
                            Bcar_vel = car["velocity"]
                            Bcar_pos = car["pos"]
                            trans_pos = Bcar_pos[0]
                            if Bcar[i] < 100:
                                for j in range(m):
                                    if Bcar_pos[0] >= j*70-5 and  Bcar_pos[0] < (j+1)*70-5: trans_pos = j*70+35
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

            if lane_dis[mid_lane-1] <120 and vel_diff_mid > 11: return ["BRAKE"]
        
            if left_lane != 0 and right_lane != m+1 :
                if lane_dis[mid_lane-1] == max_dis: return ["SPEED"]
                elif left_banner == 0 and lane_dis[left_lane-1] > lane_dis[mid_lane-1]+40 and lane_dis[left_lane-1] >= lane_dis[right_lane-1] : return ["SPEED","MOVE_LEFT"]
                elif right_banner == 0 and lane_dis[right_lane-1] > lane_dis[mid_lane-1]+40 and lane_dis[right_lane-1] > lane_dis[left_lane-1] : return ["SPEED","MOVE_RIGHT"]
                elif lane_dis[mid_lane-1] > 80+buffer: return ["SPEED"]
                else: return ["BRAKE"]
                
            elif left_lane == 0:
                if lane_dis[mid_lane-1] == max_dis: return ["SPEED"]
                elif lane_dis[mid_lane-1] > 80+buffer and right_banner == 0 and lane_dis[right_lane-1]  > lane_dis[mid_lane-1]+40 : return ["SPEED","MOVE_RIGHT"]
                elif lane_dis[mid_lane-1] > 80+buffer: return ["SPEED"]
                else: return ["BRAKE"]

            elif right_lane == m+1:
                if lane_dis[mid_lane-1] == max_dis: return ["SPEED"]
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
                            if Bcar[i] < 100:
                                for j in range(m):
                                    if Bcar_pos[0] >= j*70-5 and  Bcar_pos[0] < (j+1)*70-5: trans_pos = j*70+35                 
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

            if lane_dis[left_lane-1] <120 or lane_dis[right_lane-1] <120:
                if vel_diff_left > 11 or vel_diff_right > 11:
                    return ["BRAKE"]           
        
            if lane_dis[left_lane-1] == max_dis and left_banner == 0 and self.car_pos[0] > 35 : return ["SPEED","MOVE_LEFT"]
            elif lane_dis[right_lane-1] == max_dis and right_banner == 0 and self.car_pos[0] < 385: return ["SPEED","MOVE_RIGHT"]
            elif self.car_pos[0] < 35 : return ["MOVE_RIGHT"]
            elif self.car_pos[0] > m*70-35 : return ["MOVE_LEFT"]
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
