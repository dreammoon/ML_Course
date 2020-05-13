"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
from mlgame.communication import ml as comm
import random

def ml_loop(side: str):
    """
    The main loop for the machine learning process
    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```
    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    ball_served = False
    hit_range = 10
    pred_range = 3
    def move_to(player, pred) : #move platform to predicted position to catch ball 
        if player == '1P':
            if scene_info["platform_1P"][0]+20  > (pred-pred_range) and scene_info["platform_1P"][0]+20 < (pred+pred_range): return 0 # NONE
            elif scene_info["platform_1P"][0]+20 <= (pred-pred_range) : return 1 # goes right
            else : return 2 # goes left
        else :
            if scene_info["platform_2P"][0]+20  > (pred-pred_range) and scene_info["platform_2P"][0]+20 < (pred+pred_range): return 0 # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-pred_range) : return 1 # goes right
            else : return 2 # goes left

    def get_blocker_direction(bkx,pre_bkx):
        if bkx > pre_bkx :
            return 1
        elif bkx < pre_bkx :
            return -1
        else :
            return 0
    
    def ml_loop_for_1P(bkx,bkxdir):
        if scene_info["ball_speed"][1] > 0  and scene_info["ball"][1] < scene_info["blocker"][1] : #ball goes down and over blocker for 1P
            hit_blocker_frames = ( scene_info["blocker"][1]+10-scene_info["ball"][1] ) // scene_info["ball_speed"][1] #frames of hit blocker
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*hit_blocker_frames)
            turn_head =0;
            turn_rear = 0
            if pred > 200 :
                pred =400 - pred
                turn_rear = 1
            elif pred < 0 :
                pred = 0- pred
                turn_head = 1
            if scene_info["ball_speed"][0] > 0 and turn_rear == 0: #ball goes right and not hit wall
                pred_1P = scene_info["ball"][0]+(scene_info["platform_1P"][1]-scene_info["ball"][1])                
                if bkxdir  == 1 :
                    predic_bkx = bkx + hit_blocker_frames//2*5
                    if predic_bkx > 170 : predic_bkx = 340 - predic_bkx
                elif bkxdir == -1 :
                    predic_bkx = bkx -hit_blocker_frames//2*5
                    if predic_bkx < 0 : predic_bkx = 0 - predic_bkx
            elif scene_info["ball_speed"][0] > 0 and turn_rear == 1: #ball goes right and hit wall
                pred_1P = scene_info["ball"][0]+(scene_info["platform_1P"][1]-scene_info["ball"][1])
                if bkxdir  == 1 :
                    predic_bkx = bkx + hit_blocker_frames//2*5+30
                    if predic_bkx > 200 : predic_bkx = 400 - predic_bkx
                elif bkxdir == -1 :
                    predic_bkx = bkx -hit_blocker_frames//2*5+30
                    if predic_bkx < 30 : predic_bkx = 30+(30 - predic_bkx)                
            elif scene_info["ball_speed"][0] < 0 and turn_head == 0 : #ball goes left and not hit wall
                pred_1P = scene_info["ball"][0]-(scene_info["platform_1P"][1]-scene_info["ball"][1])
                if bkxdir  == 1 :
                    predic_bkx = bkx +hit_blocker_frames//2*5+30
                    if predic_bkx > 200 : predic_bkx = 400 - predic_bkx
                elif bkxdir == -1 :
                    predic_bkx = bkx - hit_blocker_frames//2*5+30
                    if predic_bkx < 30 : predic_bkx = 30+(30 - predic_bkx)
            elif scene_info["ball_speed"][0] < 0 and turn_head == 1 : #ball goes left and hit wall
                pred_1P = scene_info["ball"][0]-(scene_info["platform_1P"][1]-scene_info["ball"][1])
                if bkxdir  == 1 :
                    predic_bkx = bkx + hit_blocker_frames//2*5
                    if predic_bkx > 170 : predic_bkx = 340 - predic_bkx
                elif bkxdir == -1 :
                    predic_bkx = bkx -hit_blocker_frames//2*5
                    if predic_bkx < 0 : predic_bkx = 0 - predic_bkx                
            if abs(predic_bkx-pred) < hit_range : # hit blocker situation
                if scene_info["ball_speed"][0] > 0 and turn_rear == 0 :
                    pred_1P = predic_bkx - 170
                elif scene_info["ball_speed"][0] > 0 and turn_rear == 1 :
                    pred_1P = predic_bkx + 170
                elif scene_info["ball_speed"][0] < 0 and turn_head == 0 :
                    pred_1P = predic_bkx + 170
                elif scene_info["ball_speed"][0] < 0 and turn_head == 1 :
                    pred_1P = predic_bkx - 170
        elif scene_info["ball_speed"][1] > 0 : #ball goes down for 1P
            if scene_info["ball_speed"][0] > 0 :#ball goes right
                pred_1P = scene_info["ball"][0]+(scene_info["platform_1P"][1]-scene_info["ball"][1])
            else :#ball goes left
                pred_1P = scene_info["ball"][0]-(scene_info["platform_1P"][1]-scene_info["ball"][1])
        elif scene_info["ball_speed"][1] < 0 and scene_info["ball"][1] > scene_info["blocker"][1]+20 : #ball goes up and below blocker for 1P    
            if scene_info["ball_speed"][0] > 0 :#ball goes right
                px = scene_info["ball"][0] - (scene_info["platform_1P"][1]-scene_info["ball"][1])
                if px < -80 :
                    pred_1P = 160
                elif px < 80 :
                    pred_1P = 80 - px
                else :
                    pred_1P = px - 80
            else :#ball goes left
                px = scene_info["ball"][0] + (scene_info["platform_1P"][1]-scene_info["ball"][1])
                if px > 300 :
                    pred_1P =20
                elif px > 120 :
                    pred_1P =320 - px
                else :
                    pred_1P = px + 80
        else :
            pred_1P = 80
        
        bound = pred_1P // 200 # Determine if it is beyond the boundary
        if (bound > 0): # pred > 200 # fix landing position
            if (bound%2 == 0) : 
                pred_1P = pred_1P - bound*200                    
            else :
                pred_1P = 200 - (pred_1P - 200*bound)
        elif (bound < 0) : # pred < 0
            if (bound%2 ==1) :
                pred_1P = abs(pred_1P - (bound+1) *200)
            else :
                pred_1P = pred_1P + (abs(bound)*200)
        return move_to(player = '1P',pred = pred_1P)

    def ml_loop_for_2P(bkx,bkxdir):  
        if scene_info["ball_speed"][1] < 0  and scene_info["ball"][1] > scene_info["blocker"][1]+20 : #ball goes down and over blocker for 2P
            hit_blocker_frames = (scene_info["blocker"][1]+10-scene_info["ball"][1]) // scene_info["ball_speed"][1] #frames of hit blocker
            pred = scene_info["ball"][0]+(scene_info["ball_speed"][0]*hit_blocker_frames)
            turn_head =0;
            turn_rear = 0
            if pred > 200 :
                pred =400 - pred
                turn_rear = 1
            elif pred < 0 :
                pred = 0- pred
                turn_head = 1
            if scene_info["ball_speed"][0] > 0 and turn_rear == 0: #ball goes right and not hit wall
                pred_2P = scene_info["ball"][0]+(scene_info["ball"][1]-scene_info["platform_2P"][1]-30)                
                if bkxdir  == 1 :
                    predic_bkx = bkx + hit_blocker_frames//2*5
                    if predic_bkx > 170 : predic_bkx = 340 - predic_bkx
                elif bkxdir == -1 :
                    predic_bkx = bkx -hit_blocker_frames//2*5
                    if predic_bkx < 0 : predic_bkx = 0 - predic_bkx
            elif scene_info["ball_speed"][0] > 0 and turn_rear == 1: #ball goes right and hit wall
                pred_2P = scene_info["ball"][0]+(scene_info["ball"][1]-scene_info["platform_2P"][1]-30)
                if bkxdir  == 1 :
                    predic_bkx = bkx + hit_blocker_frames//2*5+30
                    if predic_bkx > 200 : predic_bkx = 400 - predic_bkx
                elif bkxdir == -1 :
                    predic_bkx = bkx -hit_blocker_frames//2*5+30
                    if predic_bkx < 30 : predic_bkx = 30+(30 - predic_bkx)                        
            elif scene_info["ball_speed"][0] < 0 and turn_head == 0  : #ball goes left and not hit wall
                pred_2P = scene_info["ball"][0]-(scene_info["ball"][1]-scene_info["platform_2P"][1]-30)
                if bkxdir  == 1 :
                    predic_bkx = bkx +hit_blocker_frames//2*5+30
                    if predic_bkx > 200 : predic_bkx = 400 - predic_bkx
                elif bkxdir == -1 :
                    predic_bkx = bkx - hit_blocker_frames//2*5+30
                    if predic_bkx < 30 : predic_bkx = 30+(30 - predic_bkx)
            elif scene_info["ball_speed"][0] < 0 and turn_head == 1  : #ball goes left and hit wall
                pred_2P = scene_info["ball"][0]-(scene_info["ball"][1]-scene_info["platform_2P"][1]-30)
                if bkxdir  == 1 :
                    predic_bkx = bkx + hit_blocker_frames//2*5
                    if predic_bkx > 170 : predic_bkx = 340 - predic_bkx
                elif bkxdir == -1 :
                    predic_bkx = bkx -hit_blocker_frames//2*5
                    if predic_bkx < 0 : predic_bkx = 0 - predic_bkx                
            if abs(predic_bkx-pred) < hit_range : # hit blocker situation
                if scene_info["ball_speed"][0] > 0 and turn_rear == 0 :
                    pred_2P = predic_bkx - 170
                elif scene_info["ball_speed"][0] > 0 and turn_rear == 1 :
                    pred_2P = predic_bkx + 170
                elif scene_info["ball_speed"][0] < 0 and turn_head == 0 :
                    pred_2P = predic_bkx + 170
                elif scene_info["ball_speed"][0] < 0 and turn_head == 1 :
                    pred_2P = predic_bkx - 170
        elif scene_info["ball_speed"][1] < 0 : #ball goes down for 2P
            if scene_info["ball_speed"][0] > 0 :#ball goes right
                pred_2P = scene_info["ball"][0]+(scene_info["ball"][1]-scene_info["platform_2P"][1]-30)
            else :#ball goes left
                pred_2P = scene_info["ball"][0]-(scene_info["ball"][1]-scene_info["platform_2P"][1]-30)
        elif scene_info["ball_speed"][1] > 0 and scene_info["ball"][1] < scene_info["blocker"][1] : #ball goes up and below blocker for 2P    
            if scene_info["ball_speed"][0] > 0 :#ball goes right
                px = scene_info["ball"][0] - (scene_info["ball"][1]-scene_info["platform_2P"][1]-30)
                if px < -80 :
                    pred_2P = 160
                elif px < 80 :
                    pred_2P = 80 - px
                else :
                    pred_2P = px - 80
            else :#ball goes left
                px = scene_info["ball"][0] + (scene_info["ball"][1]-scene_info["platform_2P"][1]-30)
                if px > 300 :
                    pred_2P =20
                elif px > 120 :
                    pred_2P =320 - px
                else :
                    pred_2P = px + 80
        else :
            pred_2P = 80

        bound = pred_2P// 200 
        if (bound > 0):
            if (bound%2 == 0):
                pred_2P = pred_2P - bound*200 
            else :
                pred_2P = 200 - (pred_2P - 200*bound)
        elif (bound < 0) :
            if bound%2 ==1:
                pred_2P = abs(pred_2P - (bound+1) *200)
            else :
                pred_2P = pred_2P + (abs(bound)*200)
        return move_to(player = '2P',pred = pred_2P)

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    pre_bkx = 80
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.recv_from_game()
        bkx=scene_info["blocker"][0]

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info["status"] != "GAME_ALIVE":
            # Do some updating or resetting stuff
            ball_served = False

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # 3.4 Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_to_game({"frame": scene_info["frame"], "command": "SERVE_TO_LEFT"})
            ball_served = True
        else:
            if side == "1P":
                pd1 = get_blocker_direction(bkx,pre_bkx)
                if pd1 == 0 : pd1 = ppd1
                command = ml_loop_for_1P(bkx,pd1)
                pre_bkx = bkx
                ppd1 = pd1
            else:
                pd2 = get_blocker_direction(bkx,pre_bkx)
                if pd2 == 0 : pd2 = ppd2                
                command = ml_loop_for_2P(bkx,pd2)
                pre_bkx = bkx
                ppd2 = pd2

        # for parameter in scene_info.keys():
        #    print("parameters are ", parameter)
        #print("blocker position : ", scene_info["blocker"][0], scene_info["blocker"][1])
            #print("speed ", scene_info["ball_speed"])
            #print("ball ", scene_info["ball"])
            #print("platform_1P ",scene_info["platform_1P"], "platform_2P", scene_info["platform_2P"])
            if command == 0:
                comm.send_to_game({"frame": scene_info["frame"], "command": "NONE"})
            elif command == 1:
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_RIGHT"})
            else :
                comm.send_to_game({"frame": scene_info["frame"], "command": "MOVE_LEFT"})
