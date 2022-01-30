#HAY QUE CAMBIAR COSAS CABRON DENTRO DEL UPDATE
#import math
import arcade
#import os

#from arcade.texture import load_texture   

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
TITULO_PANTALLA= "primer intento" 

ESCALA_PERSONAJE = 1
ESCALA_LOZA = 1
TAMANIO_SPRITE_PIXEL = 128
TAMAÑO_CUADRICULA_PIXEL = TAMANIO_SPRITE_PIXEL*ESCALA_LOZA
ESCALA_MONEDA = 0.5

#CONSTANTES DE MOVIMIENTO
VELOCIDAD_MOVIMIENTO_JUGADOR = 10
GRAVEDAD = 1
VELOCIDAD_SALTO_JUGADOR = 20

#CONSTANTES DE POSICION INICIAL
JUGADOR_EMPIEZA_X = TAMANIO_SPRITE_PIXEL * ESCALA_LOZA * 2
JUGADOR_EMPIEZA_Y = TAMANIO_SPRITE_PIXEL * ESCALA_LOZA * 1

#CONSTANTES DE LOS DISPAROS
ESCALA_SPRITE_DISPARO = 0.8
VELOCIDAD_DISPARO = 15
VELOCIDAD_BALA = 12

#CONSTANTES USADAS PARA SEGUIR SI EL JUGADOR ESTA MIRANDO A LA IZQUIERA O LA DERECHA
MIRAR_DERECHA = 0
MIRAR_IZQUIERDA = 1

#NOMBRES DE LAS CAPAS DE TILED
CAPA_NOMBRE_FONDO = "Fondo"
CAPA_NOMBRE_OBJETOS = "Cajas"
CAPA_NOMBRE_PISO = "piso"
#CAPA_NOMBRE_NO_TOCAS = "Cactus"
#CAPA_NOMBRE_LLAMA = "Llama"
#CAPA_NOMBRE_ENEMIGO ="Enemigo"

#def load_texture_pair(filename):
#    return [arcade.load_texture(filename),arcade.load_texture(filename,flipped_horizontally=True),]
#
#
#class entidad(arcade.Sprite):
#    def __init__(self):
#        
#        #config. clase padre
#        super.__init__(self, name_folder, name_file)
#
#        #direccion a la que mira por defecto
#        self.direccion_mira_personaje = MIRAR_DERECHA
#
#         # se utiliza para cambiar entre sequencias de imagenes
#        self.cur_texture = 0
#        self.scale = ESCALA_PERSONAJE
#
#        #seguimiento de que hace
#        self.saltando = False
#
#        #cargar las texturas
#        main_path = f"pimer_proyecto/recursos/imagenes/{name_folder}/{name_file}"
#
#        self.idle_texture_pair = load_texture_pair(f"{name_file}_idle.png")
#
#        # Load textures for walking
#        self.walk_textures = []
#        for i in range(3):
#            texture = load_texture_pair(f"{main_path}_Mov_{i}.png")
#            self.walk_textures.append(texture)
#
#        #conf inicar texttura
#        self.texture = self.idle_texture_pair[0]
#
#        self.hit_box = self.texture.hit_box_points
#
#
#
#class llama(entidad):
#
#    def __init__(self): 
#
#        # Conf clase padre
#        super().__init__("Llama_Blanca", "Llama_Blanca")
#
#        # Track our state
#        self.jumping = False
#        self.climbing = False
#        self.is_on_ladder = False
#
#    def update_animation(self, delta_time: float = 1 / 60):
#
#        if self.change_x < 0 and self.character_face_direction == MIRAR_DERECHA:
#            self.character_face_direction = MIRAR_IZQUIERDA
#        elif self.change_x > 0 and self.character_face_direction == MIRAR_IZQUIERDA:
#            self.character_face_direction = MIRAR_DERECHA
#
#        # Idle animation
#        if self.change_x == 0:
#            self.texture = self.idle_texture_pair[self.character_face_direction]
#            return
#
#        # Walking animation
#        self.cur_texture += 1
#        if self.cur_texture > 7:
#            self.cur_texture = 0
#        self.texture = self.walk_textures[self.cur_texture][
#            self.character_face_direction
#        ]
#
#class Enemy(entidad):
#    def __init__(self, name_folder, name_file):
#
#        # Setup parent class
#        super().__init__(name_folder, name_file)
#
#class Enemy(entidad):
#    def __init__(self, name_folder, name_file):
#
#        # Setup parent class
#        super().__init__(name_folder, name_file)
#
#
#class SoldadoEnemy(Enemy):
#    def __init__(self):
#
#        # Set up parent class
#        super().__init__("soldado", "soldado")


