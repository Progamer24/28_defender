import math
import random
import pygame

VIEW_W, VIEW_H = 800, 560
WORLD_W = 3200
RADAR_H = 56
PLAY_TOP = RADAR_H + 6
HUMANOID_COUNT = 6
FALL_LIMIT = 160
PHASES = [random.uniform(0, math.tau) for _ in range(3)]


def sky_color(wave):
<<<<<<< HEAD
    """Return an (r, g, b) sky colour for the current wave, or None for the default."""
    pass


def on_humanoid_rescued(humanoid):
    """Called when the player catches a falling humanoid; add a bonus or celebration here."""
    pass


def bonus_life_threshold():
    """Return a score value at which the player earns an extra life, or None to disable bonus lives."""
    pass
=======
    """Return a wave-dependent sky colour."""
    # Keep the early game dark, then gradually introduce a blue/violet tint.
    # The values are deliberately capped so the playfield remains readable.
    w = max(1, int(wave))
    intensity = min(24, 4 + (w - 1) * 2)
    blue = min(38, 20 + (w - 1) * 2)
    red = min(14, 5 + (w // 6))
    green = min(12, 5 + (w // 8))
    return red, green + intensity // 3, blue


def on_humanoid_rescued(humanoid):
    """Give a rescued humanoid a short-lived +500 celebration popup."""
    # The hook intentionally does not depend on a Game instance.  draw()
    # reads these temporary attributes from the rescued humanoid.
    humanoid.rescue_popup = 0.9
    humanoid.rescue_text = "+500"


def bonus_life_threshold():
    """Award one extra life every 10,000 points."""
    return 10000
>>>>>>> 802c1e2 (Tasks Completed)


def wrap_delta(a, b):
    """Shortest signed distance from world x=a to world x=b on a wrapping world."""
    return (b - a + WORLD_W / 2) % WORLD_W - WORLD_W / 2


def ground_y(x):
    angle = math.tau * x / WORLD_W
<<<<<<< HEAD
    return 505 - 25 * math.sin(3 * angle + PHASES[0]) - 14 * math.sin(7 * angle + PHASES[1]) - 6 * math.sin(13 * angle + PHASES[2])
=======
    return (
        505
        - 25 * math.sin(3 * angle + PHASES[0])
        - 14 * math.sin(7 * angle + PHASES[1])
        - 6 * math.sin(13 * angle + PHASES[2])
    )
>>>>>>> 802c1e2 (Tasks Completed)


class Humanoid:
    def __init__(self, x):
<<<<<<< HEAD
        self.x, self.y = x, ground_y(x) - 8
        self.state = "ground"
        self.fall_from = self.y
        self.vy = 0.0

    def update(self, dt):
=======
        self.x = x % WORLD_W
        self.y = ground_y(self.x) - 8
        self.state = "ground"
        self.fall_from = self.y
        self.vy = 0.0
        self.rescue_popup = 0.0
        self.rescue_text = ""

    def update(self, dt):
        if self.rescue_popup > 0:
            self.rescue_popup = max(0.0, self.rescue_popup - dt)

>>>>>>> 802c1e2 (Tasks Completed)
        if self.state == "falling":
            self.vy += 300 * dt
            self.y += self.vy * dt
            floor = ground_y(self.x) - 8
            if self.y >= floor:
                self.y = floor
                self.vy = 0
                self.state = "dead" if floor - self.fall_from > FALL_LIMIT else "ground"


class Lander:
    def __init__(self, x):
<<<<<<< HEAD
        self.x, self.y = x, PLAY_TOP + 20
=======
        self.x = x % WORLD_W
        self.y = PLAY_TOP + 20
>>>>>>> 802c1e2 (Tasks Completed)
        self.target = None
        self.mutant = False

    def pick_target(self, humanoids, landers):
<<<<<<< HEAD
        free = [h for h in humanoids if h.state == "ground" and not any(h is l.target for l in landers)]
=======
        free = [
            h
            for h in humanoids
            if h.state == "ground"
            and not any(h is l.target for l in landers if l is not self)
        ]
>>>>>>> 802c1e2 (Tasks Completed)
        self.target = random.choice(free) if free else None

    def update(self, dt, player, humanoids, landers, wave):
        if self.mutant:
            dx = wrap_delta(self.x, player.x)
            dy = player.y - self.y
<<<<<<< HEAD
            dist = math.hypot(dx, dy) or 1
            speed = 110 + wave * 10
            self.x = (self.x + dx / dist * speed * dt + random.uniform(-40, 40) * dt) % WORLD_W
            self.y += dy / dist * speed * dt
            return
        if self.target is None or self.target.state not in ("ground", "carried"):
            self.target = None
            self.pick_target(humanoids, landers)
        target = self.target
        if target is None:
            dx, dy = wrap_delta(self.x, player.x), player.y - self.y
            dist = math.hypot(dx, dy) or 1
            self.x = (self.x + dx / dist * 60 * dt) % WORLD_W
            self.y += dy / dist * 60 * dt
        elif target.state == "carried":
            self.y -= 45 * dt
            target.x, target.y = self.x, self.y + 20
            if self.y <= PLAY_TOP + 8:
                humanoids.remove(target)
                self.target, self.mutant = None, True
        else:
            dx, dy = wrap_delta(self.x, target.x), target.y - 18 - self.y
            dist = math.hypot(dx, dy)
            if dist < 6:
                target.state = "carried"
            else:
                self.x = (self.x + dx / dist * 70 * dt) % WORLD_W
                self.y += dy / dist * 70 * dt
=======
            dist = math.hypot(dx, dy) or 1.0
            speed = 110 + wave * 10
            self.x = (
                self.x
                + dx / dist * speed * dt
                + random.uniform(-40, 40) * dt
            ) % WORLD_W
            self.y += dy / dist * speed * dt
            self.y = max(PLAY_TOP + 8, min(VIEW_H - 24, self.y))
            return

        if self.target is None or self.target.state not in ("ground", "carried"):
            self.target = None
            self.pick_target(humanoids, landers)

        target = self.target

        if target is None:
            dx = wrap_delta(self.x, player.x)
            dy = player.y - self.y
            dist = math.hypot(dx, dy) or 1.0
            speed = 60 + min(45, wave * 3)
            self.x = (self.x + dx / dist * speed * dt) % WORLD_W
            self.y += dy / dist * speed * dt
        elif target.state == "carried":
            self.y -= (45 + wave * 2) * dt
            target.x, target.y = self.x, self.y + 20
            if self.y <= PLAY_TOP + 8:
                if target in humanoids:
                    humanoids.remove(target)
                self.target = None
                self.mutant = True
        else:
            dx = wrap_delta(self.x, target.x)
            dy = target.y - 18 - self.y
            dist = math.hypot(dx, dy)
            if dist < 6:
                target.state = "carried"
            elif dist > 0:
                speed = 70 + min(35, wave * 2)
                self.x = (self.x + dx / dist * speed * dt) % WORLD_W
                self.y += dy / dist * speed * dt
>>>>>>> 802c1e2 (Tasks Completed)


class Player:
    def __init__(self):
<<<<<<< HEAD
        self.x, self.y, self.vx, self.facing = WORLD_W / 2, 250.0, 0.0, 1
        self.invulnerable, self.cooldown = 1.5, 0.0
=======
        self.x = WORLD_W / 2
        self.y = 250.0
        self.vx = 0.0
        self.facing = 1
        self.invulnerable = 1.5
        self.cooldown = 0.0
>>>>>>> 802c1e2 (Tasks Completed)

    def update(self, dt, keys):
        thrust = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        if thrust:
            self.facing = thrust
<<<<<<< HEAD
        self.vx = max(-520, min(520, self.vx + thrust * 900 * dt))
        self.vx *= 1 - min(1.0, 0.8 * dt)
        self.x = (self.x + self.vx * dt) % WORLD_W
        self.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 260 * dt
        self.y = max(PLAY_TOP + 10, min(VIEW_H - 30, self.y))
        self.invulnerable = max(0.0, self.invulnerable - dt)
        self.cooldown -= dt
=======

        self.vx = max(-520, min(520, self.vx + thrust * 900 * dt))
        self.vx *= 1 - min(1.0, 0.8 * dt)
        self.x = (self.x + self.vx * dt) % WORLD_W

        self.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 260 * dt
        self.y = max(PLAY_TOP + 10, min(VIEW_H - 30, self.y))

        self.invulnerable = max(0.0, self.invulnerable - dt)
        self.cooldown = max(0.0, self.cooldown - dt)
>>>>>>> 802c1e2 (Tasks Completed)


class Game:
    def __init__(self):
        self.font = pygame.font.Font(None, 26)
<<<<<<< HEAD
=======
        self.small_font = pygame.font.Font(None, 22)
        self.big_font = pygame.font.Font(None, 34)
>>>>>>> 802c1e2 (Tasks Completed)
        self.reset()

    def reset(self):
        self.player = Player()
<<<<<<< HEAD
        self.humanoids = [Humanoid(i * WORLD_W / HUMANOID_COUNT + 100) for i in range(HUMANOID_COUNT)]
        self.landers, self.bullets = [], []
        self.score, self.lives, self.wave, self.state = 0, 3, 1, "play"
        self.bonus_awarded = 0
        self.start_wave()

    def start_wave(self):
        self.to_spawn = 3 + self.wave * 2
        self.spawn_timer = 1.0
=======
        self.humanoids = [
            Humanoid(i * WORLD_W / HUMANOID_COUNT + 100)
            for i in range(HUMANOID_COUNT)
        ]
        self.landers = []
        self.bullets = []
        self.score = 0
        self.lives = 3
        self.wave = 1
        self.state = "play"
        self.bonus_awarded = 0
        self.wave_banner = 1.5
        self.start_wave()

    def start_wave(self):
        # More landers each wave, with a reasonable cap to prevent runaway
        # object counts in long games.
        self.to_spawn = min(18, 3 + self.wave * 2)
        self.spawn_timer = 0.7
        self.wave_banner = 1.5

>>>>>>> 802c1e2 (Tasks Completed)
        while len(self.humanoids) < HUMANOID_COUNT:
            self.humanoids.append(Humanoid(random.uniform(0, WORLD_W)))

    def shoot_lander(self, lander):
<<<<<<< HEAD
        self.landers.remove(lander)
        if lander.target is not None and lander.target.state == "carried":
            lander.target.state = "falling"
            lander.target.fall_from = lander.target.y
        self.score += 150
=======
        if lander not in self.landers:
            return

        self.landers.remove(lander)

        if lander.target is not None and lander.target.state == "carried":
            lander.target.state = "falling"
            lander.target.fall_from = lander.target.y
            lander.target.vy = 40

        # Mutants are worth more than normal landers.
        self.score += 300 if lander.mutant else 150
>>>>>>> 802c1e2 (Tasks Completed)

    def update(self, dt, keys):
        if self.state != "play":
            return
<<<<<<< HEAD
        player = self.player
        player.update(dt, keys)
        threshold = bonus_life_threshold()
        if threshold and self.score // threshold > self.bonus_awarded:
            self.bonus_awarded = self.score // threshold
            self.lives += 1
        if keys[pygame.K_SPACE] and player.cooldown <= 0:
            player.cooldown = 0.18
            self.bullets.append({"x": player.x + player.facing * 20, "y": player.y, "dir": player.facing, "life": 0.7})
        self.spawn_timer -= dt
        if self.to_spawn > 0 and self.spawn_timer <= 0:
            self.landers.append(Lander(random.uniform(0, WORLD_W)))
            self.to_spawn -= 1
            self.spawn_timer = 1.5
        for lander in self.landers:
            lander.update(dt, player, self.humanoids, self.landers, self.wave)
        for humanoid in self.humanoids[:]:
            humanoid.update(dt)
            if humanoid.state == "dead":
                self.humanoids.remove(humanoid)
            elif humanoid.state == "falling" and abs(wrap_delta(player.x, humanoid.x)) < 24 and abs(humanoid.y - player.y) < 24:
                humanoid.state, humanoid.y = "ground", ground_y(humanoid.x) - 8
                self.score += 500
                on_humanoid_rescued(humanoid)
        self.update_bullets(dt)
        if player.invulnerable <= 0:
            for lander in self.landers:
                if abs(wrap_delta(player.x, lander.x)) < 22 and abs(lander.y - player.y) < 18:
                    self.lives -= 1
                    self.player = Player()
                    if self.lives <= 0:
                        self.state = "lose"
                    break
=======

        player = self.player
        player.update(dt, keys)

        if self.wave_banner > 0:
            self.wave_banner = max(0.0, self.wave_banner - dt)

        threshold = bonus_life_threshold()
        if threshold and threshold > 0:
            earned = self.score // threshold
            if earned > self.bonus_awarded:
                self.lives += earned - self.bonus_awarded
                self.bonus_awarded = earned

        if keys[pygame.K_SPACE] and player.cooldown <= 0:
            player.cooldown = 0.18
            self.bullets.append(
                {
                    "x": (player.x + player.facing * 20) % WORLD_W,
                    "y": player.y,
                    "dir": player.facing,
                    "life": 0.7,
                }
            )

        self.spawn_timer -= dt
        if self.to_spawn > 0 and self.spawn_timer <= 0:
            # Spawn away from the player when possible so new enemies do not
            # appear directly on top of the ship.
            spawn_x = random.uniform(0, WORLD_W)
            for _ in range(10):
                if abs(wrap_delta(player.x, spawn_x)) > VIEW_W * 0.45:
                    break
                spawn_x = random.uniform(0, WORLD_W)

            self.landers.append(Lander(spawn_x))
            self.to_spawn -= 1
            self.spawn_timer = max(0.55, 1.5 - self.wave * 0.025)

        for lander in self.landers[:]:
            lander.update(dt, player, self.humanoids, self.landers, self.wave)

        for humanoid in self.humanoids[:]:
            humanoid.update(dt)

            if humanoid.state == "dead":
                self.humanoids.remove(humanoid)
                continue

            if (
                humanoid.state == "falling"
                and abs(wrap_delta(player.x, humanoid.x)) < 24
                and abs(humanoid.y - player.y) < 24
            ):
                humanoid.state = "ground"
                humanoid.y = ground_y(humanoid.x) - 8
                humanoid.vy = 0
                self.score += 500
                on_humanoid_rescued(humanoid)

        self.update_bullets(dt)

        if player.invulnerable <= 0:
            for lander in self.landers:
                if (
                    abs(wrap_delta(player.x, lander.x)) < 22
                    and abs(lander.y - player.y) < 18
                ):
                    self.lives -= 1

                    if self.lives <= 0:
                        self.state = "lose"
                    else:
                        self.player = Player()
                    break

>>>>>>> 802c1e2 (Tasks Completed)
        if self.to_spawn == 0 and not self.landers:
            self.wave += 1
            self.start_wave()

    def update_bullets(self, dt):
        for bullet in self.bullets:
<<<<<<< HEAD
            bullet["x"] = (bullet["x"] + bullet["dir"] * 900 * dt) % WORLD_W
            bullet["life"] -= dt
            for lander in self.landers[:]:
                if abs(wrap_delta(bullet["x"], lander.x)) < 16 and abs(bullet["y"] - lander.y) < 12:
                    self.shoot_lander(lander)
                    bullet["life"] = 0
                    break
        self.bullets = [b for b in self.bullets if b["life"] > 0]

    def screen_x(self, x):
        return VIEW_W / 2 + wrap_delta(self.player.x, x)

    def draw_radar(self, screen):
        pygame.draw.rect(screen, (10, 10, 30), (0, 0, VIEW_W, RADAR_H))
        pygame.draw.rect(screen, (90, 90, 140), (0, 0, VIEW_W, RADAR_H), 1)
        blips = [(h.x, h.y, (90, 230, 120)) for h in self.humanoids]
        blips += [(l.x, l.y, (255, 90, 90) if l.mutant else (230, 200, 60)) for l in self.landers]
        blips.append((self.player.x, self.player.y, (255, 255, 255)))
        for x, y, color in blips:
            rx = self.screen_x(x) % VIEW_W
            ry = (y - PLAY_TOP) / (VIEW_H - PLAY_TOP) * (RADAR_H - 8) + 4
=======
            bullet["x"] = (
                bullet["x"] + bullet["dir"] * 900 * dt
            ) % WORLD_W
            bullet["life"] -= dt

            for lander in self.landers[:]:
                if (
                    abs(wrap_delta(bullet["x"], lander.x)) < 16
                    and abs(bullet["y"] - lander.y) < 12
                ):
                    self.shoot_lander(lander)
                    bullet["life"] = 0
                    break

        self.bullets = [b for b in self.bullets if b["life"] > 0]

    def screen_x(self, x):
        """Convert world x to player-relative viewport x."""
        return VIEW_W / 2 + wrap_delta(self.player.x, x)

    def draw_radar(self, screen):
        """Draw the complete wrapping world, not the player-relative viewport."""
        pygame.draw.rect(screen, (10, 10, 30), (0, 0, VIEW_W, RADAR_H))
        pygame.draw.rect(screen, (90, 90, 140), (0, 0, VIEW_W, RADAR_H), 1)

        # IMPORTANT: radar_x is based directly on absolute world x.
        # Do not use screen_x(), because that is intentionally camera-relative.
        def radar_x(world_x):
            return (world_x % WORLD_W) / WORLD_W * VIEW_W

        blips = [
            (h.x, h.y, (90, 230, 120))
            for h in self.humanoids
        ]
        blips += [
            (l.x, l.y, (255, 90, 90) if l.mutant else (230, 200, 60))
            for l in self.landers
        ]
        blips.append((self.player.x, self.player.y, (255, 255, 255)))

        for x, y, color in blips:
            rx = radar_x(x)
            ry = (
                (y - PLAY_TOP) / (VIEW_H - PLAY_TOP)
                * (RADAR_H - 8)
                + 4
            )
            ry = max(4, min(RADAR_H - 4, ry))
>>>>>>> 802c1e2 (Tasks Completed)
            pygame.draw.rect(screen, color, (rx - 2, ry - 2, 4, 4))

    def draw(self, screen):
        screen.fill(sky_color(self.wave) or (5, 5, 20))
<<<<<<< HEAD
        points = [(sx, ground_y(self.player.x + sx - VIEW_W / 2)) for sx in range(0, VIEW_W + 8, 8)]
        pygame.draw.polygon(screen, (110, 70, 40), points + [(VIEW_W, VIEW_H), (0, VIEW_H)])
        pygame.draw.lines(screen, (230, 150, 60), False, points, 2)
        for humanoid in self.humanoids:
            sx = self.screen_x(humanoid.x)
            if -20 < sx < VIEW_W + 20:
                pygame.draw.rect(screen, (90, 230, 120), (sx - 3, humanoid.y - 10, 6, 14))
=======

        # Draw terrain in world coordinates, sampled around the camera.
        points = [
            (
                sx,
                ground_y(
                    (self.player.x + sx - VIEW_W / 2) % WORLD_W
                ),
            )
            for sx in range(0, VIEW_W + 8, 8)
        ]
        pygame.draw.polygon(
            screen,
            (110, 70, 40),
            points + [(VIEW_W, VIEW_H), (0, VIEW_H)],
        )
        pygame.draw.lines(
            screen,
            (230, 150, 60),
            False,
            points,
            2,
        )

        for humanoid in self.humanoids:
            sx = self.screen_x(humanoid.x)
            if -20 < sx < VIEW_W + 20:
                pygame.draw.rect(
                    screen,
                    (90, 230, 120),
                    (sx - 3, humanoid.y - 10, 6, 14),
                )

                if humanoid.rescue_popup > 0:
                    alpha = min(255, int(255 * humanoid.rescue_popup / 0.9))
                    popup = self.small_font.render(
                        humanoid.rescue_text or "+500",
                        True,
                        (255, 255, 120),
                    )
                    popup.set_alpha(alpha)
                    screen.blit(
                        popup,
                        (sx + 8, humanoid.y - 28 - int((0.9 - humanoid.rescue_popup) * 20)),
                    )

>>>>>>> 802c1e2 (Tasks Completed)
        for lander in self.landers:
            sx = self.screen_x(lander.x)
            if -20 < sx < VIEW_W + 20:
                color = (255, 90, 90) if lander.mutant else (230, 200, 60)
<<<<<<< HEAD
                pygame.draw.ellipse(screen, color, (sx - 14, lander.y - 9, 28, 18))
        for bullet in self.bullets:
            sx = self.screen_x(bullet["x"])
            pygame.draw.line(screen, (255, 255, 200), (sx - 8, bullet["y"]), (sx + 8, bullet["y"]), 2)
        player = self.player
        if player.invulnerable <= 0 or int(player.invulnerable * 10) % 2 == 0:
            f, cx = player.facing, VIEW_W / 2
            pygame.draw.polygon(screen, (240, 240, 250), [(cx + f * 18, player.y), (cx - f * 14, player.y - 8), (cx - f * 14, player.y + 8)])
        self.draw_radar(screen)
        hud = self.font.render(f"Score {self.score}  Lives {self.lives}  Wave {self.wave}  Humanoids {len(self.humanoids)}", True, (240, 240, 240))
        screen.blit(hud, (10, RADAR_H + 4))
        if self.state == "lose":
            label = self.font.render("GAME OVER - Press R", True, (255, 255, 120))
            screen.blit(label, label.get_rect(center=(VIEW_W // 2, VIEW_H // 2)))
=======
                pygame.draw.ellipse(
                    screen,
                    color,
                    (sx - 14, lander.y - 9, 28, 18),
                )

                if lander.mutant:
                    pygame.draw.line(
                        screen,
                        (255, 180, 180),
                        (sx - 10, lander.y),
                        (sx + 10, lander.y),
                        2,
                    )

        for bullet in self.bullets:
            sx = self.screen_x(bullet["x"])
            if -20 < sx < VIEW_W + 20:
                pygame.draw.line(
                    screen,
                    (255, 255, 200),
                    (sx - 8, bullet["y"]),
                    (sx + 8, bullet["y"]),
                    2,
                )

        player = self.player
        if player.invulnerable <= 0 or int(player.invulnerable * 10) % 2 == 0:
            f, cx = player.facing, VIEW_W / 2
            pygame.draw.polygon(
                screen,
                (240, 240, 250),
                [
                    (cx + f * 18, player.y),
                    (cx - f * 14, player.y - 8),
                    (cx - f * 14, player.y + 8),
                ],
            )

        self.draw_radar(screen)

        hud = self.font.render(
            f"Score {self.score}  Lives {self.lives}  "
            f"Wave {self.wave}  Humanoids {len(self.humanoids)}",
            True,
            (240, 240, 240),
        )
        screen.blit(hud, (10, RADAR_H + 4))

        if self.wave_banner > 0 and self.state == "play":
            label = self.big_font.render(
                f"WAVE {self.wave}",
                True,
                (255, 230, 120),
            )
            label.set_alpha(min(255, int(255 * self.wave_banner / 1.5)))
            screen.blit(
                label,
                label.get_rect(center=(VIEW_W // 2, 95)),
            )

        if self.state == "lose":
            label = self.font.render(
                "GAME OVER - Press R",
                True,
                (255, 255, 120),
            )
            screen.blit(
                label,
                label.get_rect(center=(VIEW_W // 2, VIEW_H // 2)),
            )
>>>>>>> 802c1e2 (Tasks Completed)


def main():
    pygame.init()
    screen = pygame.display.set_mode((VIEW_W, VIEW_H))
    pygame.display.set_caption("Defender")
    clock = pygame.time.Clock()
    game = Game()
    running = True
<<<<<<< HEAD
    while running:
        dt = min(clock.tick(60) / 1000, 0.05)
=======

    while running:
        dt = min(clock.tick(60) / 1000, 0.05)

>>>>>>> 802c1e2 (Tasks Completed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()
<<<<<<< HEAD
        game.update(dt, pygame.key.get_pressed())
        game.draw(screen)
        pygame.display.flip()
=======

        game.update(dt, pygame.key.get_pressed())
        game.draw(screen)
        pygame.display.flip()

>>>>>>> 802c1e2 (Tasks Completed)
    pygame.quit()


if __name__ == "__main__":
    main()
