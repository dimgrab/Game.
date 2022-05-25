import tkinter
import random

def move_wrap(obj, move):   # функция движения объекта по полю
    canvas.move(obj, move[0], move[1])
    o_c = canvas.coords(obj)
    if o_c[1] < 0:
        o_c[1] = 540
    if o_c[1] > 540:
        o_c[1] = 0
    if o_c[0] < 0:
        o_c[0] = 540
    if o_c[0] > 540:
        o_c[0] = 0
    canvas.coords(obj, o_c)
def prepare_and_start():
    canvas.delete("all")
    global player, exit, fires, enemies, N_ENEMIES, n_fires, h
    h = h1   # задание количества жизней
    c = set()   # множество занятых на поле позицый
    player_pos = (random.randint(1, N_X - 1) * step, random.randint(1, N_Y - 1) * step)
    c.add(player_pos)
    while True:
        exit_pos = (random.randint(1, N_X - 1) * step, random.randint(1, N_Y - 1) * step)
        if exit_pos not in c:
            c.add(exit_pos)
            break
    player = canvas.create_image(player_pos[0], player_pos[1], image=player_pic, anchor="nw")
    exit = canvas.create_image(exit_pos[0], exit_pos[1], image=exit_pic, anchor="nw")
    fires = []
    for i in range(n_fires):
        while True:
            fire_pos = (random.randint(1, N_X - 1) * step, random.randint(1, N_Y - 1) * step)
            if fire_pos not in c:
                c.add(fire_pos)
                break
        fire = canvas.create_image(fire_pos[0], fire_pos[1], image=fire_pic, anchor="nw")
        fires.append(fire)    
    enemies = []
    for i in range(N_ENEMIES):
        while True:
            enemy_pos = (random.randint(0, N_X - 1) * step, random.randint(0, N_Y - 1) * step)
            if enemy_pos not in c:
                c.add(enemy_pos)
                break
        enemy = canvas.create_image(enemy_pos, image=enemy_pic, anchor='nw')
        enemies.append((enemy, random.choice([vsi, always_right, random_move])))
    label.config(text="Найдите выход.")
    master.bind("<KeyPress>", key_pressed)
    
def always_right(a):   # функция для движения врага всегда вправо
    return (step, 0)
def always_left(a):    # функция для движения врага всегда влево
    return (-step, 0)
def random_move(a):    # функция для движения врага в случайном направлении
    return random.choice([(step, 0), (-step, 0), (0, step), (0, -step)])
def vsi(e_c):   # функция движения в сторону игрока.
    p_c = canvas.coords(player)
    if p_c[0] - e_c[0] < 0:
        a = (-step,)
    elif p_c[0] - e_c[0] > 0:
        a = (step,)
    else:
        a = (0,)
    if p_c[1] - e_c[1] < 0:
        a = a + (-step,)
    elif p_c[1] - e_c[1] > 0:
        a = a + (step,)
    else:
        a = a + (0,)
    return a
def do_nothing(event):
    pass

def check_move():   # функция для проверки перемещения игрока.
    global h
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(f) == canvas.coords(player):
            h = h - 1
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e[0]):
            h = h - 1
    if h <= 0:
        label.config(text="Вы проиграли!")
        master.bind("<KeyPress>", do_nothing)
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
        direction = enemy[1](canvas.coords(enemy[0]))
        move_wrap(enemy[0], direction)
    check_move()
    
N_X, N_Y, step = 10, 10, 60
N_ENEMIES, n_fires, h1 = 4, 9, 1
print("На 1 сложности 3 врага, 3 препятствия и 6 единиц здоровья.")
print("На 2 сложности 6 врагов, 6 препятствий и 3 единицы здоровья.")
print("На 3 сложности 9 врагов, 9 препятствий и 1 еденица здоровья.")
print("Если сложность не указана, то в игре будет 4 врага, 9 препятствий и 1 единица здоровья.")
print('Вы можете указать другое количество врагов, препятствий и здоровья, введя "д".')
s = input("Введите сложность(1, 2, 3, д). ")
# h1 - количество жизней на даннном уровне сложности
if s == "1":
    N_ENEMIES, n_fires, h1 = 3, 3, 6
if s == "2":
    N_ENEMIES, n_fires, h1 = 6, 6, 3
if s == "3":
    N_ENEMIES = 9
if s == "д":
    N_ENEMIES, n_fires, h1 = int(input("Введите количество врагов. ")), int(input("Введите количество препятствий. ")), int(input("Введите количество здоровья. "))
master = tkinter.Tk()
player_pic = tkinter.PhotoImage(file="2.gif")
exit_pic = tkinter.PhotoImage(file="3.gif")
fire_pic = tkinter.PhotoImage(file="1.gif")
enemy_pic = tkinter.PhotoImage(file="enemy_pic.gif")

canvas = tkinter.Canvas(master, bg="white", height=step * N_Y, width=step * N_X)
canvas.pack()
restart = tkinter.Button(master, text="Начать играть.", command=prepare_and_start)
restart.pack()
label = tkinter.Label(master, text="")
label.pack()
master.mainloop()