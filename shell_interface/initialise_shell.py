import pygame as pg
from shell_interface import ShellContent


def shell_main():
    WIDTH = 800
    HEIGHT = 600
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('new shell')
    font = pg.font.Font(pg.font.match_font('sfnsmono'), 15)
    clock = pg.time.Clock()
    color = pg.Color('white')

    pg.key.set_repeat(500, 75)  # set keys to repeatedly send pygame.KEYDOWN events
    # ... after the first 500ms and then once every 75 ms.

    # initialise a shell object
    prompt = "(koopa) larrypig@larrypig / $ "
    shell = ShellContent.Shell(prompt, font, WIDTH, HEIGHT, screen, color)

    done = False

    while not done:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    shell.enter_command()

                elif event.key == pg.K_BACKSPACE:
                    shell.backspace()

                # shortcuts
                elif event.key == pg.K_u and (event.mod & pg.KMOD_CTRL):
                    shell.clear_current_command()

                elif event.key == pg.K_UP and not shell.prev_selected:
                    shell.clear_current_command()
                    shell.prev_selected = True
                    for ch in shell.prev_command:
                        shell.enter_character(ch)

                elif event.key == pg.K_DOWN and shell.prev_selected:
                    shell.clear_current_command()
                    shell.prev_selected = False
                    for ch in shell.current_command:
                        shell.enter_character(ch)

                else:
                    shell.enter_character(event.unicode)

        shell.render()

        pg.display.flip()
        clock.tick(60)


def shellmain2():
    pg.init()
    shell_main()
    pg.quit()
