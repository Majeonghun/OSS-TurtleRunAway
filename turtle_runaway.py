# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random
import time, math

class RunawayGame:
    def __init__(self, canvas, runners, chaser, catch_radius=75):
        self.canvas = canvas
        self.runners = runners  # 리스트로 도망자 3명
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.start_time = None
        self.score = 900
        self.caught_count = 0

        # 도망자 초기화
        for runner in self.runners:
            runner.shape(shape2)
            runner.penup()

        chaser.shape(shape1)
        chaser.penup()

        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def check_catch(self, runner):
        dx = runner.xcor() - self.chaser.xcor()
        dy = runner.ycor() - self.chaser.ycor()
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.start_time = time.time()
        runner_positions = [
            (-init_dist / 2, 150),
            (-init_dist / 2, 0),
            (-init_dist / 2, -150)
        ]
        for i, runner in enumerate(self.runners):
            runner.setpos(runner_positions[i])
            runner.setheading(0)

        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        self.canvas.bgpic("background.gif")
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        for runner in self.runners:
            runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runners[0].pos(), self.runners[0].heading())

        elapsed = int(time.time() - self.start_time)
        time_score = max(1500 - elapsed * 10, 0)
        catch_score = self.caught_count * 500
        self.score = time_score + catch_score

        for runner in self.runners[:]:
            if self.check_catch(runner):
                self.caught_count += 1
                runner.hideturtle()
                self.runners.remove(runner)

        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.color("white")
        self.drawer.write(f'Score: {self.score} | Time: {elapsed}s | Caught: {self.caught_count}',
                          align="left", font=("Arial", 14, "normal"))

        if len(self.runners) == 0 or time_score == 0:
            self.score = time_score + self.caught_count * 500
            self.game_over(elapsed, time_score)
        else:
            self.score = time_score + self.caught_count * 500
            self.canvas.ontimer(self.step, self.ai_timer_msec)

    def game_over(self, elapsed, time_score):
        # 모든 도망자와 쫓는 사람 숨기기
        for runner in self.runners:
            runner.hideturtle()
            del runner
        self.chaser.hideturtle()
        del self.chaser

        self.drawer.clear()
        if time_score == 0:
            self.canvas.bgpic("lose_ending.gif")
            self.drawer.goto(0, 150)
            self.drawer.color("red")
            self.drawer.write(f"⌚ TimeOver! ⌚", align="center", font=("Arial", 28, "bold"))
        else:
            self.canvas.bgpic("win_ending.gif")
            self.drawer.goto(0, 150)
            self.drawer.color("red")
            self.drawer.write(f"🏁 Finish! 🏁", align="center", font=("Arial", 28, "bold"))

        self.drawer.goto(0, 80)
        self.drawer.color("white")
        self.drawer.write(f"Survived {elapsed} sec\nFinal Score: {self.score}",
                          align="center", font=("Arial", 24, "bold"))
        self.drawer.goto(0, -20)
        self.drawer.color("yellow")
        self.drawer.write("Thanks for playing!\nPress Esc to exit",
                          align="center", font=("Arial", 18, "normal"))

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=5):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        canvas.onkeypress(lambda: self.move_within_bounds(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.move_within_bounds(-self.step_move), 'Down')
        canvas.onkeypress(lambda: self.turn_and_check(-self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.turn_and_check(self.step_turn), 'Right')
        canvas.listen()

    def move_within_bounds(self, distance):
        self.forward(distance)
        self.check_bounds()

    def turn_and_check(self, angle):
        self.right(angle)
        self.check_bounds()

    def check_bounds(self):
        x, y = self.pos()
        if x < -300: self.setx(-300)
        elif x > 300: self.setx(300)
        if y < -300: self.sety(-300)
        elif y > 300: self.sety(300)

    def run_ai(self, opp_pos, opp_heading):
        pass  # 수동 이동이므로 AI 없음

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=60, step_turn=30):
        super().__init__(canvas)
        self.step_move = step_move
        self.boost_move = 120
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        dx = self.xcor() - opp_pos[0]
        dy = self.ycor() - opp_pos[1]
        angle = math.degrees(math.atan2(dy, dx))
        self.setheading(angle + (random.randint(70, 100) * random.choice([-1, 1])))

        mode = random.randint(0, 1)
        if mode == 0: self.forward(self.boost_move)
        else: self.forward(self.step_move)
        self.check_bounds()

    def check_bounds(self):
        x, y = self.pos()
        if x < -300: self.setx(-300); self.right(180)
        elif x > 300: self.setx(300); self.right(180)
        if y < -300: self.sety(-300); self.right(180)
        elif y > 300: self.sety(300); self.right(180)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Midnight Thief")
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # 캐릭터 모양 등록
    shape1 = "police.gif"
    shape2 = "runner.gif"
    screen.register_shape(shape1)
    screen.register_shape(shape2)

    # 초기 배경
    screen.bgpic("opening.gif")
    screen.update()

    Is_start = False  # 게임 시작 여부

    def start_game(event=None):
        global Is_start
        if not Is_start:
            Is_start = True  # 이제 한 번만 실행
            # 도망자 3명
            runner1 = RandomMover(screen)
            runner2 = RandomMover(screen)
            runner3 = RandomMover(screen)
            chaser = ManualMover(screen)

            game = RunawayGame(screen, [runner1, runner2, runner3], chaser)
            game.drawer.clear()
            game.start()


    # 스페이스 키 이벤트 등록 (조건문 밖)
    screen.onkeypress(start_game, "space")
    screen.onkeypress(root.destroy, "Escape")

    screen.listen()
    screen.mainloop()
