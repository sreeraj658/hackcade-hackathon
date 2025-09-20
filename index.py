import pygame, sys, math, random, copy
pygame.init()

# ------------------- SCREEN -------------------
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rage Realm")
clock = pygame.time.Clock()
FPS = 60

# ------------------- PLAYER -------------------
player = pygame.Rect(100, HEIGHT - 250, 20, 40)
PLAYER_SPEED = 5
player_vel_y = 0
GRAVITY = 1
JUMP_STRENGTH = -16
on_ground = False
player_state = "idle"
facing_right = True

# ------------------- DEATH -------------------
dead = False
particles = []
death_timer = 0
DEATH_DURATION = 50

# ------------------- LEVELS -------------------
current_level = 0
DEFAULT_TORCHES = [(150,600),(600,450),(1050,320)]
level_templates = []

# ------------------- LEVEL DEFINITIONS -------------------
# Level 1
level_templates.append({
    "platforms":[
        pygame.Rect(0,650,WIDTH,70),
        pygame.Rect(220,540,160,20),
        pygame.Rect(420,500,160,20),
        pygame.Rect(660,460,160,20),
        pygame.Rect(920,420,180,20)
    ],
    "spikes":[pygame.Rect(860,630,80,20)],
    "disappearing":[],
    "fake":[{"rect": pygame.Rect(420,500,160,20),"falling":False,"vel":0,"start_y":500}],
    "falling_spikes":[],
    "saws":[{"center":(560,350),"radius":100,"angle":0.0,"speed":0.045,"r":20}],
    "popup":[],
    "holes":[],
    "chains":[{"x":500,"y":200,"length":100,"swing":0,"speed":0.04}],
    "moving_platforms":[{"rect":pygame.Rect(660,460,160,20),"dir":1,"range":100,"start_x":660}],
    "key":pygame.Rect(940,380,28,28),
    "door":pygame.Rect(1120,360,60,100),
    "torches":[(150,600),(550,480),(900,420)]
})

# Level 2
level_templates.append({
    "platforms":[
        pygame.Rect(0,650,WIDTH,70),
        pygame.Rect(180,560,140,20),
        pygame.Rect(380,520,160,20),
        pygame.Rect(600,480,160,20),
        pygame.Rect(820,440,160,20),
        pygame.Rect(1040,400,160,20)
    ],
    "spikes":[pygame.Rect(980,630,80,20)],
    "disappearing":[],
    "fake":[],
    "falling_spikes":[{"rect":pygame.Rect(620,160,40,40),"falling":False,"start_y":160}],
    "saws":[],
    "popup":[{"rect":pygame.Rect(760,630,40,20),"active":False}],
    "holes":[],
    "chains":[{"x":700,"y":300,"length":120,"swing":0,"speed":0.05}],
    "moving_platforms":[{"rect":pygame.Rect(600,480,160,20),"dir":1,"range":80,"start_x":600}],
    "key":pygame.Rect(1060,360,28,28),
    "door":pygame.Rect(1160,340,60,100),
    "torches":[(150,600),(650,450),(1050,380)]
})

# Level 3
level_templates.append({
    "platforms":[
        pygame.Rect(0,650,WIDTH,70),
        pygame.Rect(200,560,150,20),
        pygame.Rect(420,510,150,20),
        pygame.Rect(660,470,150,20),
        pygame.Rect(900,430,150,20)
    ],
    "spikes":[pygame.Rect(880,630,80,20)],
    "disappearing":[],
    "fake":[],
    "falling_spikes":[],
    "saws":[{"center":(560,350),"radius":100,"angle":0.0,"speed":0.045,"r":20}],
    "popup":[],
    "holes":[{"rect":pygame.Rect(300,650,120,70),"active":True}],
    "chains":[{"x":800,"y":250,"length":90,"swing":0,"speed":0.06}],
    "moving_platforms":[{"rect":pygame.Rect(420,510,150,20),"dir":1,"range":120,"start_x":420}],
    "key":pygame.Rect(920,390,28,28),
    "door":pygame.Rect(1100,360,60,100),
    "torches":[(150,600),(600,440),(1000,420)]
})

