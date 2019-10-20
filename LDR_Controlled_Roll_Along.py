#!/usr/bin/env python
# coding: utf-8

# In[1]:

#Author: Daniel Kulik

# Setup Python
import random, os, glob, time, sys, statistics
from pyfirmata import Arduino, util
import pygame
pygame.init()
pygame.mixer.init()

#################################################################################
#Setup Arduino Connection,Variables and Test Condition
try:
    board = Arduino('COM3')#baudrate=57600
    it = util.Iterator(board)
    it.start()
    pygame.time.delay(100)
    #board.analog[0].enable_reporting()

    analog_0 = board.get_pin('a:1:i')
    analog_1 = board.get_pin('a:2:i')
    analog_2 = board.get_pin('a:3:i')
    analog_3 = board.get_pin('a:4:i')
    LED_Lose = board.get_pin('d:10:o')
    LED_Win = board.get_pin('d:11:o')

    pygame.time.delay(200)
    V0_start = float(analog_0.read())
    V1_start = float(analog_1.read())
    V2_start = float(analog_2.read())
    V3_start = float(analog_3.read())
    error_list = [V0_start,V1_start,V2_start,V3_start]
    stdev = 10*statistics.stdev(error_list)
    print(stdev)
    
except:
    pass

LDR = 5
count = 0
V0 = 0
V1 = 0
V2 = 0
V3 = 0

def LDR_motion(V0,V1,V2,V3):

    if (V0<V1-stdev) & (V0<V2-stdev) & (V0<V3-stdev):
        motion = 0 #Move UP
        return motion
        
    elif (V1<V0-stdev) & (V1<V2-stdev) & (V1<V3-stdev):
        motion = 1 #Move DOWN
        return motion
        
    elif (V2<V0-stdev) & (V2<V1-stdev) & (V2<V3-stdev):
        motion = 2 #Move LEFT
        return motion
        
    elif (V3<V0-stdev) & (V3<V1-stdev) & (V3<V2-stdev):
        motion = 3 #Move RIGHT
        return motion
        
    else:
        motion = 5 #Dummy value to make no motion occur
        return motion
    
##################################################################################
#Setup Pygame/Window & Variables
HEIGHT = 650
WIDTH = 1200

radius = 10
running = False
paused = False

x = 10
y = 10
maze = []
streamers_x = []
streamers_y = []
skill = 7
runs = 0
current = 0
volume = 0.15

cursor = 0
blank = False
silent = False
schoice = 0
cx1 = 35
cx2 = 20
cy1 = 110
cy2 = 100

FONT1 = pygame.font.SysFont("comicsansms", 35)
FONT2 = pygame.font.SysFont("arial", 25)
FONT3 = pygame.font.SysFont("Aharoni", 30)

try:
    folder =  os.path.abspath(os.path.join(__file__, "../"))
except:
    folder = os.path.join(os.path.dirname(sys.argv[0]), "")
    
gsfold = os.path.join(folder, 'Game_Stats/')

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Roll Along!")

# Test To Determine Correct Rendering Speed
def speed_test():

    if not os.path.isdir(gsfold):
        os.makedirs(gsfold)

    if os.path.isfile(gsfold + 'Speed.txt'):
        speed = open(gsfold + "Speed.txt","r")

    else:
        speed = open(gsfold + "Speed.txt","w+")
        tic = time.time()
        test1 = []
        for i in range(5000000):
            test1.append('x')

        toc = time.time()
        guage = toc-tic
        speed.write(str(guage))

    latency = speed.read()
    try:
        wait = int(-10*float(latency)+13)
    except:
        latency = guage
        wait = int(-10*float(latency)+13)
        
    return wait

wait = speed_test()

#Background Image
def background():

    bground = []
    bfold = os.path.join(folder, 'Background/')

    if not os.path.isdir(bfold):
        os.makedirs(bfold)

    extensions = [ "jpg", "jpeg", "png", "bmp", "gif" ]
    try:
        for extension in extensions:
            for backg in glob.glob(bfold + "*." + extension):
                bground.append(backg)
    
        back = random.randint(0,len(bground)-1)
        bg = pygame.image.load(str(bground[back]))
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        return bg
    
    except:
        pass
