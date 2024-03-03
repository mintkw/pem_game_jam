import pygame as pg
from shell_interface import ShellContent


def main():
    WIDTH = 800
    HEIGHT = 600
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('new shell')
    font = pg.font.Font(pg.font.match_font('sfnsmono'), 17)
    clock = pg.time.Clock()
    color = pg.Color('white')

    pg.key.set_repeat(500, 100)  # set keys to repeatedly send pygame.KEYDOWN events
    # ... after the first 500ms and then every 100 ms.

    # initialise a shell object
    prompt = "(base) user@device ~ % "
    shell = ShellContent.Shell(prompt, font, WIDTH, screen, color)

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
                elif event.key == pg.K_u:
                    if event.mod & pg.KMOD_CTRL:
                        shell.clear_current_command()

                else:
                    shell.enter_character(event.unicode)

        shell.render()

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
