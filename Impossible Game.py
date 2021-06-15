import sys
import os
import numpy as np
import pygame
import random
from pygame.locals import *
from Entity import Entity
from Player import Player
from Enemy import Enemy
from Species import Species
from Network import Network

def main():
    path = "C:\\Users\\Fritz\\Documents\\Impossible Game\\"
    if len(sys.argv) == 1:
        humanGame(path)
        return
    inp = 16
    hidden = 0
    size = 20
    speciesName = ""
    if sys.argv[1:].__contains__("-n"):
        speciesName = sys.argv[sys.argv.index("-n") + 1]
        species = Species(path, speciesName, inp, hidden)
        species.newpop(size)
    draw = False
    if sys.argv[1:].__contains__("-d"):
        draw = True
    if sys.argv[1:].__contains__("-f"):
        if (speciesName == ""):
            speciesName = sys.argv[sys.argv.index("-f") + 1]
            species = Species(path, speciesName, inp, hidden)
            n = int(sys.argv[sys.argv.index("-f") + 2])
        else:
            n = int(sys.argv[sys.argv.index("-f") + 1])
        forwardGen(path, draw, species, size, inp, hidden, n)
    if sys.argv[1:].__contains__("-r"):
        speciesName = sys.argv[sys.argv.index("-r") + 1]
        species = Species(path, speciesName, inp, hidden)
        gen = sys.argv[sys.argv.index("-r") + 2]
        runGen(path, draw, species, size, inp, hidden, gen, 1)
    if sys.argv[1:].__contains__("-s"):
        speciesName = sys.argv[sys.argv.index("-s") + 1]
        species = Species(path, speciesName, inp, hidden)
        gen = sys.argv[sys.argv.index("-s") + 2]
        number = sys.argv[sys.argv.index("-s") + 3]
        network = Network(species.path + "Gen" + str(gen) + "\\" + number + "\\", inp, hidden)
        machineGame(draw, network)
        

def runGen(path, draw, species, size, inp, hidden, gen, n):
    print("Gen" + str(gen))
    path = species.path + "Gen" + str(gen) + "\\"
    ascores = []
    fitnesses = []
    for x in range(size):          
        network = Network(path + str(x) + "\\", inp, hidden)
        results = []
        scores = []
        totals = []
        for y in range(n):
            results.append(machineGame(draw, network))
        for y in range(n):
            scores.append(results[y][0])
            totals.append(results[y][0] + results[y][1])
        print("Number " + str(x) + " Scores: ")
        print(scores)
        # for y in range(n):
        #     totals[y] = totals[y]*totals[y]/10000
        print("Number " + str(x) + " Fitnesses: ")
        print(totals)
        ascore = np.average(scores)
        ascores.append(ascore)
        print("Number " + str(x) + " Average Scores: " + str(ascore))
        fitness = np.average(totals)
        fitnesses.append(fitness)
        print("Number " + str(x) + " Average Fitnesses: " + str(fitness) + "\n\n")
    print("\nAverage Scores: " + str(np.average(ascores)))
    print("Average Fitness: " + str(np.average(fitnesses)) + "\n\n")
    return fitnesses    


def forwardGen(path, draw, species, size, inp, hidden, n):
    #Forward n generations
    for x in range(n):
        gen = species.currentGen()
        #Run 10 times and take average
        fitnesses = runGen(path, draw, species, size, inp, hidden, gen, 10)
        average = np.average(fitnesses)
        f = open(species.path + "Fitness.txt", "a")
        f.write("Gen" + str(gen) + " Average Fitness: " + str(average) + "\n")
        f.close()
        tosort = []
        for fit in fitnesses:
            tosort.append(fit)
        tosort.sort(reverse=True)
        rank = []
        #Sort by index
        while len(rank) < size:
            fit = tosort[len(rank)]
            fitness = np.array(fitnesses)
            indices = np.where(fitness == fit)
            for i in indices[0]:
                rank.append(i)
        total = int(size/2)
        species.breed(rank[:total])


def machineGame(draw, network):
    #Setup game
    width = 1600
    height = 900
    score = 0
    bonus = 0
    player = Player(width/2, height/2, width, height)
    spawns = ((width/10, height/10), (width*9/10, height/10), (width/10, height*9/10-27), (width*9/10, height*9/10-27))
    enemies = []
    four = True
    if four:
        enemies.append( Enemy(spawns[0], width, height, player) )
        enemies.append( Enemy(spawns[1], width, height, player) )
        enemies.append( Enemy(spawns[2], width, height, player) )
        enemies.append( Enemy(spawns[3], width, height, player) )
    else:
        enemies.append( Enemy(spawns[random.randint(0, 3)], width, height, player) )

    if draw:
        pygame.init()
        screen = pygame.display.set_mode([width, height])
        clock = pygame.time.Clock()
        font = pygame.font.SysFont('Comic Sans MS', 30)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            #Get player move
            inp = player.getInput(enemies, network.inp)
            out = network.getOutput(inp)
            dx = 0
            dy = 0
            if out[0] > 0:
                dy -= 1
            if out[1] > 0:
                dx -= 1
            if out[2] > 0:
                dy += 1
            if out[3] > 0:
                dx += 1    
            player.setVelocity((dx, dy))

            #Update game
            score += 1
            if four == False:
                if (score%250 == 0):
                    enemies.append( Enemy(spawns[random.randint(0, 3)], width, height, player) )

            player.update()
            bonus += max(0, (player.getAverageVelocity() - 100)/20)
            if player.hit:
                running = False
            if player.xwall:
                bonus -= 600
                bonus /= 2
                running = False
            if player.ywall:
                bonus -= 350
                bonus /= 2
                running = False
            for enemy in enemies:
                enemy.update()

            screen.fill((255, 255, 255))
            #Scores
            scoreText = font.render(str(score), True, (0, 0, 0))
            screen.blit(scoreText, (width/2-50, 25))
            #Entities
            player.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            
            #Flip
            pygame.display.flip()
            clock.tick(100)    

        #Exit
        pygame.quit()
        return (score, bonus)

    else:
        running = True
        while running:
            #Get player move
            inp = player.getInput(enemies, network.inp)
            out = network.getOutput(inp)
            dx = 0
            dy = 0
            if out[0] > 0:
                dy -= 1
            if out[1] > 0:
                dx -= 1
            if out[2] > 0:
                dy += 1
            if out[3] > 0:
                dx += 1    
            player.setVelocity((dx, dy))

            #Update game
            score += 1
            if four == False:
                if (score%250 == 0):
                    enemies.append( Enemy(spawns[random.randint(0, 3)], width, height, player) )

            player.update()
            bonus += max(0, (player.getAverageVelocity() - 100)/20)
            if player.hit:
                running = False
            if player.xwall:
                bonus -= 600
                bonus /= 2
                running = False
            if player.ywall:
                bonus -= 350
                bonus /= 2
                running = False
            for enemy in enemies:
                enemy.update()

        return (score, bonus)



def humanGame(path):
    #Setup pygame
    pygame.init()
    draw = True
    width = 1600
    height = 900
    screen = pygame.display.set_mode([width, height])
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    font2 = pygame.font.SysFont('Comic Sans MS', 20)

    #Read data
    file1 = open(path + "Highscore.txt", "r")
    highscore = int(file1.read())
    file1.close()

    #Setup game
    score = 0
    player = Player(width/2, height/2, width, height)
    spawns = ((width/10, height/10), (width*9/10, height/10), (width/10, height*9/10), (width*9/10, height*9/10))
    enemies = []
    enemies.append( Enemy(spawns[random.randint(0, 3)], width, height, player) )

    #Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Get player move
        pressed = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if pressed[K_w]:
            dy -= 1
        if pressed[K_a]:
            dx -= 1
        if pressed[K_s]:
            dy += 1
        if pressed[K_d]:
            dx += 1    
        player.setVelocity((dx, dy))

        #Update game
        score += 1
        if (score%250 == 0):
            enemies.append( Enemy(spawns[random.randint(0, 3)], width, height, player) )


        player.update()
        if player.hit or player.xwall or player.ywall:
            if score > highscore:
                file1 = open(path + "Highscore.txt", "w")
                file1.write(str(score))
                file1.close()
            running = False
        for enemy in enemies:
            enemy.update()


        #Draw
        if draw:
            #Background
            screen.fill((255, 255, 255))
            #Scores
            scoreText = font.render(str(score), True, (0, 0, 0))
            screen.blit(scoreText, (width/2-50, 25))
            highscoreText = font2.render("Highscore: " + str(highscore), True, (0, 0, 0))
            screen.blit(highscoreText, (width*9/10, 25))
            #Entities
            player.draw(screen)
            for enemy in enemies:
                enemy.draw(screen)
            
            #Flip
            pygame.display.flip()
            clock.tick(100)    
    print("Score: " + str(score))
    #Exit
    pygame.quit()

if __name__ == "__main__":
    main()