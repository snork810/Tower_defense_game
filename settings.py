class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.rows = 10
        self.cols = 15
        self.grid_size = (64, 64)

        self.tower_cost = 100
        self.tower_upgrade_cost = 150
        self.tower_sell_percentage = 0.75

        self.enemy_path = [
            (50, 400), (300, 400), (300, 200), (600, 200),
            (600, 600), (900, 600), (900, 300), (1150, 300)
        ]

        self.tower_sprites = {
            'basic': 'tower_defence/assets/towers/basic_tower.png',
            'sniper': 'tower_defence/assets/towers/sniper_tower.png',
            'money': 'tower_defence/assets/towers/money_tower.png'
        }
        self.enemy_sprite = 'tower_defence/assets/enemies/basic_enemy.png'
        self.bullet_sprite = 'tower_defence/assets/bullets/basic_bullet.png'
        self.background_image = 'tower_defence/assets/backgrounds/game_background.png'

        self.shoot_sound = 'tower_defence/assets/sounds/shoot.wav'
        self.new_wave_sound = 'tower_defence/assets/sounds/new_wave.wav'
        self.upgrade_sound = 'tower_defence/assets/sounds/upgrade.wav'
        self.sell_sound = 'tower_defence/assets/sounds/sell.wav'
        self.enemy_hit_sound = 'tower_defence/assets/sounds/enemy_hit.wav'
        self.background_music = 'tower_defence/assets/sounds/background_music.mp3'

        self.starting_money = 500
        self.lives = 20

        self.tower_positions = [
            (x * self.grid_size[0] + self.grid_size[0] // 2, y * self.grid_size[1] + self.grid_size[1] // 2)
            for x in range(1, self.cols) for y in range(3, self.rows)]
