#HAY QUE CAMBIAR COSAS CABRON DENTRO DEL UPDATE

import arcade
from arcade.color import TITANIUM_YELLOW

ANCHO_PANTALLA = 1920
ALTO_PANTALLA = 700
TITULO_PANTALLA= "primer intento" 

ESCALA_PERSONAJE = 1
ESCALA_LOZA = 1
TAMANIO_SPRITE_PIXEL = 128
TAMAÑO_CUADRICULA_PIXEL = TAMANIO_SPRITE_PIXEL*ESCALA_LOZA

#CONSTANTES DE MOVIMIENTO
VELOCIDAD_MOVIMIENTO_JUGADOR = 10
GRAVEDAD = 1
VELOCIDAD_SALTO_JUGADOR = 20

#CONSTANTES DE LOS DISPAROS
ESCALA_SPRITE_DISPARO = 0.8
VELOCIDAD_DISPARO = 15
VELOCIDAD_BALA = 12

#CONSTANTES USADAS PARA SEGUIR SI EL JUGADOR ESTA MIRANDO A LA IZQUIERA O LA DERECHA
MIRAR_DERECHA = 0
MIRAR_IZQUIERDA = 1

#class entidad(arcade.Sprite):
#    def __init__(self):
#
#        super.__init__()
#
#        # direccion donde mira por defecto
#        self.facing_direction = MIRAR_DERECHA
#
#
#
#class llama(entidad):
#
#    def __init__(self):
#
#        super.__init__()
#
#        #seguimiento de que hace
#        self.saltando = False
#        
#        image_source = "C:/Users/cpu/Desktop/Mi_proyecto_pyarcade/pimer_proyecto/recursos/imagenes/zombie.png"
#
#        self.sprite = arcade.Sprite(image_source, ESCALA_PERSONAJE)
#
#
#class enemigos(entidad):
#    def __init__(self):
#        super().__init__()

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

        #variable de movimiento
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shoot_pressed = False
        self.jump_needs_reset = False
        
        #direccion hacia donde mira
        self.padonde_miro = None
        #variables del personaje
        self.player_sprite = None
        #motor de fisicas 
        self.physics_engine = None

        # mecanicas del disparo
        self.can_shoot = False
        self.shoot_timer = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        map_name = "pimer_proyecto/recursos/mapas/Mapa_nivel_1..json"

        layer_options = {
            "piso": {
                "use_spatial_hash": True,
            }
        }

        self.tile_map = arcade.load_tilemap(map_name, ESCALA_LOZA, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #posicion y sprite de mi personaje
        image_source = "pimer_proyecto/recursos/imagenes/zombie.png"
        self.player_sprite = arcade.Sprite(image_source, ESCALA_PERSONAJE)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 144
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVEDAD, walls=self.scene["piso"])

        # mecanicas del disparo
        self.can_shoot = True
        self.shoot_timer = 0

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
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -VELOCIDAD_MOVIMIENTO_JUGADOR
            self.padonde_miro = MIRAR_IZQUIERDA
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = VELOCIDAD_MOVIMIENTO_JUGADOR
            self.padonde_miro = MIRAR_DERECHA
        
        if key == arcade.key.SPACE:
            self.shoot_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

        if key == arcade.key.SPACE:
            self.shoot_pressed = False

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        if  self.player_sprite.change_x  < 0 and self.padonde_miro == MIRAR_DERECHA:
            self.padonde_miro = MIRAR_IZQUIERDA
        elif  self.player_sprite.change_x  > 0 and self.padonde_miro == MIRAR_IZQUIERDA:
            self.padonde_miro = MIRAR_DERECHA
        
        #mecanicas del disparo
        #
        if self.can_shoot:
             if self.shoot_pressed:
                bullet = arcade.Sprite(
                    ":resources:images/space_shooter/laserBlue01.png",
                    ESCALA_SPRITE_DISPARO,
                )
                
                #HAY QUE CAMBIAR ESTO CABROON
                if self.padonde_miro == MIRAR_DERECHA:
                    bullet.change_x = VELOCIDAD_BALA
                else:
                    bullet.change_x = -VELOCIDAD_BALA

                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y
                #HAY QUE CAMBIAR ESTO CABRON
                self.scene.add_sprite("BALAS", bullet)

                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == VELOCIDAD_DISPARO:
                self.can_shoot = True
                self.shoot_timer = 0


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()