try:
    bg = background()
    if bg == None:
        wait = int(wait*3.4 + 3.8)
except:
    wait = int(wait*3.4 + 3.8)

# Setup Audio
def music(schoice):
    songs = []
        
    mfold = os.path.join(folder, 'Music/')

    if not os.path.isdir(mfold):
        os.makedirs(mfold)
    
    for tune in glob.glob(mfold + "*.mp3"):
        songs.append(tune)

    if (schoice == 0) or (schoice==len(songs)):
        schoice = 0
        songs = random.sample(songs,len(songs))
        
    pygame.mixer.music.load(str(songs[schoice]))
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(volume)

try:
    music(schoice)
except:
    pass

# Setup High Score Logfile
def HScore():
        
    if os.path.isfile(gsfold + 'HScore.txt'):
        Hi_score = open(gsfold + "HScore.txt","r")
        current = Hi_score.read()
        Hi_score.close()

    else:
        Hi_score = open(gsfold + "HScore.txt","w+")
        Hi_score.write(str(runs))
        current = str(runs)
        Hi_score.close()

    return current

current = HScore()

# Setup High Score Updater
def HFile(current):

    try:
        for i in range(15):
            LED_Win.write(1)
            pygame.time.delay(100)
            LED_Win.write(0)
            pygame.time.delay(100)
    except:
        pass
    
    if runs>=int(current):
        Hi_score = open(gsfold + "HScore.txt","w+")
        Hi_score.write(str(runs))
        current = str(runs)
        Hi_score.close()
        
    return current

# Create Randomized Maze
def Start_Maze():
    
    for rows in range(random.randint(20,30)):

        t = (random.randint(20,WIDTH-30)) #position of columns    
        n = (random.randint(10,HEIGHT-10)) #center of column postions
        v = random.randint(20,150) #size of columns
        
        for stacks in range(25):
    
            maze.append(t)
            maze.append(random.randint(n-v,n+v))

# Generate Maze
def Draw_Maze():
    
    for i in range(len(maze)-1):
        if (i % 2) == 0:
            pygame.draw.rect(win, (80,30,30), (maze[i], maze[i+1], radius, radius))

# Create Player Icon           
def Draw_circle(x,y):
    pygame.draw.circle(win, (255,0,0), (int(x), int(y)), radius)

# Streamer Functions       
def move(items):
    for item in items:
        item[0] += item[2]
        item[1] += item[3]
    
def removeUseless_x(items):
    for item in items:
        if item[1] > HEIGHT:
            items.remove(item)
            
def removeUseless_y(items):
    for item in items:
        if item[0] < 25:
            items.remove(item)

# Create Moving Objects To Avoid aka Streamers            
def Draw_streamers():
    
    num_s = 1
    xvals = set()
    yvals = set()
    
    ticker = random.randint(0,skill)
    attack = random.randint(0,3)
    
    if (ticker>=(random.randint(5,10))) & (attack>0): 
        while len(xvals) < num_s:
            pos = random.randint(40, WIDTH-15)
            xvals.add(pos)
            
        DY = random.randint(2,5)
        for val in xvals:
            streamers_x.append([val,0,0,DY])
        
    for item in streamers_x:        
        pygame.draw.circle(win, (50, 30, 150),(item[0], item[1]), 4)
        
    if (ticker>=(random.randint(5,10))) & (attack==0): 
        while len(yvals) < num_s:
            pos = random.randint(10, HEIGHT)
            yvals.add(pos)
            
        DX = random.randint(2,5)
        for val in yvals:
            streamers_y.append([WIDTH,val,-DX,0])
        
    for item in streamers_y:        
        pygame.draw.circle(win, (50, 30, 150),(item[0], item[1]), 4)
        
    move(streamers_x)
    move(streamers_y)
    removeUseless_x(streamers_x)
    removeUseless_y(streamers_y)

