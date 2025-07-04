import os
import random
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA ={ #移動用辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.rect) -> tuple[bool,bool]:
    yoko,tate =True,True
    if rct.left <0 or WIDTH < rct.right:
        yoko=False
    if rct.top <0 or HEIGHT < rct.bottom:
        tate=False
    return yoko,tate

def gameover(screen: pg.Surface)-> None:
    # ブラックアウト
    black= pg.Surface(screen.get_size())
    black.set_alpha(150) 
    screen.blit(black, (0, 0))
    pg.draw.rect(black,(0,0,0),(0,0,WIDTH,HEIGHT))
    

    # こうかとん表示
    kokaton_sad1 = pg.image.load("fig/8.png")
    kokaton_rect1 = kokaton_sad1.get_rect(center=(370, 330))

    kokaton_sad2 = pg.image.load("fig/8.png")
    kokaton_rect2 = kokaton_sad2.get_rect(center=(740, 330))

    screen.blit(kokaton_sad1, kokaton_rect1)
    screen.blit(kokaton_sad2, kokaton_rect2)

    # ゲームオーバー文字
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(550, 330 ))
    screen.blit(text, text_rect)

    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:
    bb_imgs=[]
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)

    return bb_imgs,bb_accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    base_img = pg.image.load("fig/3.png")
    kk_img_dict = {
        (0, 0): pg.transform.rotozoom(base_img, 0, 0.9),
        (+5, 0): pg.transform.rotozoom(base_img, 135, 0.9),
    }
    return kk_img_dict.get(sum_mv, kk_img_dict[(0, 0)])











def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img=pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    # bb_rct.center=random.randint(0,WIDTH),random.randint(0,HEIGHT)
    bb_rct.centerx=random.randint(0,WIDTH)
    bb_rct.centery=random.randint(0,HEIGHT)
    vx,vy=+5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_imgs,bb_accs=init_bb_imgs()
        avx=vx*bb_accs[min(tmr//500,9)]
        avy=vy*bb_accs[min(tmr//500,9)]
        bb_img=bb_imgs[min(tmr//500,9)]

        bb_rct.move_ip(avx,avy)
        yoko,tate= check_bound(bb_rct)
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1
        screen.blit(bb_img, bb_rct)
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        kk_img = get_kk_img((0, 0))
        kk_img = get_kk_img(tuple(sum_mv))
        pg.display.update()
        tmr += 1
        clock.tick(50)



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
