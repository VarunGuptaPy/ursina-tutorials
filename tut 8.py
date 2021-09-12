'''
1. Being able to destroy trees
2. To improve the terrain generation
3. costomize our mob
4. Add depth
'''
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from perlin_noise import PerlinNoise
from random import *
from blocks import BTYPE
from Trees import Trees
app = Ursina()
life = Trees()
player = FirstPersonController()
player.y = 20
player.gravity = 0.2
player.cursor.visible = False
window.exit_button.visible = False
Grass = 'grassCube.png'
GrassModel = 'GrassCube.obj'
Zombie = 'zombie.png'
frameTex = 'Frame'

Btype = BTYPE.Grass

frame = Entity(model='cube', texture=frameTex)

def input(key):
	if key == 'escape':
		quit()
	if key == 'right mouse up':
		global Btype
		e = duplicate(frame)
		e.collider = 'mesh'
		e.model = GrassModel
		e.texture = Btype
	if key == '1':
		Btype = BTYPE.Brick
	if key == '0':
		Btype = BTYPE.Grass
	if key == '2':
		Btype = BTYPE.Sand
	if key == '3':
		Btype = BTYPE.Log

def genTrees(_x, _z, plantTree=True):
    y = 1
    freq = 32
    amp = 21
    y += ((noise([_x/freq,_z/freq]))*amp)
    if plantTree==True:
        life.checkTree(_x,y,_z)


def update():
	if player.y < -3:
		player.y = 10

	frame.position = floor(player.position + camera.forward * 4)
	frame.y = frame.y + 2
	zombie1.look_at(player, 'forward')
	zombie1.rotation_x = 0
	genTrees(randrange(-100, 100), randrange(-100, 100))
	genTerr()

noise = PerlinNoise(octaves=2,seed=randrange(1, 100000000000000000000000000000000000))
amp = 6
freq = 24

shells = []
shellWidth = 12
for i in range(shellWidth*shellWidth):
    ent = Entity(model=GrassModel, texture=Grass, collider='box')
    shells.append(ent)

def genTerr():
	global amp, freq
	for i in range(len(shells)):
		x = shells[i].x = floor((i/shellWidth) + player.x - 0.5*shellWidth)
		z = shells[i].z = floor((i%shellWidth) + player.z - 0.5*shellWidth)
		y = shells[i].y = floor(noise([x/freq, z/freq])*amp)

ZombieModel = load_model('AnyConv.com__zombie (1).obj')
zombie1 = Entity(model=ZombieModel, texture=Zombie, scale=0.07, double_sided=True, y=1,)
app.run()