import random
import tkinter as tk
from tkinter import *
import customtkinter as customtkinter
from customtkinter import *

def update_buttons():              #tkinter saistīta funkcija
    for i in range(n//2):
        pair_buttons[i].configure(text = str(nums[i*2]) + " " + str(nums[i*2+1]))
    if(n%2==1):
        pair_buttons[n//2].configure(text = str(nums[-1]))
    else:
        pair_buttons[n//2].destroy()

class Node:
    def __init__(self, state, bank=0, points=0, value = 0, pair = 1):
        self.state = state  # šī brīža stāvoklis
        self.bank = bank  # Spēles banka
        self.points = points  # kopējie punkti
        self.children = []  # saraksts ar visiem nākamajiem stāvokļiem
        self.value = value  # virsotnes vertība
        self.pair = pair # nākamais pāris, kas būs izvēlēts

#Atrod spēles rezultātu, ja spēlētāji līdz spēles beigām nekad neizvēlas numuru bez pāra (pēdējo numuru)
def find_game_value(root):
    state = [int(i) for i in root.state]
    sum_st = sum(state)
    if((sum_st%2)!=(root.bank+(sum_st-0.5)//6+root.points+len(root.state))%2):
        if((root.points+len(root.state))%2!=sum_st%2): 
            root.value=1
        else: 
            root.value=-1
    else:
        root.value=0
# 1 - uzvar max/alpha spēlētājs, -1 - uzvar min/beta spēlētājs

def sim_alpha(d,root,prev):
    pairs_total = (len(root.state)+1)//2    # Aprēķina iespējamo pāru skaitu no pašreizējā stāvokļa

    for i in range(1,pairs_total+1):        #spēles gajiena simulācija ar kopētiem mainīgajiem jaunajai virsotnei 
        root.children.append(Node(state = root.state, points = root.points, bank = root.bank, value = 2, pair = 1))

        rc = root.children[i-1]            # pievienotais pēctecis
        
        
        if(i==pairs_total):                 # Tiek sasniegts pēdējais virknes elements
            rc.points-=1                    # Samazina punktus, jo tiek noedzēsts pēdējais elements
            rc.state = rc.state[:-1]        # Nodzēš pēdējo elementu
        else:
            num = int(rc.state[i*2-1]) + int(rc.state[i*2-2])       # saskaita pāri un atjaunina stāvokli
            if(num)>6:
                num-=6
                rc.bank+=1                  # Pievieno punktu bankai, ja summa ir lielāka par 6
            rc.points+=1                    # Pievieno punktu kopējiem punktiem, jo notikusi summēšana
            rc.state = rc.state[:i*2-2] + str(num) + rc.state[i*2:]         #Atjauno stāvokli


        if(d!= 1):                      #nākamais rekursijas solis vai rezultāta vērtības atrašana, ja ir sasniegta dziļuma robeža
            sim_beta(d-1,rc,root.value)
        else:
            find_game_value(rc)

        if(rc.value>root.value):         #vērtību salīdzinājums, lai atrastu labāko nākamo gājienu
            root.value=rc.value
            root.pair=i
            if(root.value>=prev):         #alfa/beta griešana
                return
            

def sim_beta(d,root,prev):
    pairs_total = (len(root.state)+1)//2          # Aprēķina iespējamo pāru skaitu no pašreizējā stāvokļa

    for i in range(1,pairs_total+1):              #spēles gajiena simulācija ar kopētiem mainīgajiem jaunajai virsotnei       
        root.children.append(Node(state = root.state, points = root.points, bank = root.bank, value = -2, pair = 1))
        
        rc = root.children[i-1]                   # pievienotais pēctecis
        num = int(rc.state[i*2-1]) + int(rc.state[i*2-2])
        if(num)>6:
            num-=6
            rc.bank+=1
        rc.points+=1
        rc.state = rc.state[:i*2-2] + str(num) + rc.state[i*2:]                      #
                                               

        if(d!= 1):                      #nākamais rekursijas solis vai rezultāta vērtības atrašana, ja ir sasniegta dziļuma robeža
            sim_alpha(d-1,rc,root.value)
        else:
            find_game_value(rc)

        if (rc.value < root.value):            #vērtību salīdzinājums, lai atrastu labāko nākamo gājienu
            root.value=rc.value
            root.pair=i
            if(root.value<=prev):       #alfa/beta griešana
                return


def sim_max(d,root):
    pairs_total = (len(root.state)+1)//2       # Aprēķina iespējamo pāru skaitu pašreizējā stāvoklī

    for i in range(1,pairs_total+1):           #spēles gajiena simulācija ar kopētiem mainīgajiem jaunajai virsotnei 
        root.children.append(Node(state = root.state, points = root.points, bank = root.bank, value = 2, pair = 1))

        rc = root.children[i-1]                # pievienotais pēctecis
        
        if(i==pairs_total):                    # Tiek sasniegts pēdējais virknes elements
            rc.points-=1
            rc.state = rc.state[:-1]
        else:
            num = int(rc.state[i*2-1]) + int(rc.state[i*2-2])   # saskaita pāri un atjaunina stāvokli
            if(num)>6:
                num-=6
                rc.bank+=1
            rc.points+=1
            rc.state = rc.state[:i*2-2] + str(num) + rc.state[i*2:]         #Atjauno stāvokli


        if(d!= 1):          #nākamais rekursijas solis vai rezultāta vērtības atrašana, ja ir sasniegta dziļuma robeža
            sim_min(d-1,rc)
        else:
            find_game_value(rc)

        if(rc.value>root.value):               #vērtību salīdzinājums, lai atrastu labāko nākamo gājienu
            root.value=rc.value
            root.pair=i
            

def sim_min(d,root):
    pairs_total = (len(root.state)+1)//2      # Aprēķina iespējamo pāru skaitu pašreizējā stāvoklī

    for i in range(1,pairs_total+1):          #spēles gajiena simulācija ar kopētiem mainīgajiem jaunajai virsotnei        
        root.children.append(Node(state = root.state, points = root.points, bank = root.bank, value = -2, pair = 1))
        
        rc = root.children[i-1]               # pievienotais pēctecis
        num = int(rc.state[i*2-1]) + int(rc.state[i*2-2])
        if(num)>6:
            num-=6
            rc.bank+=1
        rc.points+=1
        rc.state = rc.state[:i*2-2] + str(num) + rc.state[i*2:]                      #
                                                       

        if(d!= 1):          #nākamais rekursijas solis vai rezultāta vērtības atrašana, ja ir sasniegta dziļuma robeža
            sim_max(d-1,rc)
        else:
            find_game_value(rc)

        if (rc.value < root.value):        #vērtību salīdzinājums, lai atrastu labāko nākamo gājienu
            root.value=rc.value
            root.pair=i


def computer_move():
    global root 
    root = Node(state = "".join(str(i) for i in nums),bank = bank,points = points, value = (2 if n%2==0 else -2), pair = 1) #koka sakne
    depth=5               #uzbūvētā koka dziļums

    if(n<=depth):
        depth=n-1
    
    if(minmax_is_chosen):       #algoritma izvēle, pamatojoties uz atlasīto opciju un pašreizējo numuru virknes garumu
        if(n%2==0):
            sim_min(depth,root)
        else:        
            sim_max(depth,root)
    else:        
        if(n%2==0):
            sim_beta(depth,root,-2)
        else:        
            sim_alpha(depth,root,2)
        

def new_game():
    global chosen_pair, points, bank, computer_turn, n, player_started,minmax_is_chosen
                       
    n = int(slider.get()) #sākotnējā garuma iegūšana no slīdņa
    
    for i in range(len(pair_buttons)):  #pāru pogu atiestatīšana
        if(pair_buttons[i].winfo_exists()):
            pair_buttons[i].destroy()

    nums.clear()            #sarakstu un vērtību atiestatīšana
    pair_buttons.clear() 
    points = 0
    bank = 0

    for i in range(n):                              #noteikta garuma nejaušu skaitļu rindas izveidošana
        nums.append((int)(1+random.random()*6))
    
    chosen_pair = customtkinter.IntVar()            #pāru pogu izveide
    
    for i in range(n//2+1):
        pair_buttons.append(customtkinter.CTkRadioButton(window, hover = True, fg_color="#4158D0", hover_color= "#3547AB", variable=chosen_pair, value=i))
        pair_buttons[i].pack()
        pair_buttons[i].place(x=100+(i%5)*60, y=135+(i//5)*30)

    update_buttons()


    player_started = player_is_first.get()      #pirma spēlētāja iegūšana
    computer_turn = not player_started


    turn_label_var.set("Your turn!")        #pareizo iezīmju nosaukumu iestatīšana

    points_label_var.set("Points: 0")
    bank_label_var.set("Bank: 0")

    minmax_is_chosen = mm_ab.get()          #izvēlētā algoritma iegūšana

    computer_label_var.set("")
    if(computer_turn):
        next_move()


def next_move():
    global n,computer_turn,points,bank, root

    if(n==1):
        return

    pair = 0

    if(computer_turn):               #datora izvēlēta pāra iegūšana un tā izvadīšana vai spēlētāju pāra iegūšana
        computer_move()
        pair = root.pair
        del root
        if(pair != (n+1)//2) or n==2:
            computer_label_var.set("Computer chose: " + str(nums[pair*2-1]) + " + " + str(nums[pair*2-2]))
        else:
            computer_label_var.set("Computer chose: " + str(nums[-1]))
    else:
        pair = int(chosen_pair.get()+1)
        if pair>(n+1)//2: return



    if(n%2==1 and pair == (n+1)//2):       #pēdējā skaitļa dzēšana vai pāru summēšana, punktu un bankas vertību maiņa
        points-=1
        del nums[-1]
    else:
        nums[pair*2-1]+=nums[pair*2-2]
        points+=1
        if(nums[pair*2-1]>6):
            nums[pair*2-1]-=6
            bank+=1
        del nums[pair*2-2]

    n-=1                                  #mainīgo vērtības maiņa nākamajam gajienam
    computer_turn = not computer_turn

    update_buttons()                      #teksta un pogas informācijas maiņa

    points_label_var.set("Points: " + str(points))
    bank_label_var.set("Bank: " + str(bank))
    

    if(n==1):                                           #rezultāta izvade, ja spēle ir beigusies
        if(nums[0]%2 == (points+bank)%2):
            if((nums[0]%2==1) != player_started):
                turn_label_var.set("Player has won")
            else:
                turn_label_var.set("Computer has won")
        else:
            turn_label_var.set("Nobody has won")
    elif(computer_turn):
        next_move()






#mainīgie vēlākai lietošanai

n=1
nums = []
pair_buttons = []


#tkinter iestatījumi

window = customtkinter.CTk()
window.geometry("500x350")
window.title("Game")
window.resizable(False, False)

set_appearance_mode("dark")

player_is_first = customtkinter.BooleanVar()
R1 = customtkinter.CTkRadioButton(window, hover = True, fg_color="#4158D0", hover_color= "#3547AB",text="Player is first", variable=player_is_first, value=1)
R1.pack()
R1.place(x=15, y=17)
R2 = customtkinter.CTkRadioButton(window, hover = True, fg_color="#4158D0", hover_color= "#3547AB",text="Computer is first", variable=player_is_first, value=0)
R2.pack()
R2.place(x=15, y=57)


mm_ab = BooleanVar()
R3 = customtkinter.CTkRadioButton(window, hover = True, fg_color="#4158D0", hover_color= "#3547AB",text="MinMax", variable=mm_ab, value=True)
R3.pack()
R3.place(x=380, y=17)
R4 = customtkinter.CTkRadioButton(window, hover = True, fg_color="#4158D0", hover_color= "#3547AB",text="Alpha-beta", variable=mm_ab, value=False)
R4.pack()
R4.place(x=380, y=57)


start_button=customtkinter.CTkButton(window,text="Start new game",corner_radius = 32, fg_color="#4158D0", hover_color= "#3547AB",  command=new_game)
start_button.pack()
start_button.place(x=80, y=230)

continue_button=customtkinter.CTkButton(window,text="Next turn",corner_radius = 32, fg_color="#4158D0", hover_color= "#3547AB", command=next_move)
continue_button.pack()
continue_button.place(x=280, y=230)


turn_label_var = customtkinter.StringVar()
turn_label_var.set("Choose the options")
turn_label = customtkinter.CTkLabel(window,width=140, fg_color="#4158D0" ,textvariable=turn_label_var)
turn_label.pack()
turn_label.place(x=185, y=15)

computer_label_var = customtkinter.StringVar()
computer_label_var.set("")
computer_label = customtkinter.CTkLabel(window,width=140, fg_color="#4158D0" ,textvariable=computer_label_var)
computer_label.pack()
computer_label.place(x=185, y=90)


points_label_var = customtkinter.StringVar()
points_label = customtkinter.CTkLabel(window, width=100,fg_color="#F18700", textvariable=points_label_var)
points_label.pack()
points_label.place(x=150, y=55)

bank_label_var = customtkinter.StringVar()
bank_label = customtkinter.CTkLabel(window, width=100, fg_color="#F18700" ,textvariable=bank_label_var)
bank_label.pack()
bank_label.place(x=260, y=55)

points_label_var.set("Points: 0")
bank_label_var.set("Bank: 0")

def slider_callback(value):
    slider_label_var.set(value)

slider = CTkSlider(window, button_color = "#4158D0", button_hover_color= "#3547AB", from_= 15, to = 25, number_of_steps=10, command = slider_callback)
slider.pack()
slider.place (x=170, y= 290)

value_of_slider = slider.get()

slider_label_var = customtkinter.StringVar()
slider_label_var.set(value_of_slider)

slider_label = customtkinter.CTkLabel(window, width=35, fg_color="#F18700", textvariable= slider_label_var)
slider_label.pack()
slider_label.place(x = 125, y = 283)

slider_label_name = customtkinter.CTkLabel(window, width=55, fg_color="#F18700", text= "Length:")
slider_label_name.pack()
slider_label_name.place(x = 70, y = 283)

slider.bind("<ButtonRelease-1>", lambda event: slider_callback(slider.get()))

window.mainloop()
