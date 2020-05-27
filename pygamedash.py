import pygame
from datetime import datetime
import random
import numpy as np 
import math

# ======
# colors
# ======

BLACK = ( 0  , 0  , 0  )
WHITE = ( 255, 255, 255)
GREEN = ( 0  , 204, 0  )
RED   = ( 255, 0  , 0  )
PURPLE= ( 204,  51, 255)

def strftdelta(tdelta):
    tdiff = tdelta.total_seconds()
    minutes, seconds = divmod(tdiff, 60)
    return "%2d:%05.2f"%(minutes,seconds)

def listadd(a,b):
    a = list(a)
    b = list(b)
    for i in range(len(a)):
        b[i] += a[i]
    return b

def addtext(txt,font,color,topleft,surf):
    txtobj = font.render(txt,True,color)
    surf.blit(txtobj,topleft)
    return txtobj

def addtext_center(txt,font,color,center,surf):
    txtobj = font.render(txt,True,color)
    txtrect = txtobj.get_rect().center
    surf.blit(txtobj,listadd(center,[-txtrect[0],-txtrect[1]]))
    return txtobj

def loadnscale(fname,finalsize):
    png = pygame.image.load(fname).convert_alpha()
    size = png.get_size()
    scale = float(finalsize)/max(size)
    png = pygame.transform.rotozoom(png, 0, scale)
    return png

def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


def logger_entry():
    return "11111"

def main(fpsflag):     
    # init
    pygame.init()
    clock    = pygame.time.Clock()
    screensz = (800,600)
    gearlist = ['1','N','2','3','4','5','6']
    logger = []
    starttime = datetime.now()
        # set logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Customized Dash")
        # create window
    screen = pygame.display.set_mode(screensz)
        # font
    font = pygame.font.SysFont("Arial",200)
    medium_font = pygame.font.SysFont("Arial",50)
    small_font = pygame.font.SysFont("Arial",30,bold=False)
        # Load images
    iconsz = 40
    batt_png = loadnscale(r'icons/batt.png',iconsz)
    water_png = loadnscale(r'icons/water_temp.png',iconsz)
    protractor_png = loadnscale(r'icons/protractor.png',400)
    rpm_empty_png = loadnscale(r'icons/rpmV2_1.png',700)
    rpm_empty_png.set_colorkey(WHITE)
    rpm_full_png = loadnscale(r'icons/rpmV2_2.png',700)
    rpm_full_png.set_colorkey(WHITE)
    front_png = loadnscale(r'icons/front.png',200)
        # Rotate images
    front_png_deg = []
    for deg in range(-900,900):
        rotated = rotate(front_png, deg/10.0, [400,350], pygame.math.Vector2(0,-100))
        front_png_deg.append(rotated)

    running  = True
    counter = 0
    while running:
        # gets all event from the event queue
        for event in pygame.event.get():
            # exit condition
            if event.type == pygame.QUIT:
                running = False
        
        #=============Logic===============
        gear = gearlist[round(counter/100)%7]
        logger.append(logger_entry())
        leanangle = round(90+math.sin(counter/100)*55,1)
        rpm = round(10000+math.sin(counter/50)*6000)
        counter += 1
        #============Drawing==============
        screen.fill(WHITE)
        # Render Gear section
        gear_rect = pygame.draw.rect(screen, RED, [25, 375, 140, 180],5)
        if gear == 'N':
            gear_txt = addtext_center(gear,font,GREEN,gear_rect.center,screen)
        else:
            gear_txt = addtext_center(gear,font,BLACK,gear_rect.center,screen)

        # Render Time Section
            # Global 
        time_caption = small_font.render("Current Time",True,BLACK)
        screen.blit(time_caption,listadd(gear_rect.topleft,[150,105]))
        time_txt = medium_font.render(datetime.now().strftime("%H:%M:%S"),True,BLACK)
        screen.blit(time_txt,listadd(gear_rect.topleft,[150,130]))

        laptime_caption = small_font.render("Last Lap",True,BLACK)
        screen.blit(laptime_caption,listadd(gear_rect.topleft,[150,30]))
        laptime_txt = medium_font.render("1:59.063",True,BLACK)
        screen.blit(laptime_txt,listadd(gear_rect.topleft,[150,55]))

        best_laptime_caption = small_font.render("Best Lap",True,BLACK)
        screen.blit(best_laptime_caption,listadd(gear_rect.topleft,[350,30]))
        best_laptime_txt = medium_font.render("1:58.574",True,PURPLE)
        screen.blit(best_laptime_txt,listadd(gear_rect.topleft,[350,55]))

        this_laptime_caption = small_font.render("This Lap",True,BLACK)
        screen.blit(this_laptime_caption,listadd(gear_rect.topleft,[550,30]))
        this_lap = strftdelta(datetime.now()-starttime)
        this_laptime_txt = medium_font.render(this_lap,True,BLACK)
        screen.blit(this_laptime_txt,listadd(gear_rect.topleft,[550,55]))

        # Render RPMs
        screen.blit(rpm_empty_png, [20,15])
        l7width = 23.6
        g7width = 49.66
        leadwidth = 6.0
        if rpm<=7000:
            rpm_band = leadwidth+l7width*(rpm-1000)/1000
        else:
            rpm_band = leadwidth+l7width*6 + g7width*(rpm-7000)/1000
        screen.blit(rpm_full_png,[20,15],[0,0,rpm_band,980])

        # Render Status icons
        status_bar_loc = [400,490]
        screen.blit(batt_png, status_bar_loc) 
        batt_txt = small_font.render(str(12.35)+" V",True,BLACK)
        screen.blit(batt_txt,listadd(status_bar_loc,[50,3]))

        screen.blit(water_png, listadd(status_bar_loc,[150,0])) 
        water_txt = small_font.render(str(216+random.randint(-5,5))+" F",True,BLACK)
        screen.blit(water_txt,listadd(status_bar_loc,[200,3]))

        # Render Right misc data display
        screen.blit(protractor_png, [200,150])
        screen.blit(front_png_deg[round(leanangle*10)][0], front_png_deg[round(leanangle*10)][1]) 
        lean_text = small_font.render(str(round(leanangle-90)), True, BLACK)
        lean_text = pygame.transform.rotate(lean_text, 90-leanangle)
        r = 215
        screen.blit(lean_text, listadd([380, 335],[-r*math.cos(leanangle/180*math.pi),-r*math.sin(leanangle/180*math.pi)]))
        # Others
        # pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
        # pygame.draw.ellipse(screen, BLACK, [20,20,250,100], 2)
        if fpsflag:
            fps = str(int(clock.get_fps()))
            fps_txt = medium_font.render(fps,True,BLACK)
            screen.blit(fps_txt,[10,10])

        pygame.display.flip()
        clock.tick(120)
    
    # =========Stop and Clean up============
    # save log file
    logfname = '2020-05-15-1831.txt'
    with open(logfname, 'w') as f:
        for item in logger:
            f.write("%s\n" % item)
    
    # Quite engine
    pygame.quit()
     

if __name__=="__main__":
    main(True)