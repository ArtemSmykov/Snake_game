import pygame
import sys
import random
import pygame_menu


class SnakeBlock:
    '''
    класс змеи
    '''
    def __init__(self, x, y):
        '''
         инициализация атрибутов класса, сохраняет x и y
         в экземпляр класса
        '''
        self.x = x
        self.y = y

    def is_inside(self):
        '''
        функция проверяет находится ли змейка внутри игрового поля или не
        при выполнении условия функции получаем ответ,
        что змейка внутри игрового поля
        проверяются координаты головы, тк голова идет впереди всей змейки
        '''
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        '''
        функция принимает два аргумента self и other
        сравнивает два экземпляра класса SneakBlock
        '''
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

def draw_block(color, row, column):
    '''
    функция приннимает переменные row, column, color,
    по которым определяет цвет и координаты блока
    '''
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1), SIZE_BLOCK,
                                     SIZE_BLOCK])
def start_the_game():
    '''
    функция выполняется при нажатии в меню кнопки Play
    запускает весь игровой цикл
    '''

    def random_apple():
        '''
        возвращает обьект класса SneakBlock в игровое поле
        по случайным координатам, не совпадающим с координатами змейки
        '''
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 9)]
    apple = random_apple()
    d_row = 0
    d_col = 1
    score = 0
    speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print('exit')
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1

        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])
        text_score = courier.render(f'Score: {score}', 0, WHITE)
        screen.blit(text_score, (SIZE_BLOCK, SIZE_BLOCK))
        text_speed = courier.render(f'Speed: {speed}', 0, WHITE)
        screen.blit(text_speed, (SIZE_BLOCK+270, SIZE_BLOCK))

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE
                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('crash')
            break

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        pygame.display.flip()

        if apple == head:
            score += 1
            speed = score // 5 + 1
            snake_blocks.append(apple)
            apple = random_apple()

        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print('crash yourself')
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)
        timer.tick(3+speed)

if __name__ == '__main__':
    pygame.init()

    SIZE_BLOCK = 20
    FRAME_COLOR = (128, 128, 128)
    WHITE = (255, 255, 255)
    BLUE = (204, 255, 255)
    RED = (224, 0, 0)
    COUNT_BLOCKS = 20
    HEADER_COLOR = (47, 53, 60)
    SNAKE_COLOR = (0, 102, 0)
    HEADER_MARGIN = 70
    MARGIN = 1
    size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
            SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]
    print(size)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Змейка')
    timer = pygame.time.Clock()
    courier = pygame.font.SysFont('courier', 50)
    menu = pygame_menu.Menu('Welcome', 400, 300,
                            theme=pygame_menu.themes.THEME_BLUE)  #
    menu.add.button('Play', start_the_game)  # взято из документации
    menu.add.button('Quit', pygame_menu.events.EXIT)  # к pygame-menu
    menu.mainloop(screen)  #