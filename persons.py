import pygame

SCREEN = WIDTH, HEIGHT = (600, 200)

class Road():
	def __init__(self):
		self.image = pygame.image.load('images/ground.png')
		self.rect = self.image.get_rect()

		self.width = self.image.get_width()
		self.x1 = 0
		self.x2 = self.width
		self.y = 150

	def update(self, speed):
		self.x1 -= speed
		self.x2 -= speed

		if self.x1 <= -self.width:
			self.x1 = self.width

		if self.x2 <= -self.width:
			self.x2 = self.width

	def draw(self, win):
		win.blit(self.image, (self.x1, self.y))
		win.blit(self.image, (self.x2, self.y))


class Lula():
	def __init__(self, x, y):
		self.x, self.base = x, y

		self.run_list = []
		self.crouching_list = []

		for i in range(1, 4):
			img = pygame.image.load(f'images/lula/{i}.png')
			img = pygame.transform.scale(img, (80,87))
			self.run_list.append(img)

		for i in range(4, 6):
			img = pygame.image.load(f'images/lula/{i}.png')
			img = pygame.transform.scale(img, (80,84))
			self.crouching_list.append(img)

		self.dead_image = pygame.image.load(f'images/lula/8.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (65,72))

		self.reset()

		self.vel = 0
		self.gravity = 0.65
		self.jump_height = 15
		self.is_jumping = False

	def reset(self):
		self.index = 0
		self.image = self.run_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.bottom = self.base

		self.alive = True
		self.counter = 0

	def update(self, jump, crouching):
		if self.alive:
			if not self.is_jumping and jump:
				self.vel = -self.jump_height
				self.is_jumping = True

			self.vel += self.gravity
			if self.vel >= self.jump_height:
				self.vel = self.jump_height

			self.rect.y += self.vel
			if self.rect.bottom > self.base:
				self.rect.bottom = self.base
				self.is_jumping = False

			if crouching:
				self.counter += 1
				if self.counter >= 6:
					self.index = (self.index + 1) % len(self.crouching_list)
					self.image = self.crouching_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = self.base
					self.counter = 0

			elif self.is_jumping:
				self.index = 0
				self.counter = 0
				self.image = self.run_list[self.index]
			else:
				self.counter += 1
				if self.counter >= 4:
					self.index = (self.index + 1) % len(self.run_list)
					self.image = self.run_list[self.index]
					self.rect = self.image.get_rect()
					self.rect.x = self.x
					self.rect.bottom = self.base
					self.counter = 0

			self.mask = pygame.mask.from_surface(self.image)

		else:
			self.image = self.dead_image

	def draw(self, win):
		win.blit(self.image, self.rect)

class Trucks(pygame.sprite.Sprite):
	def __init__(self, rand):
		super(Trucks, self).__init__()

		self.image_list = []
		for i in range(3):
			scale = 1.3
			img = pygame.image.load(f'images/caminhoes/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.image = self.image_list[rand-1]
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH + 10
		self.rect.bottom = 165

	def update(self, speed, lula):
		if lula.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)

class Gaudy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Gaudy, self).__init__()

		self.image_list = []
		for i in range(2):
			scale = 0.65
			img = pygame.image.load(f'images/berrante/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.index = 0
		self.image = self.image_list[self.index]
		self.rect = self.image.get_rect(center=(x, y))

		self.counter = 0

	def update(self, speed, lula):
		if lula.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.counter += 1
			if self.counter >= 6:
				self.index = (self.index + 1) % len(self.image_list)
				self.image = self.image_list[self.index]
				self.counter = 0

			self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)


class Cloud(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Cloud, self).__init__()
		self.image = pygame.image.load(f'images/cloud.png')
		self.image = pygame.transform.scale(self.image, (60, 18))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, speed, lula):
		if lula.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

	def draw(self, win):
		win.blit(self.image, self.rect)
