import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Definición de dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idle Tycoon Empire")

# Clase para representar un negocio
class Business:
    def __init__(self, name, base_revenue, upgrade_cost):
        self.name = name
        self.base_revenue = base_revenue
        self.upgrade_cost = upgrade_cost
        self.level = 1
        self.upgrade_level = 1
        self.revenue = base_revenue * self.level

    def upgrade(self):
        if self.upgrade_level < 5:  # Máximo nivel de mejora
            self.level += 1
            self.upgrade_level += 1
            self.revenue = self.base_revenue * self.level
            self.upgrade_cost *= 1.5  # Aumentar costo de mejora

# Función para dibujar texto en la pantalla
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Función principal del juego
def main():
    clock = pygame.time.Clock()

    # Inicialización de variables del juego
    money = 0
    businesses = [
        Business("Lemonade Stand", 1, 10),
        # Agrega más negocios aquí
    ]
    income_timer = pygame.time.get_ticks()
    selected_upgrade = None

    # Bucle principal del juego
    while True:
        SCREEN.fill(WHITE)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Manejar clics en los botones de mejora
                if 50 <= event.pos[0] <= 250:
                    button_index = (event.pos[1] - 100) // 60
                    if 0 <= button_index < len(businesses):
                        selected_upgrade = button_index

                # Manejar clics en el botón de compra
                if 350 <= event.pos[0] <= 450 and 500 <= event.pos[1] <= 550:
                    if selected_upgrade is not None:
                        selected_business = businesses[selected_upgrade]
                        if money >= selected_business.upgrade_cost:
                            money -= selected_business.upgrade_cost
                            selected_business.upgrade()
                            selected_upgrade = None

        # Lógica del juego
        current_time = pygame.time.get_ticks()
        if current_time - income_timer >= 1000:  # Generar ingresos cada segundo
            total_revenue = sum(business.revenue for business in businesses)
            money += total_revenue
            income_timer = current_time

        # Dibujar interfaz de usuario
        draw_text("Money: $" + str(money), pygame.font.Font(None, 36), BLACK, SCREEN, 100, 50)
        for i, business in enumerate(businesses):
            draw_text(
                f"{business.name}: Level {business.level} - Revenue: ${business.revenue}",
                pygame.font.Font(None, 24),
                BLACK,
                SCREEN,
                100,
                100 + i * 60,
            )
            draw_text(
                f"Upgrade Cost: ${business.upgrade_cost}",
                pygame.font.Font(None, 18),
                BLACK,
                SCREEN,
                100,
                120 + i * 60,
            )

        # Dibujar botones de mejora
        for i, upgrade in enumerate(["Espada", "Pico", "Hacha", "Arco"]):
            pygame.draw.rect(SCREEN, GRAY, (50, 100 + i * 60, 200, 50))
            draw_text(upgrade, pygame.font.Font(None, 24), BLACK, SCREEN, 150, 125 + i * 60)

        # Dibujar botón de compra
        pygame.draw.rect(SCREEN, GRAY, (350, 500, 100, 50))
        draw_text("Comprar", pygame.font.Font(None, 24), BLACK, SCREEN, 400, 525)

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