#class LlamaEnemy(Enemy):
#    def __init__(self):
#
#        # Set up parent class
#        super().__init__("llama_marron", "Llama_marorn")


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(ANCHO_PANTALLA, ALTO_PANTALLA, TITULO_PANTALLA)
        
        #file_path = os.path.dirname(os.path.abspath(__file__))
        #os.chdir(file_path)


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
        
        #una camara para hacer scroll en la pantalla
        self.camera = None

        #cargar sonidos
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        ##direccion hacia donde mira
        self.padonde_miro = None
        ##variables del personaje
        self.player_sprite = None
        ##motor de fisicas 
        self.physics_engine = None

        # mecanicas del disparo
        self.can_shoot = False
        self.shoot_timer = 0


    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        map_name = 'C:/Users/cpu/Desktop/Mi_proyecto_pyarcade/pimer_proyecto/recursos/mapas/mapa_de_prueba/Mapa_nivel_1.json'

        layer_options = {
            CAPA_NOMBRE_PISO: {
                "use_spatial_hash": True,
            },
            CAPA_NOMBRE_OBJETOS: {
                "use_spatial_hash": True,
            },
            #CAPA_NOMBRE_NO_TOCAS: {
            #    "use_spatial_hash": True
            #}
        }

        self.tile_map = arcade.load_tilemap(map_name, ESCALA_LOZA, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        #posicion y sprite de mi personaje
        image_source = "C:/Users/cpu/Desktop/Mi_proyecto_pyarcade/pimer_proyecto/recursos/imagenes/Llama_Blanca/Llama_blanca_idle.png"
        self.player_sprite = arcade.Sprite(image_source, ESCALA_PERSONAJE)
        #self.player_sprite = llama()
        self.player_sprite.center_x = (
            self.tile_map.tile_width * ESCALA_LOZA * JUGADOR_EMPIEZA_X
        )
        self.player_sprite.center_y = (
            self.tile_map.tile_height * ESCALA_LOZA * JUGADOR_EMPIEZA_Y
        )
        self.scene.add_sprite("Player", self.player_sprite)

        #calcular fin de mapa
        self.end_of_map = self.tile_map.width * TAMAÑO_CUADRICULA_PIXEL

         # -- Enemies
        #enemies_layer = self.tile_map.object_lists[CAPA_NOMBRE_ENEMIGO]
#
        #for my_object in enemies_layer:
        #    cartesian = self.tile_map.get_cartesian(
        #        my_object.shape[0], my_object.shape[1]
        #    )
        #    enemy_type = my_object.properties["type"]
        #    if enemy_type == "llama_marron":
        #        enemy = LlamaEnemy()
        #    elif enemy_type == "Soldado":
        #        enemy = SoldadoEnemy()
        #    else:
        #        raise Exception(f"Unknown enemy type {enemy_type}.")
        #    enemy.center_x = math.floor(
        #        cartesian[0] * ESCALA_LOZA * self.tile_map.tile_width
        #    )
        #    enemy.center_y = math.floor(
        #        (cartesian[1] + 1) * (self.tile_map.tile_height * ESCALA_LOZA)
        #    )
        #    self.scene.add_sprite(CAPA_NOMBRE_ENEMIGO, enemy)


        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVEDAD, walls=self.scene[CAPA_NOMBRE_PISO])

        # config. de la camara
        self.camera = arcade.Camera(self.width, self.height)

        # monedas de prueba
        for x in range(128, 1250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", ESCALA_MONEDA)
            coin.center_x = x
            coin.center_y = 150
            self.scene.add_sprite("Coins", coin)

        # mecanicas del disparo
        self.can_shoot = True
        self.shoot_timer = 0

        #calcular el fin del mapa
        self.end_of_map = self.tile_map.width * TAMAÑO_CUADRICULA_PIXEL

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

    def on_draw(self):
        """Render the screen."""

        arcade.start_render()
        # Code to draw the screen goes here

        self.scene.draw()
        
        # Activar la camara
        self.camera.use()

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = VELOCIDAD_MOVIMIENTO_JUGADOR
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = VELOCIDAD_SALTO_JUGADOR
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -VELOCIDAD_MOVIMIENTO_JUGADOR

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = VELOCIDAD_MOVIMIENTO_JUGADOR
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -VELOCIDAD_MOVIMIENTO_JUGADOR
        else:
            self.player_sprite.change_x = 0


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = VELOCIDAD_SALTO_JUGADOR
                arcade.play_sound(self.jump_sound)
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

    def centrar_camara_al_jugador(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # No permitas que la camara viaje mas de 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Mueve al jugador con el engine de fisicas
        self.physics_engine.update()

        if  self.player_sprite.change_x  < 0 and self.padonde_miro == MIRAR_DERECHA:
            self.padonde_miro = MIRAR_IZQUIERDA
        elif  self.player_sprite.change_x  > 0 and self.padonde_miro == MIRAR_IZQUIERDA:
            self.padonde_miro = MIRAR_DERECHA

        ## ver si le pegamos a alguna caja
        #coin_hit_list = arcade.check_for_collision_with_list(
        #    self.player_sprite, self.scene["Cactus"]
        #)
#
        ## recorre cada caja que golpeamos (si lo hacemos) y las quita
        #for coin in coin_hit_list:
        #    # Remove the coin
        #    coin.remove_from_sprite_lists()
        #    # Play a sound
        #    arcade.play_sound(self.collect_coin_sound)
        #
        # Coloca la camara
        self.centrar_camara_al_jugador()

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