# Level 4
level_templates.append({
    "platforms":[
        pygame.Rect(0,650,WIDTH,70),
        pygame.Rect(220,560,150,20),
        pygame.Rect(420,520,150,20),
        pygame.Rect(640,480,150,20),
        pygame.Rect(860,440,150,20),
        pygame.Rect(1060,400,150,20)
    ],
    "spikes":[pygame.Rect(740,630,80,20)],
    "disappearing":[{"rect":pygame.Rect(640,480,150,20),"timer":0,"active":True}],
    "fake":[],
    "falling_spikes":[{"rect":pygame.Rect(500,160,40,40),"falling":False,"start_y":160}],
    "saws":[{"center":(1120,330),"radius":60,"angle":0.0,"speed":0.06,"r":18}],
    "popup":[{"rect":pygame.Rect(1040,630,40,20),"active":False}],
    "holes":[],
    "chains":[{"x":900,"y":200,"length":80,"swing":0,"speed":0.07}],
    "moving_platforms":[{"rect":pygame.Rect(860,440,150,20),"dir":1,"range":100,"start_x":860}],
    "key":pygame.Rect(1080,360,28,28),
    "door":pygame.Rect(1160,340,60,100),
    "torches":[(150,600),(650,470),(1120,330)]
})

# Level 5
level_templates.append({
    "platforms":[
        pygame.Rect(0, 650, WIDTH, 70),
        pygame.Rect(200, 560, 150, 20),
        pygame.Rect(420, 520, 150, 20),
        pygame.Rect(640, 480, 150, 20),
        pygame.Rect(860, 440, 150, 20),
        pygame.Rect(1060, 400, 150, 20),
    ],
    "spikes":[pygame.Rect(920, 630, 80, 20)],
    "disappearing":[{"rect": pygame.Rect(640, 480, 150, 20), "timer": 0, "active": True}],
    "fake":[{"rect": pygame.Rect(420, 520, 150, 20), "falling": False, "vel": 0, "start_y": 520}],
    "falling_spikes":[
        {"rect": pygame.Rect(720, 160, 40, 40), "falling": False, "start_y": 160},
        {"rect": pygame.Rect(960, 160, 40, 40), "falling": False, "start_y": 160}
    ],
    "saws":[
        {"center": (700, 300), "radius": 90, "angle": 0.0, "speed": 0.05, "r": 20},
        {"center": (960, 360), "radius": 70, "angle": 1.0, "speed": 0.06, "r": 18}
    ],
    "popup":[{"rect": pygame.Rect(880, 630, 40, 20), "active": False}],
    "holes":[{"rect": pygame.Rect(320, 650, 120, 70), "active": True}],
    "chains":[],
    "moving_platforms":[],
    "key": pygame.Rect(1040, 360, 28, 28),
    "door": pygame.Rect(1180, 340, 60, 100),
    "torches": [(150,600),(650,450),(1050,360)]
})

# Level 6
level_templates.append({
    "platforms":[
        pygame.Rect(0,650,WIDTH,70),
        pygame.Rect(250,580,180,20),
        pygame.Rect(500,520,180,20),
        pygame.Rect(780,460,160,20),
        pygame.Rect(1020,400,160,20)
    ],
    "spikes":[pygame.Rect(900,630,80,20)],
    "disappearing":[{"rect":pygame.Rect(500,520,180,20),"timer":0,"active":True}],
    "fake":[],
    "falling_spikes":[{"rect":pygame.Rect(620,160,40,40),"falling":False,"start_y":160}],
    "saws":[{"center":(700,460),"radius":100,"angle":0.0,"speed":0.05,"r":20}],
    "popup":[],
    "holes":[{"rect":pygame.Rect(320,650,120,70),"active":True}],
    "chains":[{"x":800,"y":300,"length":100,"swing":0,"speed":0.05}],
    "moving_platforms":[{"rect":pygame.Rect(780,460,160,20),"dir":1,"range":100,"start_x":780}],
    "key":pygame.Rect(1040,360,28,28),
    "door":pygame.Rect(1180,340,60,100),
    "torches": [(150,600),(650,450),(1050,360)]
})

# ------------------- FUNCTIONS -------------------
active = {}

def load_level(index):
    global active, current_level, death_timer, dead, particles, player, player_vel_y, on_ground, player_state
    current_level=index
    active=copy.deepcopy(level_templates[index])
    for s in active.get("saws",[]):
        s["x"]=s["center"][0]+math.cos(s.get("angle",0))*s["radius"]
        s["y"]=s["center"][1]+math.sin(s.get("angle",0))*s["radius"]
    for fp in active.get("fake",[]):
        if "start_y" not in fp: fp["start_y"]=fp["rect"].y
    active["key_collected"]=False
    player.x,player.y=100,HEIGHT-250
    player_vel_y=0
    on_ground=False
    player_state="idle"
    dead=False
    particles=[]
    death_timer=0
    for fp in active.get("fake",[]):
        fp["falling"]=False; fp["vel"]=0; fp["rect"].y=fp["start_y"]
    for dsp in active.get("disappearing",[]):
        dsp["active"]=True; dsp["timer"]=0
    for fs in active.get("falling_spikes",[]):
        fs["falling"]=False; fs["rect"].y=fs["start_y"]
    for ps in active.get("popup",[]):
        ps["active"]=False

def kill_player():
    global dead, particles, death_timer
    if dead: return
    dead=True
    death_timer=0
    particles=[]
    for i in range(20):
        particles.append({"x":player.centerx,"y":player.centery,"vx":random.uniform(-5,5),"vy":random.uniform(-10,-3),"size":random.randint(2,5)})

def update_particles_and_respawn():
    global particles, death_timer, dead
    for p in particles:
        p["x"]+=p["vx"]
        p["y"]+=p["vy"]
        p["vy"]+=0.5
    death_timer+=1
    if death_timer>DEATH_DURATION:
        load_level(current_level)

def draw_player():
    cx, cy = player.centerx, player.bottom
    pygame.draw.circle(screen, (0,0,0), (cx, cy-28), 7)
    pygame.draw.line(screen, (0,0,0), (cx, cy-25), (cx, cy-10), 2)
    if player_state=="walk":
        pygame.draw.line(screen, (0,0,0), (cx, cy-20), (cx-10, cy-12), 2)
        pygame.draw.line(screen, (0,0,0), (cx, cy-20), (cx+10, cy-12), 2)
    else:
        pygame.draw.line(screen, (0,0,0), (cx, cy-20), (cx-7, cy-10), 2)
        pygame.draw.line(screen, (0,0,0), (cx, cy-20), (cx+7, cy-10), 2)
    if not on_ground:
        pygame.draw.line(screen, (0,0,0), (cx, cy-10), (cx-7, cy), 2)
        pygame.draw.line(screen, (0,0,0), (cx, cy-10), (cx+7, cy), 2)
    else:
        pygame.draw.line(screen, (0,0,0), (cx, cy-10), (cx-10, cy), 2)
        pygame.draw.line(screen, (0,0,0), (cx, cy-10), (cx+10, cy), 2)

def draw_torch(tx, ty):
    pygame.draw.rect(screen, (80,50,20), (tx-3, ty, 6, 20))
    flame_y = ty - 10 + random.randint(-2,2)
    flame_size = random.randint(5,8)
    pygame.draw.circle(screen, (255,100,0), (tx, flame_y), flame_size)
    pygame.draw.circle(screen, (255,180,50), (tx, flame_y), max(2, flame_size-2))

def update_saws():
    for saw in active.get("saws", []):
        saw["angle"] += saw.get("speed",0.05)
        cx, cy = saw["center"]
        saw["x"]=cx + math.cos(saw["angle"])*saw["radius"]
        saw["y"]=cy + math.sin(saw["angle"])*saw["radius"]

def draw_saws():
    for saw in active.get("saws", []):
        pygame.draw.circle(screen, (180,180,180), (int(saw["x"]), int(saw["y"])), saw.get("r",20))
        pygame.draw.circle(screen, (100,100,100), (int(saw["x"]), int(saw["y"])), max(3, saw.get("r",20)//4))

# ------------------- START -------------------
load_level(0)
hud_font = pygame.font.SysFont(None, 26)

# ------------------- MAIN LOOP -------------------
while True:
    dt = clock.tick(FPS)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()

    # --- PLAYER MOVEMENT ---
    if not dead:
        dx=0
        if keys[pygame.K_LEFT]:
            dx=-PLAYER_SPEED; player_state="walk"; facing_right=False
        elif keys[pygame.K_RIGHT]:
            dx=PLAYER_SPEED; player_state="walk"; facing_right=True
        else:
            if on_ground: player_state="idle"
        if keys[pygame.K_SPACE] and on_ground:
            player_vel_y = JUMP_STRENGTH; on_ground=False; player_state="jump"

        player.x += dx
        player_vel_y += GRAVITY
        if player_vel_y>25: player_vel_y=25
        player.y += player_vel_y
    else:
        update_particles_and_respawn()

    # --- COLLISIONS ---
    if not dead:
        on_ground=False
        for plat in active.get("platforms",[]):
            if player.colliderect(plat):
                if player_vel_y>=0 and player.bottom-player_vel_y <= plat.top+2:
                    player.bottom=plat.top; player_vel_y=0; on_ground=True
                elif player_vel_y<0 and player.top<plat.bottom:
                    player.top=plat.bottom; player_vel_y=0

        for dsp in active.get("disappearing",[]):
            if dsp.get("active",True) and player.colliderect(dsp["rect"]):
                if player_vel_y>=0 and player.bottom-player_vel_y <= dsp["rect"].top+2:
                    player.bottom=dsp["rect"].top; player_vel_y=0; on_ground=True
                    dsp["timer"]=dsp.get("timer",0)+1
                    if dsp["timer"]>90: dsp["active"]=False

        for fp in active.get("fake",[]):
            if (not fp.get("falling",False)) and player.colliderect(fp["rect"]):
                if player_vel_y>=0 and player.bottom-player_vel_y <= fp["rect"].top+2:
                    fp["falling"]=True
            if fp.get("falling",False):
                fp["vel"]=fp.get("vel",0)+0.35
                fp["rect"].y += fp["vel"]

        for fs in active.get("falling_spikes",[]):
            if not fs.get("falling",False) and abs(player.centerx-fs["rect"].centerx)<80 and player.y<fs["rect"].y+200:
                fs["falling"]=True
            if fs.get("falling",False): fs["rect"].y += 10
            if player.colliderect(fs["rect"]): kill_player()

        for ps in active.get("popup",[]):
            if abs(player.centerx-ps["rect"].centerx)<100: ps["active"]=True
            if ps.get("active",False):
                ps["rect"].y -= 10
                if player.colliderect(ps["rect"]): kill_player()

        for spike in active.get("spikes",[]):
            for x in range(spike.x, spike.x+spike.width, 40):
                spike_hitbox = pygame.Rect(x, spike.y, 40, spike.height)
                if player.colliderect(spike_hitbox): kill_player()

        for h in active.get("holes",[]):
            if player.colliderect(h["rect"]) and player.bottom>=h["rect"].top+5: kill_player()

        # chains (swinging hazard)
        for c in active.get("chains",[]):
            c["swing"]+=c["speed"]
            cx, cy = c["x"], c["y"]
            hx = cx + math.sin(c["swing"])*10
            hy = cy + math.cos(c["swing"])*c["length"]
            chain_rect = pygame.Rect(hx-5, hy-5, 10,10)
            if player.colliderect(chain_rect): kill_player()

        # moving platforms
        for mp in active.get("moving_platforms",[]):
            mp["rect"].x += mp["dir"]
            if abs(mp["rect"].x - mp["start_x"]) > mp["range"]: mp["dir"]*=-1
            if player.colliderect(mp["rect"]):
                if player_vel_y>=0 and player.bottom-player_vel_y <= mp["rect"].top+2:
                    player.bottom=mp["rect"].top; player_vel_y=0; on_ground=True

        # key
        if not active.get("key_collected",False) and player.colliderect(active["key"]):
            active["key_collected"]=True

        # door
        if player.colliderect(active["door"]) and active.get("key_collected",False):
            if current_level<len(level_templates)-1:
                load_level(current_level+1)
            else:
                print("🎉 All levels completed!")
                pygame.quit(); sys.exit()

        # --- NEW: SAW COLLISION FIX ---
        for saw in active.get("saws", []):
            saw_rect = pygame.Rect(int(saw["x"] - saw["r"]), int(saw["y"] - saw["r"]), saw["r"]*2, saw["r"]*2)
            if player.colliderect(saw_rect):
                kill_player()

    update_saws()

    # --- DRAW ---
    screen.fill((60,40,20))
    pygame.draw.rect(screen,(220,200,120),(50,50,WIDTH-100,HEIGHT-100))
    for plat in active.get("platforms",[]): pygame.draw.rect(screen,(150,100,50),plat)
    for dsp in active.get("disappearing",[]): 
        if dsp.get("active",True): pygame.draw.rect(screen,(180,130,70), dsp["rect"])
    for fp in active.get("fake",[]): pygame.draw.rect(screen,(120,80,40),fp["rect"])
    for spike in active.get("spikes",[]):
        for x in range(spike.x, spike.x+spike.width, 40):
            pygame.draw.polygon(screen,(50,30,20),[(x,spike.y+spike.height),(x+20,spike.y),(x+40,spike.y+spike.height)])
    for fs in active.get("falling_spikes",[]):
        pygame.draw.polygon(screen,(50,30,20),[(fs["rect"].x,fs["rect"].y+fs["rect"].height),(fs["rect"].x+fs["rect"].width//2,fs["rect"].y),(fs["rect"].x+fs["rect"].width,fs["rect"].y+fs["rect"].height)])
    for ps in active.get("popup",[]): pygame.draw.rect(screen,(50,30,20), ps["rect"])
    for h in active.get("holes",[]): pygame.draw.rect(screen,(60,40,20),h["rect"])
    for c in active.get("chains",[]):
        cx, cy = c["x"], c["y"]
        hx = cx + math.sin(c["swing"])*10
        hy = cy + math.cos(c["swing"])*c["length"]
        pygame.draw.line(screen,(0,0,0),(cx,cy),(hx,hy),4)
        pygame.draw.circle(screen,(80,0,0),(int(hx),int(hy)),8)
    for mp in active.get("moving_platforms",[]): pygame.draw.rect(screen,(160,110,60), mp["rect"])
    draw_saws()
    for (tx,ty) in active.get("torches", DEFAULT_TORCHES): draw_torch(tx,ty)
    if not active.get("key_collected",False): pygame.draw.rect(screen,(255,215,0), active["key"])
    pygame.draw.rect(screen,(100,70,40), active["door"], border_radius=5)
    pygame.draw.rect(screen,(200,150,50), active["door"],3,border_radius=5)

    if dead:
        for p in particles: pygame.draw.circle(screen,(200,50,50),(int(p["x"]),int(p["y"])),p["size"])
    else:
        draw_player()

    txt = hud_font.render(f"Level {current_level+1}",True,(0,0,0))
    screen.blit(txt,(10,10))

    pygame.display.flip()