# Define Losing Parameters: Streamer Encounter   
def Lose():
    
    for itemx in streamers_x:
        if ((x-12<=itemx[0]) & 
            (x+12>=itemx[0]) & 
            (y-12<=itemx[1]) & 
            (y+12>=itemx[1])):
            running = False
            return running
    
    for itemy in streamers_y:
        if ((x-12<=itemy[0]) & 
            (x+12>=itemy[0]) & 
            (y-12<=itemy[1]) & 
            (y+12>=itemy[1])):
            running = False
            return running
        
    else:
        running = True
        return running

# Display Successive Runs Completed
def winning():

    pygame.draw.rect(win, (0, 128, 0), (WIDTH-40 , 12, 3.5*radius, 2.5*radius),1)
    nr_wins = FONT2.render(str(runs), True, (0, 128, 0))
    win.blit(nr_wins, (WIDTH-22 , 10))
    

def redrawGameWindow():
    
    try:
        if not blank:
            win.blit(bg, [0, 0])
        else:
            win.fill((0,0,0))
    except:
        win.fill((0,0,0))
        
    Draw_circle(x,y) 
    Draw_Maze()
    Draw_streamers()
    winning()
            
    pygame.display.update()
    
run = True
while run:

    # Start Game Run
    if running:

        LDR = LDR_motion(V0,V1,V2,V3)
        count += 1
        print(V0,V1,V2,V3,LDR)
    
        for event in pygame.event.get():
            pass

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Pause Function
        if event.type == pygame.KEYDOWN:

            if (event.key == pygame.K_SPACE):

                paused = not paused

                while paused:
                    
                    try:
                        pygame.mixer.music.pause()
                    except:
                        pass
                    
                    pygame.time.delay(300)
                    
                    for event in pygame.event.get():
                        
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        if event.type == pygame.KEYDOWN:

                            if (event.key == pygame.K_SPACE):
                                
                                try:
                                    pygame.mixer.music.unpause()
                                except:
                                    pass

                                paused = not paused
                
            # Update Player Movement & Maze Encounters
        if (LDR==0) & (y>=15) & ((count%2)==0):
            
            yes = True
            for i in range(len(maze)-1): 
                if (((i % 2) == 0) &
                    (x-10<=maze[i]) &
                    (x+10>=maze[i]) &
                    (y-12>=maze[i+1]) &
                    (y-20<=maze[i+1])):
                    yes = False
                    break
            
            if yes:    
                y = y - 7
                
        if (LDR==1) & (y<=HEIGHT-15) & ((count%2)==0):
            
            yes = True
            for i in range(len(maze)-1):
                if (((i % 2) == 0) &
                    (x-10<=maze[i]) &
                    (x+10>=maze[i]) &
                    (y+10<=maze[i+1]) &
                    (y+17>=maze[i+1])):
                    yes = False
                    break
                    
            if yes:    
                y = y + 7
                   
        if (LDR==2) & (x>=15) & ((count%2)==0):
            
            yes = True
            for i in range(len(maze)-1): 
                if (((i % 2) == 0) &
                    (x-10>=maze[i]) &
                    (x-22<=maze[i]) &
                    (y-10<=maze[i+1]) &
                    (y+10>=maze[i+1])):
                    yes = False
                    break
            if yes:
                x = x - 7
                
        if (LDR==3) & ((count%2)==0):

            # Setup Next Run/Restart Screen
            if x>=(WIDTH-7):
                x = 10
                y = 10
                maze = []
                streamers_x = []
                streamers_y = []
                runs += 1
                pygame.time.delay(200)
                Start_Maze()
                current = HFile(current)
                
            yes = True
            for i in range(len(maze)-1): 
                if (((i % 2) == 0) &
                    (x+10<=maze[i]) &
                    (x+17>=maze[i]) &
                    (y-10<=maze[i+1]) &
                    (y+10>=maze[i+1])):
                    yes = False
                    break
                
            if yes:    
                x = x + 7

        # Test Lose Paramaters      
        running = Lose()

        try:
            if not running:
                for i in range(15):
                    LED_Lose.write(1)
                    pygame.time.delay(100)
                    LED_Lose.write(0)
                    pygame.time.delay(100)
        except:
            pass

        if (pygame.mixer.music.get_busy() == False) & (not silent):
            try:
                schoice +=1
                music(schoice)
            except:
                pass

            
        redrawGameWindow()
        #pygame.time.delay(1)
        V0 = float(analog_0.read())
        V1 = float(analog_1.read())
        V2 = float(analog_2.read())
        V3 = float(analog_3.read())

    else:

        try:
            if not blank:
                win.blit(bg, (0, 0))
            else:
                win.fill((0,0,0))
        except:
            win.fill((0,0,0))

        # Startup Screen
        start = FONT1.render("Play", True, (0, 128, 0))
        settings = FONT1.render("Settings", True, (0, 128, 0))
        leave = FONT1.render("Exit", True, (0, 128, 0))
        caution = FONT1.render("*Please Ensure You Are In A Room With Uniform Light*", True, (0, 150, 70))
        high_score = FONT2.render("Best Run: " + current, True, (0, 128, 0))
        cursor_txt1 = FONT3.render(">", True, (50, 30, 150))
        cursor_txt2 = FONT3.render("_", True, (50, 30, 150))
        
        win.blit(start, (55, 100))
        win.blit(settings, (55, 170))
        win.blit(leave, (55, 240))
        win.blit(caution, (55, 540))
        win.blit(high_score, (WIDTH-150, 20))
        win.blit(cursor_txt1, (cx1, cy1))
        win.blit(cursor_txt2, (cx2, cy2))
        
        if skill==6:
            easy = FONT2.render("Skill: Easy", True, (0, 128, 0))
            win.blit(easy, (WIDTH-150, 50))
            
        if skill==7:
            moderate = FONT2.render("Skill: Moderate", True, (0, 128, 0))
            win.blit(moderate, (WIDTH-150, 50))
            
        if skill==9:
            hard = FONT2.render("Skill: Hard", True, (0, 128, 0))
            win.blit(hard, (WIDTH-150, 50))
        
        pygame.display.flip()
        done = False

        if (pygame.mixer.music.get_busy() == False) & (not silent):
            try:
                schoice +=1
                music(schoice)
            except:
                pass  

        # Reset Starting Conditions/Start Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            #Inside Game Options
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN)  & (cursor==0):
                    
                    running = True
                    x = 10
                    y = 10
                    maze = []
                    streamers_x = []
                    streamers_y = []
                    runs = 0
                    Start_Maze()

                if (event.key == pygame.K_RETURN)  & (cursor==2):

                    pygame.quit()
                    sys.exit()

                if (event.key == pygame.K_RETURN)  & (cursor==1):

                    settings = True
                    cursor = 0
                    cy1 = 110
                    cy2 = 100

                    # Change Game Settings
                    while settings:
                        
                        try:
                            if not blank:
                                win.blit(bg, (0, 0))
                            else:
                                win.fill((0,0,0))    
                        except:
                            win.fill((0,0,0))

                        Audio = FONT1.render("Audio", True, (0, 128, 0))
                        Display = FONT1.render("Display", True, (0, 128, 0))
                        Difficulty = FONT1.render("Difficulty", True, (0, 128, 0))
                        Hremove = FONT1.render("Reset High Score", True, (0, 128, 0))
                        MM = FONT1.render("Return To Main Menu", True, (0, 128, 0))
                        cursor_txt3 = FONT3.render(">", True, (50, 30, 150))
                        cursor_txt4 = FONT3.render("_", True, (50, 30, 150))
                        xcom = FONT1.render("r- to remove;  i- to insert;  e- easy;  m- moderate;  h- hard", True, (0, 128, 0))
                        high_score = FONT2.render("Best Run: " + current, True, (0, 128, 0))        
                        Volume = FONT1.render(str(int(volume*200)) + "%  +- to adjust", True, (0, 128, 0))

                        win.blit(Audio, (55, 100))
                        win.blit(Display, (55, 170))
                        win.blit(Difficulty, (55, 240))
                        win.blit(Hremove, (55, 310))
                        win.blit(MM, (55, 380))
                        win.blit(cursor_txt3, (cx1, cy1))
                        win.blit(cursor_txt4, (cx2, cy2))
                        win.blit(xcom, (55, HEIGHT-75))
                        win.blit(high_score, (WIDTH-150, 20))
                        
                        if cursor==0:
                            win.blit(Volume, (300, 100))
                        
                        if skill==6:
                            easy = FONT2.render("Skill: Easy", True, (0, 128, 0))
                            win.blit(easy, (WIDTH-150, 50))
                            
                        if skill==7:
                            moderate = FONT2.render("Skill: Moderate", True, (0, 128, 0))
                            win.blit(moderate, (WIDTH-150, 50))
                            
                        if skill==9:
                            hard = FONT2.render("Skill: Hard", True, (0, 128, 0))
                            win.blit(hard, (WIDTH-150, 50))
                            
                        
                        pygame.display.flip()

                        for event in pygame.event.get():
                            
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            if event.type == pygame.KEYDOWN:

                                if (cursor==0):

                                    if (event.key == pygame.K_r):
                                        try:
                                            pygame.mixer.music.stop()
                                        except:
                                            pass
                                        silent = True
                                        volume = 0.0
                                        
                                    if (event.key == pygame.K_i):
                                        
                                        if volume==0.0:
                                            volume = 0.15
                                        try:
                                            music(schoice)
                                            silent = False
                                        except:
                                            pass
                                        
                                    if (event.unicode == "+") & (volume<=0.5):
                                        try:
                                            volume += 0.025
                                            pygame.mixer.music.set_volume(volume)
                                        except:
                                            pass
                                        
                                    if (event.unicode == "-") & (volume>0.0):
                                        try:
                                            volume -= 0.025
                                            pygame.mixer.music.set_volume(volume)
                                        except:
                                            pass
                                              
                                if (cursor==1):
                                    
                                    if (event.key == pygame.K_r):
                                        
                                        win.fill((0,0,0))
                                        pygame.display.update()
                                        wait = speed_test()
                                        wait = int(wait*3.4 + 3.8)
                                        blank = True
                                        
                                    if (event.key == pygame.K_i):
                                        
                                        bg = background()
                                        blank = False
                                        wait = speed_test()

                                if (cursor==2):

                                    if (event.key == pygame.K_e):
                                        skill = 6

                                    if (event.key == pygame.K_m):
                                        skill = 7

                                    if (event.key == pygame.K_h):
                                        skill = 9

                                if (event.key == pygame.K_r) & (cursor==3):
                                    current = '0'
                                    Hi_score = open(gsfold + "HScore.txt","w+")
                                    Hi_score.write(current)
                                    Hi_score.close()
                                              
                                if (event.key == pygame.K_RETURN)  & (cursor==4): 

                                    settings = False                      
                                              
                                if (event.key == pygame.K_DOWN) & (cursor<4):

                                    cursor += 1
                                    cy1 += 70
                                    cy2 += 70

                                if (event.key == pygame.K_UP) & (cursor>0):
                                    
                                    cursor -= 1
                                    cy1 -= 70
                                    cy2 -= 70

                        pygame.time.delay(10)

                    cursor = 0
                    cy1 = 110
                    cy2 = 100
                    
                if (event.key == pygame.K_DOWN) & (cursor<2):
                    
                    cursor += 1
                    cy1 += 70
                    cy2 += 70

                if (event.key == pygame.K_UP) & (cursor>0):
                    
                    cursor -= 1
                    cy1 -= 70
                    cy2 -= 70
    
    pygame.time.delay(wait)

pygame.quit()
sys.exit()


# In[ ]:




