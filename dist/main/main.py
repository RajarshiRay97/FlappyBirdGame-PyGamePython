import random
import pygame
from pygame import mixer
import sys

# global variables
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.884
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/nature.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomescreen():
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif click[0] == 1 and ((90 < mouse[0] < 90 + 109) and (270 < mouse[1] < 270 + 45)):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                if (90 < mouse[0] < 90 + 109) and (270 < mouse[1] < 270 + 45):
                    pygame.draw.rect(SCREEN, (0, 0, 0), (90, 270, 109, 45))
                else:
                    pygame.draw.rect(SCREEN, (72, 61, 149), (90, 270, 109, 45))
                button1text = text.render("F L Y", True, (255, 255, 255))
                SCREEN.blit(button1text, (105, 271))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                instruc = inst.render("Instruction: press Space key to fly", True, (0,0,0))
                SCREEN.blit(instruc, (2, GROUNDY-5))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 2)
    playery = int(SCREENHEIGHT / 2)
    basex = 0
    level = 1

    # create two pipe for bleating on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    UpperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']}
    ]
    LowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}
    ]
    pipevelx = -4

    playervely = -9
    playermaxvely = 10
    playerminvely = -8
    playerAccy = 1

    playerflapvel = -8  # the velocity of bird when flapping/flying
    playerflapped = False  # playerflapped is True when bird is flying otherwise false

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                if playery > 0:
                    playervely = playerflapvel
                    playerflapped = True
                    GAME_SOUNDS['wing'].play()
        crashTest = iscollide(playerx, playery, UpperPipes, LowerPipes,level, score)
        if crashTest:
            scoreline = sc.render("YOUR TOTAL SCORE", True, (255, 0, 0))
            over = overfont.render("GAME OVER", True, (0, 0, 0))
            SCREEN.blit(scoreline, (22, 75))
            SCREEN.blit(over, (25, 240))
            pygame.draw.rect(SCREEN, (72, 61, 149), (60, 300, 160, 45))
            button1text = text.render("RESTART", True, (255, 255, 255))
            SCREEN.blit(button1text, (64, 300))
            pygame.draw.rect(SCREEN, (255, 0, 0), (90, 355, 109, 45))
            button2text = text.render("QUIT", True, (255, 255, 255))
            SCREEN.blit(button2text, (105, 355))
            return
        # increasing score
        playerMidpos = playerx + GAME_SPRITES['player'].get_width() / 2
        for pipe in UpperPipes:
            pipeMidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidpos <= playerMidpos < pipeMidpos + 4:
                score += 1
                print(f'The score is {score}')
                GAME_SOUNDS['point'].play()
        # player moving
        if playervely < playermaxvely and not playerflapped:
            playervely += playerAccy
        if playerflapped:
            playerflapped = False
            GAME_SOUNDS['swooshing'].play()
        playerHieght = GAME_SPRITES['player'].get_height() / 2
        playery = playery + min(playervely, GROUNDY - playery - playerHieght)
        # moving pipes in left direction
        for upperpipe, lowerpipe in zip(UpperPipes, LowerPipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx
        # if pipe is going to out of the screen generate new pipe
        if pipevelx-1 < UpperPipes[0]['x'] < 0:
            newPipe = getRandomPipe()
            UpperPipes.append(newPipe[0])
            LowerPipes.append(newPipe[1])
        # if pipe cross the screen then remove
        if UpperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            UpperPipes.pop(0)
            LowerPipes.pop(0)
        # increasing level
        if score // 10 == level:
            pipevelx += -1
            level += 1
            print(f"Level {level}")

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(UpperPipes, LowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        levelshow = Level.render("LEVEL " + str(level), True, (0, 0, 0))
        SCREEN.blit(levelshow, (85, 15))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH - width) / 2
        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT * 0.22))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def quitscreen():
    while True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (
                    click[0] == 1 and ((90 < mouse[0] < 90 + 109) and (355 < mouse[1] < 355 + 45))):
                pygame.quit()
                sys.exit()
            elif click[0] == 1 and ((90 < mouse[0] < 90 + 109) and (300 < mouse[1] < 300 + 45)):
                mainGame()
                pygame.display.update()
            else:
                if (60 < mouse[0] < 60 + 160) and (300 < mouse[1] < 300 + 45):
                    pygame.draw.rect(SCREEN, (0, 0, 0), (60, 300, 160, 45))
                else:
                    pygame.draw.rect(SCREEN, (72, 61, 149), (60, 300, 160, 45))
                button1text = text.render("RESTART", True, (255, 255, 255))
                SCREEN.blit(button1text, (64, 300))
                if (90 < mouse[0] < 90 + 109) and (355 < mouse[1] < 355 + 45):
                    pygame.draw.rect(SCREEN, (255, 0, 0), (90, 355, 109, 45))
                else:
                    pygame.draw.rect(SCREEN, (200, 0, 0), (90, 355, 109, 45))
                button2text = text.render("QUIT", True, (255, 255, 255))
                SCREEN.blit(button2text, (105, 355))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getRandomPipe():
    PipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = int(SCREENHEIGHT / 3)
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    y1 = PipeHeight - y2 + offset
    pipex = SCREENWIDTH + 10
    pipe = [
        {'x': pipex, 'y': -y1},  # upper pipe
        {'x': pipex, 'y': y2}  # lower pipe
    ]
    return pipe


