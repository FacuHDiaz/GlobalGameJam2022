import arcade
from arcade.color import TITANIUM_YELLOW

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
TITULO_PANTALLA= "primer intento" 

ESCALA_PERSONAJE = 1
ESCALA_LOZA = 1
TAMANIO_SPRITE_PIXEL = 128
TAMAÑO_CUADRICULA_PIXEL = TAMANIO_SPRITE_PIXEL*ESCALA_LOZA

#CONSTANTES DE MOVIMIENTO
VELOCIDAD_MOVIMIENTO_JUGADOR = 10
GRAVEDAD = 1
VELOCIDAD_SALTO_JUGADOR = 20

class entidad(arcade.Sprite):
    def __init__(self):
        super.__init__()


class llama(entidad):
    def __init__(self):
        super.__init__()

class enemigos(entidad):
    def __init__(self):
        super().__init__()

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO_PANTALLA)
        
        #variables del mapa
        self.tile_map = None
        self.scene = None

        #variables del personaje
        self.player_sprite = None

        #motor de fisicas 
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        map_name = "C:/Users/cpu/Desktop/Mi_proyecto_pyarcade/pimer_proyecto/recursos/mapas/Mapa_nivel_1.json"

        layer_options = {
            "piso": {
                "use_spatial_hash": True,
            }
        }

        self.tile_map = arcade.load_tilemap(map_name, ESCALA_LOZA, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        image_source = "C:/Users/cpu/Desktop/Mi_proyecto_pyarcade/pimer_proyecto/recursos/imagenes/zombie.png"
        self.player_sprite = arcade.Sprite(image_source, ESCALA_PERSONAJE)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 144
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVEDAD, walls=self.scene["piso"])

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

    def on_draw(self):
        """Render the screen."""

        arcade.start_render()
        # Code to draw the screen goes here

        self.scene.draw()
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = VELOCIDAD_SALTO_JUGADOR
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -VELOCIDAD_MOVIMIENTO_JUGADOR
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = VELOCIDAD_MOVIMIENTO_JUGADOR

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()