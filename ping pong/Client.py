import turtle 
from turtle import Screen
from socket import socket, AF_INET, SOCK_STREAM
import threading
import keyboard

Host='127.0.0.1'
Port=7000
ready_client =False


def game(game_window,player_1,middle_line,player_2,player_speed,ball,score):
    ball_dx,ball_dy= 1,1
    ball_speed= 1
    score_p1,score_p2=0,0
   
   
    while True:
        game_window.update()

        # Move the ball
        ball.sety(ball.ycor()+(ball_dy*ball_speed))
        ball.setx(ball.xcor()+(ball_dx*ball_speed))

        #ball movements
        if(ball.ycor()>290): # 290 = 300 (window border) - 10 (circle is 20)
            ball.sety(290)
            ball_dy*=-1

        if(ball.ycor()<-290): # 290 = 300 (window border) - 10 (circle is 20)
            ball.sety(-290)
            ball_dy*=-1    

        if(ball.xcor ()> 390 or ball.xcor() < -390 ):
            score.clear()
            if ball.xcor ()> 390:
                ball.goto(0,0)    
                ball_dx*=-1  
                score_p1+=1  

            if ball.xcor() < -390:
                ball.goto(0,0)    
                ball_dx*=-1
                score_p2+=1 
            score.write(f"Player 1: {score_p1}   Player 2: {score_p2}", align= "center", font=("Arial",14,"normal"))
       
        # Paddle and ball collisions
        if ball.xcor()<-330 and ball.xcor()>-350 and ball.ycor() > (player_1.ycor()-60) and ball.ycor() < (player_1.ycor()+60):
            ball.setx(-330)
            ball_dx *=-1

        if ball.xcor()>330 and ball.xcor()<350 and ball.ycor() > (player_2.ycor()-60) and ball.ycor() < (player_2.ycor()+60):
            ball.setx(330)
            ball_dx *=-1

        if(score_p1==5 or score_p2==5 ):
            break
    
    
    game_window.clear()        
    game_end(score_p1,score_p2)


def game_end(score_p1,score_p2):
   
    global ready_client
    def client_ready():
        client_socket.send("client".encode('UTF-8'))
        print("sending")
       
        

    end_window = turtle.Screen()
    end_window.title("end game player 1")
    end_window.setup(width =800, height=600)
    end_window.tracer(0) #set delay for update drawing
    end_window.bgcolor(0.1,0.1,0.1)
    end = turtle.Turtle()
    end.speed(0)
    end.color('red')
    end.penup()
    end.goto(0, 200)  # Adjusted position
    end.hideturtle()

    ready = turtle.Turtle()
    ready.speed(0)
    ready.color('white')
    ready.penup()
    ready.goto(0, -200)  # Adjusted position
    ready.hideturtle()
    ready.write(f"press space to start new game", align= "center", font=("Arial",20,"normal"))

   
    if(score_p1==5):
        end.color('red')
        end.write(f"Player 1 win the game", align= "center", font=("Arial",20,"normal"))
        
        
    elif(score_p2==5):
        end.color('blue')
        end.write(f"Player 2 win the game", align= "center", font=("Arial",20,"normal"))
       
        

    while True:
        end_window.update()
        if keyboard.read_key() == "space"  :
            client_ready()
            end.clear()
            ready.clear()
            
            break  
    while(ready_client!=True):
        ready.write(f"waiting player 2", align= "center", font=("Arial",20,"normal"))
        continue
    end_window.clear()
    ready_client =False
    start_game(client_socket)
    
def start_game(client_socket):    
    player_speed = 50
    def receive_thread(client_socket,player_1):
            global ready_client
            while True:
                message = client_socket.recv(1024).decode('UTF-8')
                print(message)
                if message=="server":
                        ready_client = True
                        print("ready2")
                else:
                    player_1.sety(int(message))

    def move_up():
        y_position = player_2.ycor()
        y_position += player_speed
        player_2.sety(y_position)
        client_socket.send(str(y_position).encode('UTF-8'))

    def move_down():
        y_position = player_2.ycor()
        y_position -= player_speed
        player_2.sety(y_position)
        client_socket.send(str(y_position).encode('UTF-8'))


    game_window = Screen()
    game_window.title("Ping Pong: player 1")
    game_window.bgcolor(0,0,0)
    game_window.setup(width =800, height=600)
    game_window.bgcolor(0.1,0.1,0.1)
    game_window.tracer(0) #set delay for update drawing


    # Paddle A
    player_1= turtle.Turtle()
    player_1.speed(0)
    player_1.shape('square')
    player_1.color('red')
    player_1.shapesize(stretch_len=1,stretch_wid=5)
    player_1.penup()
    player_1.goto(x=-350,y=0)

    #middle line
    middle_line= turtle.Turtle()
    middle_line.speed(0)
    middle_line.shape('square')
    middle_line.color('white')
    middle_line.shapesize(stretch_len=0.1 ,stretch_wid=25)
    middle_line.penup()
    middle_line.goto(x=0, y=0)

    # Paddle B
    player_2= turtle.Turtle()
    player_2.speed(0)
    player_2.shape('square')
    player_2.color('blue')
    player_2.shapesize(stretch_len=1,stretch_wid=5)
    player_2.penup()
    player_2.goto(x=350,y=0)

    # Ball
    ball = turtle.Turtle()
    ball.speed(0) #drawing speed (fastest) rang 0 to 10
    ball.shape('circle') 
    ball.color('white')
    ball.shapesize(stretch_len= 1, stretch_wid=1) #scale factor * default size (20px *20px) 
    ball.penup() #STOP drawing lines
    ball.goto(x=0,y=0)


    # Pen
    score=turtle.Turtle()
    score.speed(0)
    score.color('white')
    score.penup()
    score.goto(x=0,y=270)

    score.write(f"Player 1: 0  Player 2: 0", align= "center", font=("Arial",14,"normal"))
    score.hideturtle()
    # Keyboard binding
    game_window.listen()
    game_window.onkeypress(move_up, "w")
    game_window.onkeypress(move_down, "s")

    
    receive_thread = threading.Thread(target=receive_thread, args=(client_socket,player_1))
    receive_thread.start()
    game_thread = threading.Thread(target=game,args=(game_window,player_1,middle_line,player_2,player_speed,ball,score) )
    game_thread.start()

    


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((Host, Port))

start_game(client_socket)
turtle.mainloop()