def iscollide(playerx, playery, UpperPipes, LowerPipes, level, score):
    if playery > GROUNDY - GAME_SPRITES['player'].get_height() + 10:
        GAME_SOUNDS['hit'].play()
        SCREEN.blit(GAME_SPRITES['crash'], (69, 167))
        GAME_SOUNDS['die'].play()
        return True
    if playery < 0:
        GAME_SOUNDS['hit'].play()
        acc = 1
        GAME_SOUNDS['die'].play()
        while playery < GROUNDY - 37:
            playery += acc
            acc += 2
            SCREEN.blit(GAME_SPRITES['background'], (0, 0))
            for upperpipe, lowerpipe in zip(UpperPipes, LowerPipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
            SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
            levelshow = Level.render("LEVEL " + str(level), True, (0, 0, 0))
            SCREEN.blit(levelshow, (85, 15))
            mydigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in mydigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            xoffset = (SCREENWIDTH - width) / 2
            for digit in mydigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT * 0.22))
                xoffset += GAME_SPRITES['numbers'][digit].get_width()
            SCREEN.blit(GAME_SPRITES['crash'], (69, 167))
            SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        GAME_SOUNDS['die'].play()
        return True
    pipeHieght = GAME_SPRITES['pipe'][0].get_height()
    for pipe in UpperPipes:
        if playery < pipeHieght + pipe['y'] and (abs(pipe['x'] - playerx) < GAME_SPRITES['pipe'][0].get_width() - 10):
            GAME_SOUNDS['hit'].play()
            acc = 1
            while playery < GROUNDY - 37:
                playery += acc
                acc += 2
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                for upperpipe, lowerpipe in zip(UpperPipes, LowerPipes):
                    SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
                    SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
                SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
                levelshow = Level.render("LEVEL " + str(level), True, (0, 0, 0))
                SCREEN.blit(levelshow, (85, 15))
                mydigits = [int(x) for x in list(str(score))]
                width = 0
                for digit in mydigits:
                    width += GAME_SPRITES['numbers'][digit].get_width()
                xoffset = (SCREENWIDTH - width) / 2
                for digit in mydigits:
                    SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT * 0.22))
                    xoffset += GAME_SPRITES['numbers'][digit].get_width()
                SCREEN.blit(GAME_SPRITES['crash'], (69, 167))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
            GAME_SOUNDS['die'].play()
            return True
    for pipe in LowerPipes:
        if (playery + GAME_SPRITES['player'].get_height()) > pipe['y'] and (
                abs(pipe['x'] - playerx) < GAME_SPRITES['pipe'][1].get_width() - 10):
            GAME_SOUNDS['hit'].play()
            acc = 1
            while playery < GROUNDY - 37:
                playery += acc
                acc += 2
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                for upperpipe, lowerpipe in zip(UpperPipes, LowerPipes):
                    SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
                    SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
                SCREEN.blit(GAME_SPRITES['base'], (0, GROUNDY))
                levelshow = Level.render("LEVEL " + str(level), True, (0, 0, 0))
                SCREEN.blit(levelshow, (85, 15))
                mydigits = [int(x) for x in list(str(score))]
                width = 0
                for digit in mydigits:
                    width += GAME_SPRITES['numbers'][digit].get_width()
                xoffset = (SCREENWIDTH - width) / 2
                for digit in mydigits:
                    SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREENHEIGHT * 0.22))
                    xoffset += GAME_SPRITES['numbers'][digit].get_width()
                SCREEN.blit(GAME_SPRITES['crash'], (69, 167))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
            GAME_SOUNDS['die'].play()
            return True


if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("FLAPPY BIRD GAME")

    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['crash'] = pygame.image.load('gallery/sprites/crash.png').convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUNDS['wing'] = mixer.Sound('gallery/sounds/wing.wav')
    GAME_SOUNDS['swooshing'] = mixer.Sound('gallery/sounds/swooshing.wav')
    GAME_SOUNDS['point'] = mixer.Sound('gallery/sounds/point.wav')
    GAME_SOUNDS['hit'] = mixer.Sound('gallery/sounds/hit.wav')
    GAME_SOUNDS['die'] = mixer.Sound('gallery/sounds/die.wav')

    overfont = pygame.font.Font('Fluo Gums.ttf', 25)
    sc = pygame.font.Font('Fluo Gums.ttf', 15)
    text = pygame.font.Font('Fluo Gums.ttf', 20)
    Level = pygame.font.Font('Fluo Gums.ttf', 15)
    inst = pygame.font.Font('Adventure.otf', 20)

    welcomescreen()
    mainGame()
    pygame.display.update()
    quitscreen()
