import tkinter
import random

def move_wrap(obj, move):
    canvas.move(obj, move[0], move[1])
    if canvas.coords(player)[1] < 0:
        player_pos = canvas.coords(player)
        player_pos[1] = 540
        canvas.coords(player, player_pos)
    if canvas.coords(player)[1] > 600:
        player_pos = canvas.coords(player)
        player_pos[1] = 30
        canvas.coords(player, player_pos)
    if canvas.coords(player)[0] < 0:
        player_pos = canvas.coords(player)
        player_pos[0] = 540
        canvas.coords(player, player_pos)
    if canvas.coords(player)[0] > 600:
        player_pos = canvas.coords(player)
        player_pos[0] = 30
        canvas.coords(player, player_pos)
def prepare_and_start():
    canvas.delete("all")
    global player, exit, fires, enemies
    player_pos = (random.randint(1, N_X - 1) * step, random.randint(1, N_Y - 1) * step)
    exit_pos = (random.randint(1, N_X - 1) * step, random.randint(1, N_Y - 1) * step)
    player = canvas.create_image(player_pos[0], player_pos[1], image=player_pic, anchor="nw")
    exit = canvas.create_image(exit_pos[0], exit_pos[1], image=exit_pic, anchor="nw")
    n_fires = 9
    fires=[]
    for i in range(n_fires):
        fire_pos = (random.randint(1, N_X - 1) * step, random.randint(1, N_Y - 1) * step)
        fire = canvas.create_image(fire_pos[0], fire_pos[1], image=fire_pic, anchor="nw")
        fires.append(fire)    
    label.config(text="Найди выход!")
    master.bind("<KeyPress>", key_pressed)
    N_ENEMIES = 4
    enemies = []
    for i in range(N_ENEMIES):
        enemy_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
        enemy = canvas.create_image(enemy_pos, image=enemy_pic, anchor='nw')
        enemies.append((enemy, random.choice([always_right, random_move])))   
    
def always_right():
    return (step, 0)
def random_move():
    return random.choice([(step, 0), (-step, 0), (0, step), (0, -step)])
def do_nothing(x):
    pass

def check_move():
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(f)[0] + 30 > canvas.coords(player)[0] > canvas.coords(f)[0] - 30 and canvas.coords(f)[1] + 30 >  canvas.coords(player)[1] > canvas.coords(f)[1] - 30:
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        a = canvas.coords(e[0])
        if canvas.coords(player) == a:
            label.config(text="Ты проиграл.")
            master.bind("<KeyPress>", do_nothing)
        if a[0] > 540:
            a[0] = 0
        if a[0] < 0:
            a[0] = 540
        if a[1] > 540:
            a[1] = 0
        if a[1] < 0:
            a[1] = 540
        canvas.coords(e[0], a)
def key_pressed(event):
    if event.keysym == 'Up':
        move_wrap(player, (0, -step))
    if event.keysym == "Down":
        move_wrap(player, (0, step))
    if event.keysym == "Right":
        move_wrap(player, (step, 0))
    if event.keysym == "Left":
        move_wrap(player, (-step, 0))
    for enemy in enemies:
        direction = enemy[1]() 
        move_wrap(enemy[0], direction)    
    check_move()

master = tkinter.Tk()

step = 60
N_X = 10
N_Y = 10
player_pic = tkinter.PhotoImage(file="2.gif")
exit_pic = tkinter.PhotoImage(file="3.gif")
fire_pic = tkinter.PhotoImage(file="1.gif")
enemy_pic = tkinter.PhotoImage(file="enemy_pic.gif")
canvas = tkinter.Canvas(master, bg="white", height=step * N_Y, width=step * N_X)
restart = tkinter.Button(master, text="Начать заново", command=prepare_and_start)
restart.pack()
label = tkinter.Label(master, text="")
label.pack()
canvas.pack()
master.bind("<KeyPress>", do_nothing)
master.mainloop()