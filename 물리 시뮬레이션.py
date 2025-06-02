import pygame
import pymunk
import pymunk.pygame_util
import math

# 마찰 없는 경사면을 따라 나무도막이 미끄러지는 물리 시뮬레이션

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True

# Pymunk 공간 생성
space = pymunk.Space()
space.gravity = (0, 900)  # 아래 방향 중력 (단위: 픽셀/s²)

# Debug draw
draw_options = pymunk.pygame_util.DrawOptions(screen)

# 경사면 각도 (도 단위 → 라디안)
angle_deg = 30
angle_rad = math.radians(angle_deg)

# 경사면 (Static Segment)
start = (100, 500)
length = 600
end = (start[0] + length * math.cos(angle_rad),
       start[1] - length * math.sin(angle_rad))

ramp = pymunk.Segment(space.static_body, start, end, 5)
ramp.friction = 0.0  # 마찰 없음
space.add(ramp)

# 나무도막 (Dynamic Box)
mass = 1
size = (50, 20)
moment = pymunk.moment_for_box(mass, size)

body = pymunk.Body(mass, moment)
# 도막을 경사면 위에 위치시키기
x = start[0] + 350
y = start[1] - 350
body.position = (x, y)
body.angle = -angle_rad  # 경사면과 도막 방향 정렬

shape = pymunk.Poly.create_box(body, size)
shape.friction = 0.0  # 마찰 없음

space.add(body, shape)

# 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((240, 240, 240))
    pygame.display.set_caption("마찰 없는 빗면 시뮬레이션")
    space.step(1/60)
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()