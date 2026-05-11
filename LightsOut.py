import pygame
import sys
import random
import math
import os
import re
import xml.etree.ElementTree as ET

pygame.init()
try:
    pygame.mixer.init()
    AUDIO_HABILITADO = True
except pygame.error:
    AUDIO_HABILITADO = False

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Lights Out — WX-78")
reloj = pygame.time.Clock()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "assets_audio")
MUSIC_DIR = os.path.join(AUDIO_DIR, "music")
FONDOS_DIR = os.path.join(BASE_DIR, "assets", "fondos")
RUTA_SILUETA_FONDO = None

NEGRO     = (  3,   6,  16)
AZUL_MID  = ( 31,  45,  74)
GRIS_AZUL = ( 74,  90, 122)
LUNA      = (168, 192, 212)
BLANCO_FR = (212, 228, 240)
NARANJA   = (212, 116,  42)
AMBAR     = (232, 160,  64)
FUEGO     = (245, 192,  96)
ROJO      = (139,  32,  32)
VERDE     = ( 60, 160,  80)
ELECTRICO = ( 80, 180, 255)
SOMBRA_LUZ = (4, 8, 18)

fuente_titulo = pygame.font.SysFont("belisa_plumilla", 72, italic=True)
fuente_sub    = pygame.font.SysFont("belisa_plumilla", 22, italic=True)
fuente_menu   = pygame.font.SysFont("belisa_plumilla", 28)
fuente_hud    = pygame.font.SysFont("belisa_plumilla", 20)
fuente_small  = pygame.font.SysFont("belisa_plumilla", 14)
fuente_grande = pygame.font.SysFont("belisa_plumilla", 48, italic=True)

# Estrellas del menú: no se mueven de lógica, pueden ocupar toda la pantalla.
estrellas = [
    (
        random.randint(0, ANCHO),
        random.randint(0, ALTO),
        random.uniform(0.45, 1.0),
        random.uniform(0.0, math.tau),
        random.uniform(1.1, 2.4),
    )
    for _ in range(120)
]

# Estrellas del juego: separadas del menú para poder ajustar solo el gameplay.
estrellas_juego = [
    (
        random.randint(0, ANCHO),
        random.randint(0, int(ALTO * 0.60)),
        random.uniform(0.35, 0.85),
        random.uniform(0.0, math.tau),
        random.uniform(0.8, 1.8),
    )
    for _ in range(100)
]

FOG_X       = ANCHO // 2
FOG_Y       = ALTO  // 2 + 200
ZONA_Y      = FOG_Y + 5
ZONA_MARGEN = 240
PISO_ALTURA = 92
FOGATA_BASE_SCALE = 0.24
FOGATA_LLAMA_SCALE = 0.22
FOGATA_BASE_OFFSET_Y = -2
FOGATA_LLAMA_OFFSET_Y = -13
GARRA_SCALE = 0.22
WX_SCALE = 0.22
COFRE_SCALE = 0.19
ALQUIMIA_SCALE = 0.16
CROCKPOT_SCALE = 0.20
REFRI_SCALE = 0.19
WX_OFFSET_Y = 6
CAPACIDAD_CARGA_WX = 3
GARRA_OFFSET_IZQ = (-4, -4)
GARRA_OFFSET_DER = (5, 5)
PROPS_CAMPAMENTO_LAYOUT = [
    ("alquimia", (-170, 2)),
    ("cofre", (-96, 14)),
    ("crockpot", (94, 16)),
    ("refri", (172, 8)),
]
SPRITE_SIZES = {
    "leña": (50, 26),
    "carbon": (35,35),
    "engrane": (28, 28),
}
PISO_CELDA = 62
PISO_CUADRO_LADO = 5
PISO_TAM = (56, 42)
PISO_CENTRO_Y = FOG_Y
PISO_SELECTOR_VISIBLE = 6
PISO_SELECTOR_Y = ALTO - 74
TURF_NOMBRES = [
    # "Grass Turf",
    # "Grass Turf Alt",
    # "Forest Turf",
    "Marsh Turf",
    "Rocky Turf",
    # "Savanna Turf",
    "Deciduous Turf",
    # "Sandy Turf",
    "Wooden Flooring",
    "Checkerboard Flooring",
    "Carpeted Flooring",
    "Moon Crater Turf",
]
TURF_ARCHIVOS = {
    # "Grass Turf": os.path.join(BASE_DIR, "dst_turfs", "mini_grass_noise.png"),
    # "Grass Turf Alt": os.path.join(BASE_DIR, "dst_turfs", "mini_grass2_noise.png"),
    # "Forest Turf": os.path.join(BASE_DIR, "dst_turfs", "mini_forest_noise.png"),
    "Marsh Turf": os.path.join(BASE_DIR, "dst_turfs", "mini_marsh_noise.png"),
    "Rocky Turf": os.path.join(BASE_DIR, "dst_turfs", "mini_rocky_noise.png"),
    # "Savanna Turf": os.path.join(BASE_DIR, "dst_turfs", "mini_grass2_noise.png"),
    "Deciduous Turf": os.path.join(BASE_DIR, "dst_turfs", "mini_deciduous_noise.png"),
    # "Sandy Turf": os.path.join(BASE_DIR, "dst_turfs", "mini_desert_dirt_noise.png"),
    "Wooden Flooring": os.path.join(BASE_DIR, "dst_turfs", "mini_woodfloor_noise.png"),
    "Checkerboard Flooring": os.path.join(BASE_DIR, "dst_turfs", "mini_checker_noise.png"),
    "Carpeted Flooring": os.path.join(BASE_DIR, "dst_turfs", "mini_carpet_noise.png"),
    "Moon Crater Turf": os.path.join(BASE_DIR, "dst_turfs", "mini_meteor.png"),
}
LLUVIA_CANTIDAD = 90
LLUVIA_DAÑO = 0.5
LLUVIA_CD = 0.9
LLUVIA_STUN_CD = 5.0
LLUVIA_STUN_DURACION = 0.9

DIFICULTADES = {
    "Fácil": {
        "vidaInicial": 115.0,
        "vidaMax": 115.0,
        "fogataInicial": 115.0,
        "fogataMax": 115.0,
        "velocidadWx": 4.2,
        "consumoFogata": 0.82,
        "spawnObjetosInicial": 2.3,
        "spawnObjetosMin": 0.9,
        "spawnObjetosPaso": 0.012,
        "velObjetos": 0.9,
        "spawnGarrasInicial": 6.2,
        "spawnGarrasMin": 1.6,
        "spawnGarrasPaso": 0.045,
        "garrasDoblesProb": 0.22,
        "velGarras": 0.88,
        "dañoGarras": 0.8,
        "dañoFogataGarra": 14,
        "spawnSombrasInicial": 9.2,
        "spawnSombrasMin": 4.2,
        "spawnSombrasPaso": 0.08,
        "sombrasDesdeNivel": 3,
        "sombrasMaximas": 2,
        "velSombras": 0.85,
        "dañoSombras": 0.75,
        "dañoFogataSombra": 10,
        "nocheDuracion": 26.0,
        "nochesNormal": 5,
        "lluviaDesdeNoche": 5,
        "lluviaCantidad": 70,
        "lluviaDaño": 0.35,
        "lluviaCd": 1.1,
    },
    "Normal": {
        "vidaInicial": 100.0,
        "vidaMax": 100.0,
        "fogataInicial": 100.0,
        "fogataMax": 100.0,
        "velocidadWx": 4.0,
        "consumoFogata": 1.0,
        "spawnObjetosInicial": 2.0,
        "spawnObjetosMin": 0.7,
        "spawnObjetosPaso": 0.015,
        "velObjetos": 1.0,
        "spawnGarrasInicial": 5.0,
        "spawnGarrasMin": 1.2,
        "spawnGarrasPaso": 0.06,
        "garrasDoblesProb": 0.4,
        "velGarras": 1.0,
        "dañoGarras": 1.0,
        "dañoFogataGarra": 18,
        "spawnSombrasInicial": 8.0,
        "spawnSombrasMin": 3.5,
        "spawnSombrasPaso": 0.1,
        "sombrasDesdeNivel": 2,
        "sombrasMaximas": 3,
        "velSombras": 1.0,
        "dañoSombras": 1.0,
        "dañoFogataSombra": 12,
        "nocheDuracion": 30.0,
        "nochesNormal": 5,
        "lluviaDesdeNoche": 5,
        "lluviaCantidad": LLUVIA_CANTIDAD,
        "lluviaDaño": LLUVIA_DAÑO,
        "lluviaCd": LLUVIA_CD,
    },
    "Difícil": {
        "vidaInicial": 90.0,
        "vidaMax": 90.0,
        "fogataInicial": 90.0,
        "fogataMax": 90.0,
        "velocidadWx": 3.8,
        "consumoFogata": 1.22,
        "spawnObjetosInicial": 1.7,
        "spawnObjetosMin": 0.55,
        "spawnObjetosPaso": 0.02,
        "velObjetos": 1.15,
        "spawnGarrasInicial": 4.2,
        "spawnGarrasMin": 0.9,
        "spawnGarrasPaso": 0.08,
        "garrasDoblesProb": 0.62,
        "velGarras": 1.16,
        "dañoGarras": 1.3,
        "dañoFogataGarra": 24,
        "spawnSombrasInicial": 6.5,
        "spawnSombrasMin": 2.8,
        "spawnSombrasPaso": 0.14,
        "sombrasDesdeNivel": 2,
        "sombrasMaximas": 4,
        "velSombras": 1.18,
        "dañoSombras": 1.35,
        "dañoFogataSombra": 16,
        "nocheDuracion": 34.0,
        "nochesNormal": 5,
        "lluviaDesdeNoche": 4,
        "lluviaCantidad": 110,
        "lluviaDaño": 0.7,
        "lluviaCd": 0.75,
    },
      "Extremo": {
        "vidaInicial": 30.0,
        "vidaMax": 90.0,
        "fogataInicial": 40.0,
        "fogataMax": 90.0,
        "velocidadWx": 3.8,
        "consumoFogata": 1.22,
        "spawnObjetosInicial": 1.7,
        "spawnObjetosMin": 0.55,
        "spawnObjetosPaso": 0.02,
        "velObjetos": 1.15,
        "spawnGarrasInicial": 4.2,
        "spawnGarrasMin": 0.7,
        "spawnGarrasPaso": 0.08,
        "garrasDoblesProb": 0.62,
        "velGarras": 1.16,
        "dañoGarras": 1.3,
        "dañoFogataGarra": 20,
        "spawnSombrasInicial": 6.5,
        "spawnSombrasMin": 2.8,
        "spawnSombrasPaso": 0.14,
        "sombrasDesdeNivel": 2,
        "sombrasMaximas": 4,
        "velSombras": 1.18,
        "dañoSombras": 1.35,
        "dañoFogataSombra": 16,
        "nocheDuracion": 34.0,
        "nochesNormal": 5,
        "lluviaDesdeNoche": 1,
        "lluviaCantidad": 130,
        "lluviaDaño": 0.6,
        "lluviaCd": 0.75,
    },
}
DIFICULTAD_NOMBRES = list(DIFICULTADES.keys())


class ScmlAnimation:
    def __init__(self, scml_path, animation_name, scale=1.0, padding=0):
        self.frames = []
        self.origin = (0, 0)
        self.key_times = []
        self.length_ms = 1
        self._cargar_desde_scml(scml_path, animation_name, scale, padding)

    def _cargar_desde_scml(self, scml_path, animation_name, scale, padding):
        root = ET.parse(scml_path).getroot()
        asset_dir = os.path.dirname(scml_path)
        folders = {}

        for folder in root.findall("folder"):
            folder_id = int(folder.get("id", 0))
            files = {}
            for file_node in folder.findall("file"):
                file_id = int(file_node.get("id", 0))
                ruta = os.path.join(asset_dir, file_node.get("name", "").replace("/", os.sep))
                if not os.path.exists(ruta):
                    continue
                files[file_id] = {
                    "image": pygame.image.load(ruta).convert_alpha(),
                    "pivot_x": float(file_node.get("pivot_x", 0.0)),
                    "pivot_y": float(file_node.get("pivot_y", 1.0)),
                }
            folders[folder_id] = files

        entity = root.find("entity")
        if entity is None:
            return

        animation = None
        for candidate in entity.findall("animation"):
            if candidate.get("name") == animation_name:
                animation = candidate
                break
        if animation is None:
            return
        self.length_ms = max(1, int(animation.get("length", "1")))

        timelines = {}
        for timeline in animation.findall("timeline"):
            timeline_id = int(timeline.get("id", 0))
            timelines[timeline_id] = {}
            for key_node in timeline.findall("key"):
                key_id = int(key_node.get("id", 0))
                timelines[timeline_id][key_id] = key_node.find("object")

        lienzos = []
        union_rect = None
        canvas_size = 1024
        center = canvas_size // 2

        mainline = animation.find("mainline")
        if mainline is None:
            return

        for main_key in mainline.findall("key"):
            self.key_times.append(int(main_key.get("time", "0")))
            frame = pygame.Surface((canvas_size, canvas_size), pygame.SRCALPHA)
            object_refs = sorted(
                main_key.findall("object_ref"),
                key=lambda ref: int(ref.get("z_index", 0))
            )

            for ref in object_refs:
                timeline_id = int(ref.get("timeline", 0))
                key_id = int(ref.get("key", 0))
                obj = timelines.get(timeline_id, {}).get(key_id)
                if obj is None:
                    continue

                folder_id = int(obj.get("folder", 0))
                file_id = int(obj.get("file", 0))
                meta = folders.get(folder_id, {}).get(file_id)
                if meta is None:
                    continue

                sprite = meta["image"]
                pivot_x = float(obj.get("pivot_x", meta["pivot_x"]))
                pivot_y = float(obj.get("pivot_y", meta["pivot_y"]))
                pos_x = float(obj.get("x", 0.0)) * scale
                pos_y = float(obj.get("y", 0.0)) * scale
                scale_x = float(obj.get("scale_x", 1.0)) * scale
                scale_y = float(obj.get("scale_y", 1.0)) * scale
                alpha = float(obj.get("a", 1.0))

                ancho = max(1, int(round(sprite.get_width() * abs(scale_x))))
                alto = max(1, int(round(sprite.get_height() * abs(scale_y))))
                if ancho != sprite.get_width() or alto != sprite.get_height():
                    sprite = pygame.transform.smoothscale(sprite, (ancho, alto))

                if scale_x < 0 or scale_y < 0:
                    sprite = pygame.transform.flip(sprite, scale_x < 0, scale_y < 0)

                if alpha < 1.0:
                    sprite = sprite.copy()
                    sprite.set_alpha(int(255 * alpha))

                draw_x = center + pos_x - pivot_x * sprite.get_width()
                draw_y = center - pos_y - (1.0 - pivot_y) * sprite.get_height()
                frame.blit(sprite, (int(round(draw_x)), int(round(draw_y))))

            rect = frame.get_bounding_rect()
            if rect.width and rect.height:
                union_rect = rect if union_rect is None else union_rect.union(rect)
            lienzos.append(frame)

        if union_rect is None:
            return

        if padding > 0:
            left = max(0, union_rect.left - padding)
            top = max(0, union_rect.top - padding)
            right = min(canvas_size, union_rect.right + padding)
            bottom = min(canvas_size, union_rect.bottom + padding)
            union_rect = pygame.Rect(left, top, right - left, bottom - top)

        self.origin = (center - union_rect.left, center - union_rect.top)
        for frame in lienzos:
            self.frames.append(frame.subsurface(union_rect).copy())

    def dibujar(self, surf, x, y, t):
        frame = self.obtener_frame(t)
        if frame is None:
            return False
        surf.blit(frame, (int(x - self.origin[0]), int(y - self.origin[1])))
        return True

    def obtener_frame(self, t):
        if not self.frames:
            return None
        tiempo_ms = int(t * 1000) % self.length_ms
        idx = 0
        for i, key_time in enumerate(self.key_times):
            if tiempo_ms >= key_time:
                idx = i
            else:
                break
        return self.frames[idx]

# ── FUNCIONES VISUALES ───────────────────
anim_fogata_base = None
anim_fogata_llama = None
anim_garra = None
anim_wx_idle = None
anim_wx_run = None
anim_cofre = None
anim_alquimia = None
anim_crockpot = None
anim_refri = None
sprites_objetos = {}
sprites_pisos = []
silueta_fondo_base = None
silueta_fondo_preparada = None
silueta_fondo_tamano = None
tablero_pisos = []
turf_seleccionado_idx = 0
turf_cache = {}
mascara_piso_cache = {}
sombra_piso_cache = {}
sonidos = {}
canales_audio = {}
musicas = {}
musica_actual = None


def cargar_sonido(nombre_archivo, volumen=1.0):
    if not AUDIO_HABILITADO:
        return None
    ruta = os.path.join(AUDIO_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        return None
    try:
        sonido = pygame.mixer.Sound(ruta)
        sonido.set_volume(volumen)
        return sonido
    except pygame.error:
        return None


def cargar_audio():
    global sonidos, canales_audio, musicas, musica_actual
    canales_audio = {}
    musicas = {}
    musica_actual = None
    if AUDIO_HABILITADO:
        try:
            pygame.mixer.set_num_channels(16)
            pygame.mixer.set_reserved(5)
        except pygame.error:
            pass
        canales_audio = {
            "fogata_1": pygame.mixer.Channel(0),
            "fogata_2": pygame.mixer.Channel(1),
            "fogata_3": pygame.mixer.Channel(2),
            "pasos_wx": pygame.mixer.Channel(3),
            "lluvia": pygame.mixer.Channel(4),
        }
        ruta_musica_menu = os.path.join(MUSIC_DIR, "menu_theme.wav")
        ruta_musica_juego = os.path.join(MUSIC_DIR,  "dst_battle_loop.wav")
        if os.path.exists(ruta_musica_menu):
            musicas["menu"] = ruta_musica_menu
        if os.path.exists(ruta_musica_juego):
            musicas["juego"] = ruta_musica_juego
    sonidos = {
        "menu_mover": cargar_sonido("HUD_craft_close.wav", 0.35),
        "menu_aceptar": cargar_sonido("Map_close.wav", 0.45),
        "garra_aparece": [
            sonido for sonido in [
                cargar_sonido("charlie_warn_1.wav", 0.42),
                cargar_sonido("charlie_warn_2.wav", 0.42),
                cargar_sonido("charlie_warn_3.wav", 0.42),
                cargar_sonido("charlie_warn_4.wav", 0.42),
            ] if sonido
        ],
        "garra_muerde": cargar_sonido("charlie_bite.wav", 0.5),
        "locura": [
            sonido for sonido in [
                cargar_sonido("sanity_random_pulse_8.wav", 0.42),
                cargar_sonido("sanity_random_pulse_9.wav", 0.42),
                cargar_sonido("sanity_random_pulse_10.wav", 0.42),
                cargar_sonido("sanity_random_pulse_11.wav", 0.42),
                cargar_sonido("sanity_random_pulse_12.wav", 0.42),
                cargar_sonido("sanity_random_pulse_13.wav", 0.42),
            ] if sonido
        ],
        "golpe_wx": [
            sonido for sonido in [
                cargar_sonido("foley_metalArmour_4.wav", 0.5),
                cargar_sonido("foley_metalArmour_5.wav", 0.48),
                cargar_sonido("foley_metalArmour_6.wav", 0.5),
            ] if sonido
        ],
        "golpe_sombra": [
            sonido for sonido in [
                cargar_sonido("hit_response_sanitycreature_1.wav", 0.58),
                cargar_sonido("hit_response_sanitycreature_2.wav", 0.58),
            ] if sonido
        ],
        "fogata_leña": cargar_sonido(os.path.join("pickups", "wood_fuel.wav"), 0.6),
        "fogata_carbon": cargar_sonido(os.path.join("pickups", "charcoal_fuel.wav"), 0.62),
        "pasos_wx": [
            sonido for sonido in [
                cargar_sonido(os.path.join("wx_steps", "footstep_grass_1.wav"), 0.88),
                cargar_sonido(os.path.join("wx_steps", "footstep_grass_2.wav"), 0.92),
                cargar_sonido(os.path.join("wx_steps", "footstep_grass_3.wav"), 0.9),
                cargar_sonido(os.path.join("wx_steps", "footstep_grass_4.wav"), 0.9),
            ] if sonido
        ],
        "wx_engrane_comer": cargar_sonido(os.path.join("pickups", "wx_eat_gear.wav"), 0.55),
        "fogata_loop_1": cargar_sonido(os.path.join("campfire", "campfire_layer2_LP.wav"), 0.82),
        "fogata_loop_2": cargar_sonido(os.path.join("campfire", "campfire_layer3_1_LP.wav"), 0.72),
        "fogata_loop_3": cargar_sonido(os.path.join("campfire", "campfire_layer3_3_LP.wav"), 0.58),
        "lluvia_loop": cargar_sonido(os.path.join("rain", "rain_loop.wav"), 0.34),
        "lluvia_hit": [
            sonido for sonido in [
                cargar_sonido(os.path.join("rain", "rain_hit_147.wav"), 0.3),
                cargar_sonido(os.path.join("rain", "rain_hit_148.wav"), 0.3),
                cargar_sonido(os.path.join("rain", "rain_hit_149.wav"), 0.3),
                cargar_sonido(os.path.join("rain", "rain_hit_150.wav"), 0.3),
            ] if sonido
        ],
        "lluvia_spark": [
            sonido for sonido in [
                cargar_sonido(os.path.join("rain", "rain_spark_1087.wav"), 0.22),
                cargar_sonido(os.path.join("rain", "rain_spark_1088.wav"), 0.22),
                cargar_sonido(os.path.join("rain", "rain_spark_1089.wav"), 0.22),
            ] if sonido
        ],
    }


def reproducir_sonido(clave):
    sonido = sonidos.get(clave)
    if not sonido:
        return
    if isinstance(sonido, list):
        if sonido:
            random.choice(sonido).play()
    else:
        sonido.play()


def reproducir_pasos_wx():
    canal = canales_audio.get("pasos_wx")
    pasos = sonidos.get("pasos_wx")
    if canal is None or not pasos:
        reproducir_sonido("pasos_wx")
        return
    if canal.get_busy():
        return
    canal.play(random.choice(pasos))


def reproducir_engrane_wx():
    comer = sonidos.get("wx_engrane_comer")
    if comer:
        comer.play()


def reproducir_lluvia_wx():
    hit = sonidos.get("lluvia_hit")
    spark = sonidos.get("lluvia_spark")
    if hit:
        random.choice(hit).play()
    if spark:
        random.choice(spark).play()


def reproducir_golpe_wx(origen="general"):
    if origen == "sombra":
        reproducir_sonido("golpe_sombra")
    else:
        reproducir_sonido("golpe_wx")


def reproducir_loop(clave_sonido, canal_clave):
    if not AUDIO_HABILITADO:
        return
    canal = canales_audio.get(canal_clave)
    sonido = sonidos.get(clave_sonido)
    if canal is None or sonido is None:
        return
    if not canal.get_busy():
        canal.play(sonido, loops=-1)


def detener_loop(canal_clave):
    canal = canales_audio.get(canal_clave)
    if canal is not None:
        canal.stop()


def reproducir_musica(clave, volumen):
    global musica_actual
    if not AUDIO_HABILITADO:
        return
    ruta = musicas.get(clave)
    if ruta is None:
        return
    if musica_actual != clave:
        try:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.set_volume(volumen)
            pygame.mixer.music.play(-1)
            musica_actual = clave
        except pygame.error:
            return
    elif not pygame.mixer.music.get_busy():
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1)


def detener_musica():
    global musica_actual
    if AUDIO_HABILITADO and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    musica_actual = None


def cargar_sprite_ajustado(ruta, tamaño):
    if not os.path.exists(ruta):
        return None
    sprite = pygame.image.load(ruta).convert_alpha()
    max_w, max_h = tamaño
    factor = min(max_w / sprite.get_width(), max_h / sprite.get_height())
    ancho = max(1, int(round(sprite.get_width() * factor)))
    alto = max(1, int(round(sprite.get_height() * factor)))
    return pygame.transform.smoothscale(sprite, (ancho, alto))


def cargar_silueta_fondo():
    global silueta_fondo_base, silueta_fondo_preparada, silueta_fondo_tamano, RUTA_SILUETA_FONDO
    silueta_fondo_base = None
    silueta_fondo_preparada = None
    silueta_fondo_tamano = None
    RUTA_SILUETA_FONDO = None

    if not os.path.isdir(FONDOS_DIR):
        print(f"No existe la carpeta de fondos: {FONDOS_DIR}")
        return

    extensiones_validas = (".png", ".jpg", ".jpeg")
    rutas_candidatas = [
        os.path.join(FONDOS_DIR, nombre)
        for nombre in os.listdir(FONDOS_DIR)
        if nombre.lower().endswith(extensiones_validas)
        and (nombre.lower().startswith("silueta_") or nombre.lower().startswith("siluetas_"))
    ]

    if not rutas_candidatas:
        print(f"No se encontró ninguna silueta en: {FONDOS_DIR}")
        return

    rutas_candidatas.sort(key=natural_key)
    random.shuffle(rutas_candidatas)

    for ruta in rutas_candidatas:
        try:
            silueta_fondo_base = pygame.image.load(ruta).convert_alpha()
            RUTA_SILUETA_FONDO = ruta
            print(f"Silueta cargada: {os.path.basename(ruta)}")
            return
        except pygame.error as exc:
            print(f"Silueta ignorada: {os.path.basename(ruta)} ({exc})")

    print(f"No se pudo cargar ninguna silueta válida en: {FONDOS_DIR}")


def obtener_silueta_fondo():
    global silueta_fondo_preparada, silueta_fondo_tamano
    if silueta_fondo_base is None:
        return None

    alto_objetivo = 190
    factor = alto_objetivo / silueta_fondo_base.get_height()
    ancho_objetivo = max(1, int(round(silueta_fondo_base.get_width() * factor)))
    tamaño_objetivo = (ancho_objetivo, alto_objetivo)

    if silueta_fondo_preparada is None or silueta_fondo_tamano != tamaño_objetivo:
        silueta = pygame.transform.smoothscale(silueta_fondo_base, tamaño_objetivo)

        # Aclara la silueta sin destruir su transparencia.
        # BLEND_RGBA_ADD sube el valor visual; MULT la oscurecía todavía más.
        silueta.fill((24,17,27, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Más opaca para que no se pierda contra el cielo.
        silueta.set_alpha(230)
        silueta_fondo_preparada = silueta
        silueta_fondo_tamano = tamaño_objetivo

    return silueta_fondo_preparada


def natural_key(texto):
    return [int(parte) if parte.isdigit() else parte.lower() for parte in re.split(r"(\d+)", texto)]


def turf_actual():
    return TURF_NOMBRES[turf_seleccionado_idx]


def cargar_sprites_desde_directorio(directorio, tamaño):
    if not os.path.isdir(directorio):
        return []
    rutas = [
        os.path.join(directorio, nombre)
        for nombre in sorted(os.listdir(directorio), key=natural_key)
        if nombre.lower().endswith(".png")
    ]
    return [sprite for sprite in (cargar_sprite_ajustado(ruta, tamaño) for ruta in rutas) if sprite]


def crear_tablero_pisos():
    global tablero_pisos
    tablero_pisos = [[None for _ in range(PISO_CUADRO_LADO)] for _ in range(PISO_CUADRO_LADO)]


def rect_tablero_pisos():
    lado_px = PISO_CELDA * PISO_CUADRO_LADO
    return pygame.Rect(FOG_X - lado_px // 2, PISO_CENTRO_Y - lado_px // 2, lado_px, lado_px)


def rect_celda_piso(fila, columna):
    tablero = rect_tablero_pisos()
    return pygame.Rect(
        tablero.x + columna * PISO_CELDA,
        tablero.y + fila * PISO_CELDA,
        PISO_CELDA,
        PISO_CELDA,
    )


def celda_desde_pos(pos):
    tablero = rect_tablero_pisos()
    if not tablero.collidepoint(pos):
        return None
    columna = (pos[0] - tablero.x) // PISO_CELDA
    fila = (pos[1] - tablero.y) // PISO_CELDA
    if 0 <= fila < PISO_CUADRO_LADO and 0 <= columna < PISO_CUADRO_LADO:
        return int(fila), int(columna)
    return None


def celda_fogata():
    centro = PISO_CUADRO_LADO // 2
    return centro, centro


def celda_wx():
    if wx is None:
        return None
    pie_x = wx.x + wx.w // 2
    pie_y = wx.y + wx.h - 4
    return celda_desde_pos((pie_x, pie_y))


def seleccionar_turf(delta):
    global turf_seleccionado_idx
    turf_seleccionado_idx = (turf_seleccionado_idx + delta) % len(TURF_NOMBRES)


def generar_superficie_turf(nombre, tamaño):
    ruta = TURF_ARCHIVOS.get(nombre)
    if not ruta or not os.path.exists(ruta):
        return pygame.Surface(tamaño, pygame.SRCALPHA)
    fuente = pygame.image.load(ruta).convert_alpha()
    ancho, alto = tamaño
    destino = pygame.Surface((ancho, alto), pygame.SRCALPHA)

    if fuente.get_width() == 0 or fuente.get_height() == 0:
        return destino

    escala = alto / fuente.get_height()
    tile_w = max(1, int(round(fuente.get_width() * escala)))
    tile = pygame.transform.smoothscale(fuente, (tile_w, alto))

    x = 0
    while x < ancho:
        destino.blit(tile, (x, 0))
        x += tile_w

    # Frio nocturno base: mantiene la textura real, pero la lleva a una paleta azulada.
    destino.fill((135, 145, 160, 255), special_flags=pygame.BLEND_RGBA_MULT)
    destino.fill((6, 8, 10, 0), special_flags=pygame.BLEND_RGBA_SUB)

    velo = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    velo.fill((8, 12, 18, 28))
    destino.blit(velo, (0, 0))

    return destino


def obtener_superficie_turf(nombre, tamaño):
    key = (nombre, tamaño)
    if key not in turf_cache:
        turf_cache[key] = generar_superficie_turf(nombre, tamaño)
    return turf_cache[key]


def obtener_mascara_visibilidad_piso(tamaño):
    key = tuple(tamaño)
    if key in mascara_piso_cache:
        return mascara_piso_cache[key]

    ancho, alto = tamaño
    mascara = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    centro = (ancho // 2, alto // 2 + 4)
    radio_x = max(1, int(ancho * 0.47))
    radio_y = max(1, int(alto * 0.48))
    for paso in range(40, 0, -1):
        t = paso / 40
        alpha = int(255 * (t ** 1.7))
        ovalo = pygame.Rect(0, 0, max(2, int(radio_x * 2 * t)), max(2, int(radio_y * 2 * t)))
        ovalo.center = centro
        pygame.draw.ellipse(mascara, (255, 255, 255, alpha), ovalo)

    mascara_piso_cache[key] = mascara
    return mascara


def obtener_sombra_dinamica_piso(tamaño, fogata_ratio, centro_x, centro_y):
    bucket = int(round(max(0.0, min(1.0, fogata_ratio)) * 20))
    key = (tuple(tamaño), bucket, int(centro_x), int(centro_y))
    if key in sombra_piso_cache:
        return sombra_piso_cache[key]

    ancho, alto = tamaño
    sombra = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    ratio = bucket / 20.0
    radio_x = max(1, ancho * (0.11 + 0.26 * ratio))
    radio_y = max(1, alto * (0.30 + 0.32 * ratio))
    alpha_base = 42 + 170 * (1.0 - ratio)

    for x in range(ancho):
        dx = abs(x - centro_x) / radio_x
        for y in range(alto):
            dy = abs(y - centro_y) / radio_y
            dist = math.sqrt(dx * dx + dy * dy)
            cercania = max(0.0, 1.0 - dist)
            alpha = int(alpha_base * ((1.0 - cercania) ** 0.9))
            if alpha > 0:
                sombra.set_at((x, y), (4, 6, 10, min(255, alpha)))

    sombra_piso_cache[key] = sombra
    return sombra


def colocar_turf_en_celda(celda, turf_idx=None):
    if celda is None or not sprites_pisos:
        return
    fila, columna = celda
    if 0 <= fila < PISO_CUADRO_LADO and 0 <= columna < PISO_CUADRO_LADO:
        tablero_pisos[fila][columna] = turf_seleccionado_idx if turf_idx is None else turf_idx


def limpiar_turf_en_celda(celda):
    if celda is None:
        return
    fila, columna = celda
    if 0 <= fila < PISO_CUADRO_LADO and 0 <= columna < PISO_CUADRO_LADO:
        tablero_pisos[fila][columna] = None


def rango_selector_turfs():
    total = len(sprites_pisos)
    if total <= PISO_SELECTOR_VISIBLE:
        return 0, total
    inicio = max(0, turf_seleccionado_idx - PISO_SELECTOR_VISIBLE // 2)
    fin = min(total, inicio + PISO_SELECTOR_VISIBLE)
    inicio = max(0, fin - PISO_SELECTOR_VISIBLE)
    return inicio, fin


def rects_selector_turfs():
    inicio, fin = rango_selector_turfs()
    cantidad = fin - inicio
    separacion = 8
    ancho_item = 56
    alto_item = 56
    ancho_total = cantidad * ancho_item + max(0, cantidad - 1) * separacion
    x = ANCHO // 2 - ancho_total // 2
    rects = []
    for idx in range(inicio, fin):
        rect = pygame.Rect(x, PISO_SELECTOR_Y, ancho_item, alto_item)
        rects.append((idx, rect))
        x += ancho_item + separacion
    return rects


def cargar_animaciones():
    global anim_fogata_base, anim_fogata_llama, anim_garra, anim_wx_idle, anim_wx_run
    global anim_cofre, anim_alquimia, anim_crockpot, anim_refri
    global sprites_objetos, sprites_pisos

    ruta_base = os.path.join(BASE_DIR, "dst_extract", "firepit", "firepit.scml")
    ruta_llama = os.path.join(BASE_DIR, "dst_extract", "campfire_fire", "campfire_fire.scml")
    ruta_garra = os.path.join(BASE_DIR, "dst_extract", "creepy_hands", "creepy_hands.scml")
    ruta_wx = os.path.join(BASE_DIR, "dst_extract", "wx78", "wx78.scml")
    ruta_cofre = os.path.join(BASE_DIR, "dst_extract", "treasure_chest", "treasure_chest.scml")
    ruta_alquimia = os.path.join(BASE_DIR, "dst_extract", "researchlab2", "researchlab2.scml")
    ruta_crockpot = os.path.join(BASE_DIR, "dst_extract", "cook_pot", "cook_pot.scml")
    ruta_refri = os.path.join(BASE_DIR, "dst_extract", "ice_box", "ice_box.scml")

    anim_fogata_base = None
    anim_fogata_llama = None
    anim_garra = None
    anim_wx_idle = None
    anim_wx_run = None
    anim_cofre = None
    anim_alquimia = None
    anim_crockpot = None
    anim_refri = None
    sprites_objetos = {}
    cargar_silueta_fondo()

    if os.path.exists(ruta_base):
        try:
            anim_fogata_base = ScmlAnimation(ruta_base, "idle", scale=FOGATA_BASE_SCALE)
        except Exception as exc:
            print(f"No se pudo cargar la base de la fogata: {exc}")

    if os.path.exists(ruta_llama):
        try:
            anim_fogata_llama = ScmlAnimation(ruta_llama, "level3", scale=FOGATA_LLAMA_SCALE)
        except Exception as exc:
            print(f"No se pudo cargar la llama de la fogata: {exc}")

    if os.path.exists(ruta_garra):
        try:
            anim_garra = ScmlAnimation(ruta_garra, "idle", scale=GARRA_SCALE)
        except Exception as exc:
            print(f"No se pudo cargar la garra animada: {exc}")

    if os.path.exists(ruta_wx):
        try:
            anim_wx_idle = ScmlAnimation(ruta_wx, "idle_wx_side", scale=WX_SCALE)
            anim_wx_run = ScmlAnimation(ruta_wx, "run_loop_side", scale=WX_SCALE)
        except Exception as exc:
            print(f"No se pudo cargar la animacion de WX-78: {exc}")

    if os.path.exists(ruta_cofre):
        try:
            anim_cofre = ScmlAnimation(ruta_cofre, "closed", scale=COFRE_SCALE)
        except Exception as exc:
            print(f"No se pudo cargar el cofre: {exc}")

    if os.path.exists(ruta_alquimia):
        try:
            anim_alquimia = ScmlAnimation(ruta_alquimia, "idle", scale=ALQUIMIA_SCALE)
        except Exception as exc:
            print(f"No se pudo cargar la maquina de alquimia: {exc}")

    if os.path.exists(ruta_crockpot):
        try:
            anim_crockpot = ScmlAnimation(ruta_crockpot, "idle_empty", scale=CROCKPOT_SCALE)
        except Exception as exc:
            print(f"No se pudo cargar la crockpot: {exc}")

    if os.path.exists(ruta_refri):
        try:
            anim_refri = ScmlAnimation(ruta_refri, "closed", scale=REFRI_SCALE)
        except Exception as exc:
            print(f"No se pudo cargar el refri: {exc}")

    sprites_objetos["leña"] = cargar_sprite_ajustado(
        os.path.join(BASE_DIR, "dst_extract", "log", "log01", "log01-0.png"),
        SPRITE_SIZES["leña"],
    )
    sprites_objetos["carbon"] = cargar_sprite_ajustado(
        os.path.join(BASE_DIR, "dst_extract", "charcoal", "charcoal01", "charcoal01-1.png"),
        SPRITE_SIZES["carbon"],
    )
    sprites_objetos["engrane"] = cargar_sprite_ajustado(
        os.path.join(BASE_DIR, "dst_extract", "gears", "gears01", "gears01-1.png"),
        SPRITE_SIZES["engrane"],
    )

    sprites_pisos = []
    for carpeta in (
        os.path.join(BASE_DIR, "dst_extract", "firepit", "stones"),
        os.path.join(BASE_DIR, "dst_extract", "firepit", "singlestone"),
        os.path.join(BASE_DIR, "dst_extract", "coldfirepit", "coldstones"),
    ):
        for i, sprite in enumerate(cargar_sprites_desde_directorio(carpeta, PISO_TAM)):
            sprites_pisos.append(
                {
                    "nombre": f"{os.path.basename(carpeta)}-{i + 1}",
                    "sprite": sprite,
                }
            )
    crear_tablero_pisos()


def dibujar_estrellas(surf, t, centro_luz=None, radio_luz=0, lista_estrellas=None):
    radio_sq = radio_luz * radio_luz
    if lista_estrellas is None:
        lista_estrellas = estrellas

    for (ex, ey, brillo_base, fase, velocidad) in lista_estrellas:
        if centro_luz is not None:
            dx = ex - centro_luz[0]
            dy = ey - centro_luz[1]
            if dx * dx + dy * dy <= radio_sq:
                continue
        onda_lenta = (math.sin(t * velocidad + fase) + 1) * 0.5
        onda_rapida = (math.sin(t * (velocidad * 2.7) + fase * 1.9) + 1) * 0.5
        destello = max(0.0, math.sin(t * (velocidad * 4.8) + fase * 2.3)) ** 8
        brillo = brillo_base * (0.45 + 0.30 * onda_lenta + 0.25 * onda_rapida) + 0.55 * destello
        brillo = min(1.35, brillo)
        c = (
            min(255, int(190 * brillo)),
            min(255, int(220 * brillo)),
            min(255, int(255 * brillo)),
        )
        pygame.draw.circle(surf, c, (ex, ey), 1)


# --- Fondo de juego ---
def dibujar_fondo_juego(surf, t):
    # Cielo oscuro con degradado sutil.
    for y in range(ALTO):
        mezcla = y / ALTO

        # Mantiene el fondo inferior oscuro como antes,
        # pero aclara ligeramente la parte superior del cielo.
        top_mix = min(1.0, mezcla ** 1.35 * 1.35)

        r = int(10 * (1 - top_mix) + 4 * top_mix)
        g = int(16 * (1 - top_mix) + 7 * top_mix)
        b = int(34 * (1 - top_mix) + 18 * top_mix)

        pygame.draw.line(surf, (r, g, b), (0, y), (ANCHO, y))

    # Banda de cielo un poco más clara detrás de las montañas para mejorar lectura.
    velo_cielo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    inicio_claro = 120
    fin_claro =  400
    rango_claro = fin_claro - inicio_claro
    for y in range(inicio_claro, fin_claro):
        progreso = (y - inicio_claro) / rango_claro
        campana = math.sin(progreso * math.pi)
        alpha = int(20 * campana)
        tono = (
            int(18 + 8 * campana),
            int(24 + 10 * campana),
            int(36 + 14 * campana),
            alpha,
        )
        pygame.draw.line(velo_cielo, tono, (0, y), (ANCHO, y))
    surf.blit(velo_cielo, (0, 0))

    # Usa las estrellas globales animadas también durante el gameplay.
    dibujar_estrellas(surf, t, lista_estrellas=estrellas_juego)

    # Siluetas PNG sutiles y oscuras, con un parallax lento para dar vida al fondo.
    silueta = obtener_silueta_fondo()
    if silueta is not None:
        silueta_y = 210
        tile_w = silueta.get_width()
        solape = 28
        paso_tile = max(1, tile_w - solape)
        offset_x = 0
        inicio_x = -paso_tile

        x = inicio_x
        while x < ANCHO + paso_tile:
            surf.blit(silueta, (x, silueta_y))
            x += paso_tile

    # Niebla baja detrás del área de juego.
    niebla_fondo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    for i in range(7):
        nx = int((i * 160 + math.sin(t * 0.035 + i) * 70) % (ANCHO + 260)) - 130
        ny = 360 + int(math.sin(t * 0.06 + i * 0.8) * 16)
        pygame.draw.ellipse(niebla_fondo, (24, 28, 38, 15), (nx, ny, 300, 65))
    surf.blit(niebla_fondo, (0, 0))

def dibujar_fogata(surf, cx, cy, t):
    llama_y = cy + FOGATA_LLAMA_OFFSET_Y
    base_dibujada = False
    if anim_fogata_base:
        anim_fogata_base.dibujar(surf, cx, cy + FOGATA_BASE_OFFSET_Y, t)
        base_dibujada = True
    else:
        pygame.draw.ellipse(surf,(42,26,10),(cx-28,cy+10,56,14))
        pygame.draw.line(surf,(61,37,16),(cx-24,cy+16),(cx+10,cy+10),7)
        pygame.draw.line(surf,(61,37,16),(cx+24,cy+16),(cx-10,cy+10),7)
        pygame.draw.ellipse(surf,(180,60,0),(cx-18,cy+8,36,10))
        pygame.draw.ellipse(surf,(220,90,10),(cx-10,cy+10,20,6))
        base_dibujada = True

    if anim_fogata_llama:
        anim_fogata_llama.dibujar(surf, cx, llama_y, t)
        return

    if not base_dibujada:
        pygame.draw.ellipse(surf,(42,26,10),(cx-28,cy+10,56,14))
        pygame.draw.line(surf,(61,37,16),(cx-24,cy+16),(cx+10,cy+10),7)
        pygame.draw.line(surf,(61,37,16),(cx+24,cy+16),(cx-10,cy+10),7)
        pygame.draw.ellipse(surf,(180,60,0),(cx-18,cy+8,36,10))
    for i,(color,rx,ry,off) in enumerate([
        ((139,40,0),9,22,0),((200,80,10),7,18,2),
        ((230,130,20),5,14,4),((245,192,96),3,9,6),
    ]):
        ondeo = math.sin(t*6+i*1.2)*2
        pts = [(cx+ondeo,llama_y-ry*2+off),(cx+rx,llama_y-ry+off),
               (cx+rx*.5,llama_y+off),(cx-rx*.5,llama_y+off),(cx-rx,llama_y-ry+off)]
        pygame.draw.polygon(surf,color,pts)


def dibujar_props_campamento(surf, cx, cy, t):
    animaciones = {
        "cofre": anim_cofre,
        "alquimia": anim_alquimia,
        "crockpot": anim_crockpot,
        "refri": anim_refri,
    }
    for nombre, (offset_x, offset_y) in PROPS_CAMPAMENTO_LAYOUT:
        anim = animaciones.get(nombre)
        if anim is not None:
            anim.dibujar(surf, cx + offset_x, cy + offset_y, t)


def dibujar_pisos(surf):
    rect = pygame.Rect(FOG_X - ZONA_MARGEN, ZONA_Y - PISO_ALTURA // 2, ZONA_MARGEN * 2, PISO_ALTURA)
    textura = obtener_superficie_turf(turf_actual(), (rect.w, rect.h))

    fogata_ratio = 1.0 if fogata_max <= 0 else max(0.0, min(1.0, fogata / fogata_max))
    sombra_base = pygame.Surface((rect.w + 600, rect.h + 220), pygame.SRCALPHA)
    for i in range(18):
     alpha = max(0, 18 - i)
     shrink_x = i * 10
     shrink_y = i * 5

     rect_sombra = pygame.Rect(
        shrink_x,
        shrink_y,
        sombra_base.get_width() - shrink_x * 2,
        sombra_base.get_height() - shrink_y * 2,
    )

    pygame.draw.ellipse(
        sombra_base,
        (0, 0, 0, alpha * 2),
        rect_sombra,
    )
    sombra_rect = sombra_base.get_rect(center=(rect.centerx, rect.centery + 18))
    centro_sombra_x = FOG_X - sombra_rect.x
    centro_sombra_y = FOG_Y - sombra_rect.y + 6

    halo_piso = sombra_base.copy()
    radio_x_halo = max(1, int(rect.w * (0.01 + 0.32 * fogata_ratio)))
    radio_y_halo = max(1, int(rect.h * (0.23 + 0.31 * fogata_ratio)))
    halo_frio = pygame.Surface(halo_piso.get_size(), pygame.SRCALPHA)
    for paso in range(26, 0, -1):
        t = paso / 26
        alpha = int((4 + 16 * fogata_ratio) * (t ** 2.0))
        ovalo = pygame.Rect(0, 0, max(2, int(radio_x_halo * 2.9 * t)), max(2, int(radio_y_halo * 2.5 * t)))
        ovalo.center = (centro_sombra_x, centro_sombra_y)
        pygame.draw.ellipse(halo_frio, (18, 30, 48, alpha), ovalo)
    halo_piso.blit(halo_frio, (0, 0))

    halo_calido = pygame.Surface(halo_piso.get_size(), pygame.SRCALPHA)
    for paso in range(24, 0, -1):
        t = paso / 16
        alpha = int((3 + 10 * fogata_ratio) * (t ** 3.4))
        ovalo = pygame.Rect(0, 0, max(2, int(radio_x_halo * 1.95 * t)), max(2, int(radio_y_halo * 1.55 * t)))
        ovalo.center = (centro_sombra_x, centro_sombra_y + 2)
        pygame.draw.ellipse(halo_calido, (110, 120, 140, alpha), ovalo)
    halo_piso.blit(halo_calido, (0, 0))
    surf.blit(halo_piso, sombra_rect)

    centro_x = FOG_X - rect.x
    centro_y = FOG_Y - rect.y + 6
    piso_base = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    piso_base.blit(textura, (0, 0))

    # Enfria el bioma completo para que arranque en una paleta nocturna.
    piso_base.fill((155, 165, 178, 255), special_flags=pygame.BLEND_RGBA_MULT)
    velo_frio = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    velo_frio.fill((8, 12, 18, 14))
    piso_base.blit(velo_frio, (0, 0))

    # Capa 1: visibilidad central del bioma alrededor de la fogata.
    piso_visible = piso_base.copy()
    mascara_luz = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    radio_x = max(1, int(rect.w * (0.10 + 0.30 * fogata_ratio)))
    radio_y = max(1, int(rect.h * (0.32 + 0.30 * fogata_ratio)))
    for paso in range(14, 0, -1):
        t = paso / 14
        alpha = int((10 + 245 * fogata_ratio) * (t ** 2.2))
        glow_rect = pygame.Rect(0, 0, max(2, int(radio_x * 2 * t)), max(2, int(radio_y * 2 * t)))
        glow_rect.center = (centro_x, centro_y)
        pygame.draw.ellipse(mascara_luz, (255, 255, 255, alpha), glow_rect)
    piso_visible.blit(mascara_luz, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    # Capa 3: oscuridad encima que vuelve a cubrir lo que no entra en la luz.
    oscuridad = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    oscuridad.fill((3, 5, 9, int(70 + 58 * (1.0 - fogata_ratio))))
    for paso in range(16, 0, -1):
        t = paso / 16
        alpha = int((64 + 55 * (1.0 - fogata_ratio)) * ((1.0 - t) ** 1.3))
        hole_rect = pygame.Rect(0, 0, max(2, int(radio_x * 2.15 * t)), max(2, int(radio_y * 1.75 * t)))
        hole_rect.center = (centro_x, centro_y)
        pygame.draw.ellipse(oscuridad, (0, 0, 0, alpha), hole_rect)
    piso_visible.blit(oscuridad, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    mascara_bordes = obtener_mascara_visibilidad_piso((rect.w, rect.h))
    piso_visible.blit(mascara_bordes, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    surf.blit(piso_visible, rect.topleft)


def dibujar_selector_turfs(surf):
    if not sprites_pisos:
        return

    panel = pygame.Rect(ANCHO // 2 - 230, ALTO - 106, 460, 92)
    fondo = pygame.Surface((panel.w, panel.h), pygame.SRCALPHA)
    fondo.fill((11, 17, 30, 210))
    surf.blit(fondo, panel)
    pygame.draw.rect(surf, (44, 56, 74), panel, 1, border_radius=14)

    for idx, rect in rects_selector_turfs():
        seleccionado = idx == turf_seleccionado_idx
        fill = (38, 54, 79) if seleccionado else (22, 30, 44)
        borde = FUEGO if seleccionado else GRIS_AZUL
        pygame.draw.rect(surf, fill, rect, border_radius=10)
        pygame.draw.rect(surf, borde, rect, 2 if seleccionado else 1, border_radius=10)
        sprite = sprites_pisos[idx]["sprite"]
        sprite_rect = sprite.get_rect(center=(rect.centerx, rect.centery - 2))
        surf.blit(sprite, sprite_rect)

    nombre = sprites_pisos[turf_seleccionado_idx]["nombre"]
    etiqueta = fuente_small.render(f"Turf: {nombre}", True, LUNA)
    ayuda = fuente_small.render("Q/E cambia  •  click selecciona/coloca  •  SPACE coloca en WX  •  F en fogata  •  X borra", True, GRIS_AZUL)
    surf.blit(etiqueta, (panel.x + 14, panel.y + 10))
    surf.blit(ayuda, (panel.x + 14, panel.y + 72))

def dibujar_luz(surf, cx, cy, radio, t):
    osc = pygame.Surface((ANCHO,ALTO),pygame.SRCALPHA)
    osc.fill((*SOMBRA_LUZ, 205))
    ondeo = math.sin(t*3)*6
    for r in range(radio,0,-3):
        alpha = int(205*(1-(r/radio)**0.5))
        pygame.draw.circle(osc,(*SOMBRA_LUZ, alpha),(cx,cy),r+int(ondeo))
    surf.blit(osc,(0,0))


def crear_gota():
    return [
        random.randint(-40, ANCHO + 40),
        random.randint(-ALTO, ALTO),
        random.randint(14, 22),
        random.uniform(520, 700),
    ]


def actualizar_lluvia(gotas, dt):
    for gota in gotas:
        gota[0] -= 160 * dt
        gota[1] += gota[3] * dt
        if gota[1] > ALTO + 30 or gota[0] < -60:
            gota[0] = random.randint(0, ANCHO + 60)
            gota[1] = random.randint(-180, -20)
            gota[2] = random.randint(14, 22)
            gota[3] = random.uniform(520, 700)


def dibujar_lluvia(surf, gotas):
    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    for x, y, largo, _vel in gotas:
        pygame.draw.line(capa, (155, 160, 170, 50), (int(x), int(y)), (int(x - 6), int(y + largo)), 1)
    surf.blit(capa, (0, 0))

def dibujar_barra(surf,x,y,ancho,alto,valor,maximo,color,label):
    pygame.draw.rect(surf,(30,35,55),(x,y,ancho,alto))
    fw = int(ancho*max(0,valor/maximo))
    if fw>0: pygame.draw.rect(surf,color,(x,y,fw,alto))
    pygame.draw.rect(surf,GRIS_AZUL,(x,y,ancho,alto),1)
    surf.blit(fuente_small.render(label,True,LUNA),(x,y-16))

def dibujar_texto_centro(surf,fuente,texto,color,y):
    t = fuente.render(texto,True,color)
    surf.blit(t,(ANCHO//2-t.get_width()//2,y))


cargar_animaciones()
cargar_audio()

# ── WX-78 ────────────────────────────────
class WX78:
    def __init__(self, config):
        self.w,self.h   = 44,52
        self.x          = FOG_X-22
        self.y          = ZONA_Y-26
        self.velocidad  = config["velocidadWx"]
        self.vida       = config["vidaInicial"]
        self.vida_max   = config["vidaMax"]
        self.aturdido   = 0.0
        self.turbo      = 0.0
        self.daño_cd    = 0.0   
        self.invencible = 0.0
        self.direccion  = 1
        self.moviendo   = False
        self.descarga_lluvia = 0.0
        self.item_cargado = []

    def mover(self,keys,dt):
        self.moviendo = False
        if self.aturdido>0: return
        vel = self.velocidad*(1.8 if self.turbo>0 else 1.0)
        mov_x = 0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: mov_x -= vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: mov_x += vel
        self.x += mov_x
        self.moviendo = mov_x != 0
        if mov_x < 0: self.direccion = -1
        elif mov_x > 0: self.direccion = 1
        self.x = max(FOG_X-ZONA_MARGEN, min(FOG_X+ZONA_MARGEN-self.w, self.x))

    def tick(self,dt):
        self.turbo    = max(0,self.turbo-dt)
        self.aturdido = max(0,self.aturdido-dt)
        self.daño_cd  = max(0,self.daño_cd-dt)
        self.invencible = max(0, self.invencible - dt)
        self.descarga_lluvia = max(0, self.descarga_lluvia - dt)

    def activar_descarga_lluvia(self, duracion):
        self.aturdido = max(self.aturdido, duracion)
        self.descarga_lluvia = max(self.descarga_lluvia, duracion)

    def rect(self): return pygame.Rect(self.x,self.y,self.w,self.h)

    def puede_cargar_recurso(self):
        return len(self.item_cargado) < CAPACIDAD_CARGA_WX

    def cargar_recurso(self, tipo):
        if not self.puede_cargar_recurso():
            return False
        self.item_cargado.append(tipo)
        return True

    def descargar_recursos(self):
        recursos = self.item_cargado[:]
        self.item_cargado.clear()
        return recursos

    def dibujar(self,surf,t):
        anim = None
        frame = None
        origen_x = 0
        origen_y = 0
        brillo_lluvia = self.descarga_lluvia > 0
        pulso_lluvia = 0.55 + 0.45 * math.sin(t * 24)

        if self.moviendo and anim_wx_run:
            anim = anim_wx_run
            frame = anim.obtener_frame(t)
        elif self.aturdido > 0 and anim_wx_idle:
            anim = anim_wx_idle
            frame = anim.obtener_frame(t)
        elif anim_wx_idle and anim_wx_idle.frames:
            anim = anim_wx_idle
            frame = anim_wx_idle.frames[0]

        if anim and frame is not None:
            if self.direccion < 0:
                frame = pygame.transform.flip(frame, True, False)
                origen_x = frame.get_width() - anim.origin[0]
            else:
                origen_x = anim.origin[0]
            origen_y = anim.origin[1]
            anchor_x = self.x + self.w // 2
            anchor_y = self.y + self.h + WX_OFFSET_Y
            draw_pos = (int(anchor_x - origen_x), int(anchor_y - origen_y))

            if brillo_lluvia:
                glow_margin = 18
                glow_rect = pygame.Rect(
                    draw_pos[0] - glow_margin,
                    draw_pos[1] - glow_margin,
                    frame.get_width() + glow_margin * 2,
                    frame.get_height() + glow_margin * 2,
                )
                aura = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
                aura_alpha = int(45 + 55 * pulso_lluvia)
                pygame.draw.ellipse(aura, (110, 210, 255, aura_alpha), aura.get_rect())
                surf.blit(aura, glow_rect.topleft)
            surf.blit(frame, draw_pos)

            if brillo_lluvia:
                flash = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
                flash.fill((210, 245, 255, int(70 + 55 * pulso_lluvia)))
                surf.blit(flash, draw_pos)
            elif self.aturdido > 0:
                flash = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
                flash.fill((220,100,100,55))
                surf.blit(flash, draw_pos)

            if self.turbo > 0:
                aura=pygame.Surface((self.w+20,self.h+20),pygame.SRCALPHA)
                pygame.draw.rect(aura,(80,180,255,45),(0,0,self.w+20,self.h+20),border_radius=10)
                surf.blit(aura,(self.x-10,self.y-10))
            return

        col = LUNA
        if self.aturdido>0: col=(220,100,100)
        if brillo_lluvia:   col=BLANCO_FR
        if self.turbo>0:    col=ELECTRICO
        b = int(180+60*math.sin(t*4))
        if brillo_lluvia:
            aura=pygame.Surface((self.w+28,self.h+28),pygame.SRCALPHA)
            pygame.draw.rect(
                aura,
                (110,210,255,int(55 + 45 * pulso_lluvia)),
                (0,0,self.w+28,self.h+28),
                border_radius=12,
            )
            surf.blit(aura,(self.x-14,self.y-14))
        pygame.draw.rect(surf,(40,50,70),(self.x+4,self.y+20,36,28),border_radius=4)
        pygame.draw.rect(surf,col,       (self.x+4,self.y+20,36,28),2,border_radius=4)
        pygame.draw.rect(surf,(40,50,70),(self.x+7,self.y+2,30,20),border_radius=3)
        pygame.draw.rect(surf,col,       (self.x+7,self.y+2,30,20),2,border_radius=3)
        oc = ELECTRICO if self.turbo>0 or brillo_lluvia else (b,b,80)
        pygame.draw.circle(surf,oc,(self.x+15,self.y+11),5)
        pygame.draw.circle(surf,oc,(self.x+29,self.y+11),5)
        pygame.draw.rect(surf,col,(self.x+7, self.y+48,11,5),border_radius=2)
        pygame.draw.rect(surf,col,(self.x+26,self.y+48,11,5),border_radius=2)
        if self.turbo>0:
            aura=pygame.Surface((self.w+16,self.h+16),pygame.SRCALPHA)
            pygame.draw.rect(aura,(80,180,255,40),(0,0,self.w+16,self.h+16),border_radius=8)
            surf.blit(aura,(self.x-8,self.y-8))

# ── OBJETO QUE CAE ───────────────────────
class Objeto:
    def __init__(self,nivel):
        config = config_dificultad()
        # engranes disponibles desde noche 1
        tipos  = ["leña","carbon","engrane","rayo"]
        if lluvia_activa():
            pesos = [30, 20, 15, 35 if nivel>=2 else 0]  # más probabilidad de rayos con lluvia
        else:
            pesos = [45, 30, 18, 7 if nivel>=2 else 0]
        self.tipo = random.choices(tipos,weights=pesos)[0]
        sizes = {"leña":SPRITE_SIZES["leña"],"carbon":SPRITE_SIZES["carbon"],"engrane":SPRITE_SIZES["engrane"],"rayo":(18,32)}
        self.w,self.h = sizes[self.tipo]
        self.x = random.randint(FOG_X-ZONA_MARGEN, FOG_X+ZONA_MARGEN-self.w)
        self.y = -self.h
        self.vel = (random.uniform(2.5,4.0)+nivel*0.25) * config["velObjetos"]
        self.t = 0.0

    def actualizar(self,dt):
        self.y += self.vel
        self.t += dt

    def rect(self): return pygame.Rect(self.x,self.y,self.w,self.h)
    def fuera(self): return self.y>ALTO+10

    def dibujar(self,surf):
        cx=self.x+self.w//2; cy=self.y+self.h//2
        if self.tipo=="leña":
            sprite = sprites_objetos.get("leña")
            if sprite:
                rect = sprite.get_rect(center=(cx, cy))
                surf.blit(sprite, rect)
            else:
                pygame.draw.rect(surf,(100,60,20),(self.x,self.y+4,self.w,self.h-8),border_radius=3)
                pygame.draw.rect(surf,(140,90,40),(self.x,self.y+4,self.w,self.h-8),1,border_radius=3)
                pygame.draw.line(surf,(80,40,10),(self.x+6,cy),(self.x+self.w-6,cy),1)
        elif self.tipo=="carbon":
            sprite = sprites_objetos.get("carbon")
            if sprite:
                rect = sprite.get_rect(center=(cx, cy))
                surf.blit(sprite, rect)
            else:
                pygame.draw.rect(surf,(50,50,60),(self.x+2,self.y+2,self.w-4,self.h-4),border_radius=4)
                pygame.draw.rect(surf,(90,90,110),(self.x+2,self.y+2,self.w-4,self.h-4),1,border_radius=4)
                pygame.draw.circle(surf,(80,80,100),(self.x+8,self.y+7),3)
        elif self.tipo=="engrane":
            sprite = sprites_objetos.get("engrane")
            if sprite:
                rotado = pygame.transform.rotate(sprite, self.t * 90)
                rect = rotado.get_rect(center=(cx, cy))
                surf.blit(rotado, rect)
            else:
                pygame.draw.circle(surf,(140,140,160),(cx,cy),12)
                pygame.draw.circle(surf,(180,180,200),(cx,cy),12,2)
                pygame.draw.circle(surf,(40,50,70),(cx,cy),5)
                for ang in range(0,360,45):
                    rad=math.radians(ang+self.t*60)
                    pygame.draw.circle(surf,(180,180,200),
                        (cx+int(13*math.cos(rad)),cy+int(13*math.sin(rad))),3)
        elif self.tipo=="rayo":
            pulso=int(3*math.sin(self.t*10))
            pts=[(cx,self.y),(cx+8,cy-4),(cx+3,cy-4),
                 (cx+10,self.y+self.h),(cx-2,cy+2),(cx+3,cy+2)]
            pygame.draw.polygon(surf,(80,180,255),pts)
            pygame.draw.polygon(surf,(200,230,255),pts,1)
            glow=pygame.Surface((self.w+10,self.h+10),pygame.SRCALPHA)
            pygame.draw.ellipse(glow,(80,180,255,40+pulso*5),(0,0,self.w+10,self.h+10))
            surf.blit(glow,(self.x-5,self.y-5))

# ── GARRA ────────────────────────────────
class Garra:
    def __init__(self,nivel):
        config = config_dificultad()
        self.desde_izq = random.choice([True,False])
        self.w,self.h  = 50,40
        self.y = ZONA_Y+random.randint(-30,30)-self.h//2
        self.t = 0.0
        self.fase       = "lenta"
        self.fase_timer = 0.0
        self.vel_lenta  = (0.6+nivel*0.05) * config["velGarras"]
        self.vel_rapida = (3.5+nivel*0.4) * config["velGarras"]
        self.velocidad  = self.vel_lenta
        self.espantada  = False
        # daño que hace al tocar a WX
        self.daño_contacto = max(1, int(round((10 + nivel*2) * config["dañoGarras"])))
        self.daño_fogata = config["dañoFogataGarra"]
        if self.desde_izq: self.x,self.dir = -self.w, 1
        else:              self.x,self.dir = ANCHO,   -1

    def actualizar(self,dt):
        self.t += dt
        if not self.espantada:
            self.fase_timer += dt
            if self.fase=="lenta" and self.fase_timer>=2.0:
                self.fase="rapida"; self.velocidad=self.vel_rapida
            self.x += self.dir*self.velocidad
        else:
            self.x -= self.dir*9

    def rect(self): return pygame.Rect(self.x,self.y,self.w,self.h)

    def llego_fogata(self):
        if self.desde_izq: return self.x+self.w>=FOG_X-20
        else:              return self.x<=FOG_X+20

    def fuera(self): return self.x<-self.w-120 or self.x>ANCHO+120

    def dibujar(self,surf):
        cx=self.x+self.w//2; cy=self.y+self.h//2
        pulso=math.sin(self.t*8)*3
        if self.espantada:       cb,co=(180,100,200),(220,160,255)
        elif self.fase=="rapida": cb,co=(120,10,10),(220,40,40)
        else:                    cb,co=(60,20,80),(140,60,180)

        aura=pygame.Surface((104,104),pygame.SRCALPHA)
        pygame.draw.circle(aura,(*cb,36),(52,52),28+int(abs(pulso)))
        pygame.draw.circle(aura,(*co,24),(52,52),20+int(abs(pulso)))
        surf.blit(aura,(cx-52,cy-52))

        if anim_garra:
            frame = anim_garra.obtener_frame(self.t)
            if frame is not None:
                angulo = -90 if self.desde_izq else 90
                frame = pygame.transform.rotate(frame, angulo)
                # La garra animada no queda centrada tras rotarla; este ajuste
                # hace que lo visible coincida mejor con la colision.
                offset_x, offset_y = GARRA_OFFSET_IZQ if self.desde_izq else GARRA_OFFSET_DER
                frame_rect = frame.get_rect(center=(cx + offset_x, cy + offset_y))
                surf.blit(frame, frame_rect)
                pygame.draw.ellipse(surf,co,frame_rect.inflate(12,8),1)
            else:
                pygame.draw.ellipse(surf,cb,(self.x+8,self.y+10,34,22))
                pygame.draw.ellipse(surf,co,(self.x+8,self.y+10,34,22),1)
        else:
            pygame.draw.ellipse(surf,cb,(self.x+8,self.y+10,34,22))
            pygame.draw.ellipse(surf,co,(self.x+8,self.y+10,34,22),1)
            for i in range(4):
                oy=self.y+6+i*9+int(pulso*(1 if i%2==0 else -1))
                largo=18+int(pulso)
                if self.desde_izq:
                    pygame.draw.line(surf,co,(self.x+self.w-8,oy),(self.x+self.w-8+largo,oy+3),2)
                else:
                    pygame.draw.line(surf,co,(self.x+8,oy),(self.x+8-largo,oy+3),2)
            pygame.draw.circle(surf,(100,40,130),(cx,cy),6)

        if self.fase=="rapida" and not self.espantada:
            av=fuente_small.render("!",True,(220,40,40))
            surf.blit(av,(cx-4,self.y-16))

# ── SOMBRA LATERAL ───────────────────────
class Sombra:
    def __init__(self,nivel):
        config = config_dificultad()
        self.desde_izq = random.choice([True,False])
        self.w,self.h  = 40,50
        self.vel       = (0.4+nivel*0.08) * config["velSombras"]
        self.y         = ZONA_Y+random.randint(-30,30)-self.h//2
        self.t         = 0.0
        self.daño_cd   = 0.0
        self.radio_daño= 70
        self.daño_contacto = max(1, int(round(8 * config["dañoSombras"])))
        self.daño_fogata = config["dañoFogataSombra"]
        self.x = -self.w if self.desde_izq else ANCHO
        self.dir = 1 if self.desde_izq else -1

    def actualizar(self,dt):
        self.t += dt
        self.daño_cd = max(0,self.daño_cd-dt)
        self.x += self.dir*self.vel
      

    def rect(self): return pygame.Rect(self.x,self.y,self.w,self.h)
    def cerca_de(self,wx_rect):
        return abs((self.x+self.w//2)-(wx_rect.x+wx_rect.width//2))<self.radio_daño
    def fuera(self): return self.x<-self.w-20 or self.x>ANCHO+20

    def dibujar(self,surf):
        cx=self.x+self.w//2; cy=self.y+self.h//2
        pulso=int(4*math.sin(self.t*4))
        pts=[(cx,self.y-pulso),(self.x+self.w,self.y+self.h//3),
             (self.x+self.w,self.y+self.h*2//3),(cx,self.y+self.h+pulso),
             (self.x,self.y+self.h*2//3),(self.x,self.y+self.h//3)]
        pygame.draw.polygon(surf,(25,10,40),pts)
        pygame.draw.polygon(surf,(80,30,110),pts,1)
        pygame.draw.circle(surf,(180,80,220),(cx-8,cy-4),4)
        pygame.draw.circle(surf,(180,80,220),(cx+8,cy-4),4)
        pygame.draw.circle(surf,(255,150,255),(cx-8,cy-4),2)
        pygame.draw.circle(surf,(255,150,255),(cx+8,cy-4),2)
        aura=pygame.Surface((self.radio_daño*2,self.radio_daño*2),pygame.SRCALPHA)
        alpha=int(20+10*math.sin(self.t*3))
        pygame.draw.circle(aura,(150,50,200,alpha),(self.radio_daño,self.radio_daño),self.radio_daño)
        surf.blit(aura,(cx-self.radio_daño,cy-self.radio_daño))

# ── ESTADO GLOBAL ────────────────────────
MENU="menu"; JUGANDO="jugando"; GAME_OVER="game_over"; VICTORIA="victoria"
OPCION_DIFICULTAD = 2
OPCION_TURF = 3
estado=MENU; seleccionado=0; timer=0.0; modo_endless=False
dificultad_idx = 1
dificultad_actual = DIFICULTAD_NOMBRES[dificultad_idx]
opciones=["Modo Normal","Modo Endless","Dificultad","Turf","Salir"]

wx=None; objetos=[]; garras=[]; sombras=[]; mensajes=[]
fogata=100.0; fogata_max=100.0; puntaje=0; nivel=1
spawn_timer=0.0;  spawn_intervalo=2.0
garra_timer=0.0;  garra_intervalo=5.0
sombra_timer=0.0; sombra_intervalo=8.0
noche_actual=1;   noche_timer=0.0
noche_duracion=30.0; noches_normal=5
lluvia=[]; lluvia_daño_timer=0.0; lluvia_stun_timer=0.0
locura_sonido_timer=0.0
pasos_wx_timer=0.0


def config_dificultad():
    return DIFICULTADES[dificultad_actual]


def cambiar_dificultad(delta):
    global dificultad_idx, dificultad_actual
    dificultad_idx = (dificultad_idx + delta) % len(DIFICULTAD_NOMBRES)
    dificultad_actual = DIFICULTAD_NOMBRES[dificultad_idx]

def agregar_msg(texto,x,y,color=LUNA):
    mensajes.append([texto,float(x),float(y),1.2,color])


def rect_fogata_colision():
    return pygame.Rect(FOG_X - 30, FOG_Y - 30, 60, 60)


def aplicar_recurso_fogata(tipo, x, y):
    global fogata, puntaje
    if tipo=="leña":
        fogata=min(fogata_max,fogata+25); puntaje+=10
        reproducir_sonido("fogata_leña")
        agregar_msg("+25 🔥",x,y,NARANJA)
        return True
    if tipo=="carbon":
        fogata=min(fogata_max,fogata+40); puntaje+=20
        reproducir_sonido("fogata_carbon")
        agregar_msg("+40 🔥",x,y,AMBAR)
        return True
    return False

def iniciar_juego(endless):
    global wx,objetos,garras,sombras,fogata,fogata_max,puntaje,nivel,mensajes
    global spawn_timer,spawn_intervalo,garra_timer,garra_intervalo
    global sombra_timer,sombra_intervalo,noche_actual,noche_timer,modo_endless
    global noche_duracion,noches_normal,lluvia,lluvia_daño_timer,lluvia_stun_timer,locura_sonido_timer,pasos_wx_timer
    config = config_dificultad()
    wx=WX78(config); objetos=[]; garras=[]; sombras=[]; mensajes=[]
    fogata_max=config["fogataMax"]
    fogata=config["fogataInicial"]; puntaje=0; nivel=1
    spawn_timer=0.0;  spawn_intervalo=config["spawnObjetosInicial"]
    garra_timer=0.0;  garra_intervalo=config["spawnGarrasInicial"]
    sombra_timer=0.0; sombra_intervalo=config["spawnSombrasInicial"]
    noche_actual=1;   noche_timer=0.0
    noche_duracion=config["nocheDuracion"]
    noches_normal=config["nochesNormal"]
    modo_endless=endless
    lluvia=[crear_gota() for _ in range(config["lluviaCantidad"])]
    lluvia_daño_timer=0.0
    lluvia_stun_timer=0.0
    locura_sonido_timer=0.0
    pasos_wx_timer=0.0


def lluvia_activa():
    return noche_actual >= config_dificultad()["lluviaDesdeNoche"]


def murmullos_activos():
    if fogata_max <= 0:
        return False
    vida_baja = wx is not None and wx.vida_max > 0 and (wx.vida / wx.vida_max) <= 0.45
    fogata_baja = (fogata / fogata_max) <= 0.35
    return vida_baja or fogata_baja

# ── LOOP ─────────────────────────────────
while True:
    dt = reloj.tick(60)/1000
    timer += dt

    for evento in pygame.event.get():
        if evento.type==pygame.QUIT:
            pygame.quit(); sys.exit()
        if evento.type==pygame.KEYDOWN:
            if estado==MENU:
                if evento.key==pygame.K_UP:
                    seleccionado=(seleccionado-1)%len(opciones)
                    reproducir_sonido("menu_mover")
                if evento.key==pygame.K_DOWN:
                    seleccionado=(seleccionado+1)%len(opciones)
                    reproducir_sonido("menu_mover")
                if seleccionado==OPCION_DIFICULTAD and evento.key in (pygame.K_LEFT, pygame.K_a):
                    cambiar_dificultad(-1)
                    reproducir_sonido("menu_mover")
                if seleccionado==OPCION_DIFICULTAD and evento.key in (pygame.K_RIGHT, pygame.K_d):
                    cambiar_dificultad(1)
                    reproducir_sonido("menu_mover")
                if seleccionado==OPCION_TURF and evento.key in (pygame.K_LEFT, pygame.K_a):
                    seleccionar_turf(-1)
                    reproducir_sonido("menu_mover")
                if seleccionado==OPCION_TURF and evento.key in (pygame.K_RIGHT, pygame.K_d):
                    seleccionar_turf(1)
                    reproducir_sonido("menu_mover")
                if evento.key==pygame.K_RETURN:
                    reproducir_sonido("menu_aceptar")
                    if opciones[seleccionado]=="Salir":
                        pygame.quit(); sys.exit()
                    elif opciones[seleccionado]=="Modo Normal":
                        iniciar_juego(False); estado=JUGANDO
                    elif opciones[seleccionado]=="Modo Endless":
                        iniciar_juego(True); estado=JUGANDO
                    else:
                        if seleccionado == OPCION_DIFICULTAD:
                            cambiar_dificultad(1)
                        elif seleccionado == OPCION_TURF:
                            seleccionar_turf(1)
            elif estado in (GAME_OVER,VICTORIA):
                if evento.key==pygame.K_RETURN:
                    reproducir_sonido("menu_aceptar")
                    estado=MENU

    if estado==JUGANDO:
        config = config_dificultad()
        reproducir_musica("juego", 0.85)
        keys=pygame.key.get_pressed()
        wx.mover(keys,dt)
        wx.tick(dt)
        lluvia_daño_timer=max(0, lluvia_daño_timer-dt)
        lluvia_stun_timer=max(0, lluvia_stun_timer-dt)
        locura_sonido_timer=max(0, locura_sonido_timer-dt)
        pasos_wx_timer=max(0, pasos_wx_timer-dt)

        reproducir_loop("fogata_loop_1", "fogata_1")
        reproducir_loop("fogata_loop_2", "fogata_2")
        reproducir_loop("fogata_loop_3", "fogata_3")

        # fogata se consume más rápido con el tiempox
        fogata=max(0,fogata-(3.0+nivel*0.4)*config["consumoFogata"]*dt)

        if murmullos_activos() and locura_sonido_timer<=0:
            reproducir_sonido("locura")
            vida_ratio = (wx.vida / wx.vida_max) if wx and wx.vida_max > 0 else 1.0
            fogata_ratio = fogata / max(1.0, fogata_max)
            critico = min(vida_ratio, fogata_ratio)
            locura_sonido_timer = 2.1 if critico <= 0.2 else 3.2

        if wx.moviendo and wx.aturdido <= 0 and pasos_wx_timer <= 0:
            reproducir_pasos_wx()
            pasos_wx_timer = 0.05 if wx.turbo > 0 else 0.1

        fog_rect = rect_fogata_colision()
        if wx.rect().colliderect(fog_rect) and wx.item_cargado:
            recursos_entregados = wx.descargar_recursos()
            for recurso in recursos_entregados:
                aplicar_recurso_fogata(recurso, FOG_X, FOG_Y - 40)

        if lluvia_activa():
            reproducir_loop("lluvia_loop", "lluvia")
            actualizar_lluvia(lluvia, dt)
            if wx.invencible<=0 and lluvia_daño_timer<=0:
                daño_lluvia = config["lluviaDaño"] / 2 if wx.turbo>0 else config["lluviaDaño"]
                if daño_lluvia > 0:
                    wx.vida=max(0,wx.vida-daño_lluvia)
                    lluvia_daño_timer=config["lluviaCd"]
                    if lluvia_stun_timer<=0:
                        wx.activar_descarga_lluvia(LLUVIA_STUN_DURACION)
                        lluvia_stun_timer=LLUVIA_STUN_CD
                    reproducir_lluvia_wx()
                    agregar_msg(f"-{daño_lluvia:g} ❤ LLUVIA",wx.x-6,wx.y-28,ELECTRICO)
        else:
            detener_loop("lluvia")

        # spawn objetos
        spawn_timer+=dt
        if spawn_timer>=spawn_intervalo:
            spawn_timer=0
            objetos.append(Objeto(nivel))
            spawn_intervalo=max(config["spawnObjetosMin"],spawn_intervalo-config["spawnObjetosPaso"])

        # spawn garras
        garra_timer+=dt
        if garra_timer>=garra_intervalo:
            garra_timer=0
            # noche 3+ pueden salir 2 garras a la vez
            cantidad_garras = 2 if nivel>=3 and random.random()<config["garrasDoblesProb"] else 1
            for _ in range(cantidad_garras):
                garras.append(Garra(nivel))
            reproducir_sonido("garra_aparece")
            garra_intervalo=max(config["spawnGarrasMin"],garra_intervalo-config["spawnGarrasPaso"])

        # spawn sombras — desde noche 2, más cantidad con el tiempo
        sombra_timer+=dt
        if nivel>=config["sombrasDesdeNivel"] and sombra_timer>=sombra_intervalo:
            sombra_timer=0
            max_sombras = min(config["sombrasMaximas"], 1 + max(0, nivel - config["sombrasDesdeNivel"]))
            for _ in range(random.randint(1, max_sombras)):
                sombras.append(Sombra(nivel))
            sombra_intervalo=max(config["spawnSombrasMin"],sombra_intervalo-config["spawnSombrasPaso"])

        # objetos
        for obj in objetos[:]:
            obj.actualizar(dt)
            if obj.rect().colliderect(wx.rect()):
                if obj.tipo=="leña":
                    if wx.cargar_recurso("leña"):
                        agregar_msg(f"Leña {len(wx.item_cargado)}/{CAPACIDAD_CARGA_WX}",obj.x,obj.y,NARANJA)
                        objetos.remove(obj)
                elif obj.tipo=="carbon":
                    if wx.cargar_recurso("carbon"):
                        agregar_msg(f"Carbon {len(wx.item_cargado)}/{CAPACIDAD_CARGA_WX}",obj.x,obj.y,AMBAR)
                        objetos.remove(obj)
                elif obj.tipo=="engrane":
                    wx.vida=min(wx.vida_max,wx.vida+25); puntaje+=15
                    reproducir_engrane_wx()
                    agregar_msg("+25 ❤",obj.x,obj.y,VERDE)
                    objetos.remove(obj)
                elif obj.tipo=="rayo":
                    wx.turbo=4.0
                    wx.invencible=4.0
                    puntaje+=10
                    agregar_msg("⚡ TURBO + INVENCIBLE",obj.x,obj.y,ELECTRICO)
                    agregar_msg("⚡ TURBO",obj.x,obj.y,ELECTRICO)
                    objetos.remove(obj)
            elif obj.fuera():
                objetos.remove(obj)

        # garras — tocarlas las espanta PERO hacen daño a WX
        for g in garras[:]:
            g.actualizar(dt)
            if not g.espantada and g.rect().colliderect(wx.rect()):
                g.espantada=True
                puntaje+=15
                # daño al espantar — menos si tiene turbo
                if wx.daño_cd<=0 and wx.invencible<=0:
                    daño = g.daño_contacto//2 if wx.turbo>0 else g.daño_contacto
                    wx.vida=max(0,wx.vida-daño)
                    wx.daño_cd=0.5
                    wx.aturdido=0.3
                    reproducir_golpe_wx()
                    agregar_msg(f"-{daño} ❤",wx.x,wx.y-20,(220,80,80))
                    agregar_msg("¡Espantada!",g.x,g.y-20,(180,100,220))
            if not g.espantada and g.llego_fogata():
                fogata=max(0,fogata-g.daño_fogata)
                reproducir_sonido("garra_muerde")
                agregar_msg(f"-{g.daño_fogata} 🔥",FOG_X,FOG_Y-40,(220,80,80))
                garras.remove(g); continue
            if g.fuera(): garras.remove(g)

        # sombras
        # sombras
        for s in sombras[:]:
            s.actualizar(dt)
            if s not in sombras:
                continue
            # toca a WX
            if s.rect().colliderect(wx.rect()):
                if wx.invencible<=0:
                    wx.vida=max(0,wx.vida-s.daño_contacto)
                    wx.aturdido=0.4
                    reproducir_golpe_wx("sombra")
                    agregar_msg(f"-{s.daño_contacto} ❤",wx.x,wx.y-20,(220,80,80))
                sombras.remove(s)
                continue
            # llega a la fogata
            if s.rect().colliderect(fog_rect):
                fogata=max(0,fogata-s.daño_fogata)
                agregar_msg(f"-{s.daño_fogata} 🔥",FOG_X,FOG_Y-40,(220,80,80))
                sombras.remove(s)
                continue
            if s.fuera():
                sombras.remove(s)


        # mensajes flotantes
        for m in mensajes[:]:
            m[2]-=40*dt; m[3]-=dt
            if m[3]<=0: mensajes.remove(m)

        # noche
        noche_timer+=dt
        if noche_timer>=noche_duracion:
            noche_timer=0; noche_actual+=1; nivel+=1
            if not modo_endless and noche_actual>noches_normal:
                estado=VICTORIA

        if fogata<=0 or wx.vida<=0:
            estado=GAME_OVER
            detener_loop("fogata_1")
            detener_loop("fogata_2")
            detener_loop("fogata_3")
            detener_loop("lluvia")
    else:
        pasos_wx_timer = 0.0
        if estado == MENU:
            reproducir_musica("menu", 0.32)
        else:
            detener_musica()
        if estado in (MENU, VICTORIA):
            reproducir_loop("fogata_loop_1", "fogata_1")
            reproducir_loop("fogata_loop_2", "fogata_2")
            reproducir_loop("fogata_loop_3", "fogata_3")
        else:
            detener_loop("fogata_1")
            detener_loop("fogata_2")
            detener_loop("fogata_3")
        detener_loop("lluvia")

    # ── DIBUJAR ──────────────────────────
    centro_estrellas = None
    radio_estrellas = 0
    if estado==MENU:
        centro_estrellas = (ANCHO//2, ALTO//2+60)
        radio_estrellas = 160
    elif estado==JUGANDO:
        centro_estrellas = (FOG_X, FOG_Y)
        radio_estrellas = int(45 + (fogata / fogata_max) * 90)
    elif estado==GAME_OVER:
        centro_estrellas = (ANCHO//2, ALTO//2)
        radio_estrellas = 40
    elif estado==VICTORIA:
        centro_estrellas = (ANCHO//2, ALTO//2)
        radio_estrellas = 200

    if estado == JUGANDO:
        dibujar_fondo_juego(pantalla, timer)
    else:
        pantalla.fill(NEGRO)

    if estado==MENU:
        dibujar_estrellas(pantalla,timer,centro_estrellas,radio_estrellas)
        t1=fuente_titulo.render("Lights Out",True,BLANCO_FR)
        dibujar_fogata(pantalla,ANCHO//2,ALTO//2+60,timer)
        s1=fuente_titulo.render("Lights Out",True,(20,25,45))
        pantalla.blit(s1,(ANCHO//2-t1.get_width()//2+2,72))
        pantalla.blit(t1,(ANCHO//2-t1.get_width()//2,  70))
        dibujar_texto_centro(pantalla,fuente_sub,"La Prisión de Charlie  ·  WX-78",GRIS_AZUL,148)
        pygame.draw.line(pantalla,AZUL_MID,(ANCHO//2-120,178),(ANCHO//2+120,178),1)
        for i,texto in enumerate(opciones):
            y_op=300+i*52; es=(i==seleccionado)
            texto_menu = texto
            if texto=="Dificultad":
                texto_menu = f"Dificultad: < {dificultad_actual} >"
            elif texto=="Turf":
                texto_menu = f"Turf: < {turf_actual()} >"
            if es:
                rb=pygame.Rect(ANCHO//2-180,y_op-6,360,38)
                fo=pygame.Surface((360,38),pygame.SRCALPHA)
                fo.fill((31,45,74,80)); pantalla.blit(fo,rb)
                pygame.draw.rect(pantalla,AZUL_MID,rb,1)
                pantalla.blit(fuente_menu.render("✦",True,NARANJA),(ANCHO//2-145,y_op))
                ctxt=FUEGO if texto!="Salir" else (200,80,80)
            else:
                ctxt=LUNA if texto!="Salir" else GRIS_AZUL
            ts=fuente_menu.render(texto_menu,True,ctxt)
            pantalla.blit(ts,(ANCHO//2-ts.get_width()//2,y_op))
        preview_rect = pygame.Rect(ANCHO//2 - 170, ALTO - 110, 340, 42)
        pantalla.blit(obtener_superficie_turf(turf_actual(), (preview_rect.w, preview_rect.h)), preview_rect.topleft)
        pygame.draw.rect(pantalla, AZUL_MID, preview_rect, 1, border_radius=10)
        dibujar_texto_centro(pantalla,fuente_small,"↑ ↓ mover   ← → cambiar opción   ENTER aceptar",(50,65,90),ALTO-28)

    elif estado==JUGANDO:
        radio_luz=radio_estrellas
        
        if lluvia_activa():
            velo=pygame.Surface((ANCHO,ALTO),pygame.SRCALPHA)
            velo.fill((18, 28, 46, 12))
            pantalla.blit(velo,(0,0))
        dibujar_pisos(pantalla)
        dibujar_props_campamento(pantalla, FOG_X, FOG_Y, timer)
        dibujar_fogata(pantalla,FOG_X,FOG_Y,timer)
        for obj in objetos: obj.dibujar(pantalla)
        for g   in garras:  g.dibujar(pantalla)
        for s   in sombras: s.dibujar(pantalla)
        wx.dibujar(pantalla,timer)
        if lluvia_activa():
            dibujar_lluvia(pantalla, lluvia)
        for m in mensajes:
            txt=fuente_small.render(m[0],True,m[4])
            txt.set_alpha(int(255*min(1,m[3])))
            pantalla.blit(txt,(int(m[1]),int(m[2])))
        dibujar_barra(pantalla,20,36,200,16,fogata,fogata_max,NARANJA,"🔥 FOGATA")
        dibujar_barra(pantalla,20,76,200,16,wx.vida,wx.vida_max,(80,180,100),"❤ VIDA")
        if wx.turbo>0:
            dibujar_barra(pantalla,20,116,200,10,wx.turbo,4.0,ELECTRICO,"⚡ TURBO")
        carga_y = 142 if wx.turbo > 0 else 116
        carga_texto = ", ".join(wx.item_cargado) if wx.item_cargado else "vacia"
        carga_color = LUNA if wx.item_cargado else GRIS_AZUL
        carga = fuente_small.render(
            f"Carga {len(wx.item_cargado)}/{CAPACIDAD_CARGA_WX}: {carga_texto}",
            True,
            carga_color,
        )
        pantalla.blit(carga,(20,carga_y))
        pts=fuente_hud.render(f"Puntos: {puntaje}",True,LUNA)
        pantalla.blit(pts,(ANCHO-pts.get_width()-20,20))
        dif=fuente_small.render(f"Dificultad: {dificultad_actual}",True,GRIS_AZUL)
        pantalla.blit(dif,(ANCHO-dif.get_width()-20,48))
        if not modo_endless:
            nt=fuente_hud.render(f"Noche {noche_actual} / {noches_normal}",True,GRIS_AZUL)
        else:
            nt=fuente_hud.render(f"Noche {noche_actual}  •  ENDLESS",True,(120,60,60))
        pantalla.blit(nt,(ANCHO//2-nt.get_width()//2,16))
        prog=noche_timer/noche_duracion
        pygame.draw.rect(pantalla,(30,35,55),(ANCHO//2-100,38,200,6))
        pygame.draw.rect(pantalla,AZUL_MID,(ANCHO//2-100,38,int(200*prog),6))
        pygame.draw.rect(pantalla,GRIS_AZUL,(ANCHO//2-100,38,200,6),1)

    elif estado==GAME_OVER:
        dibujar_estrellas(pantalla,timer,centro_estrellas,radio_estrellas)
        causa="La fogata se apagó..." if fogata<=0 else "WX-78 cayó..."
        dibujar_texto_centro(pantalla,fuente_grande,"Charlie ganó.",(160,40,40),ALTO//2-80)
        dibujar_texto_centro(pantalla,fuente_sub,causa,GRIS_AZUL,ALTO//2-10)
        dibujar_texto_centro(pantalla,fuente_sub,f"Puntos: {puntaje}",LUNA,ALTO//2+30)
        dibujar_texto_centro(pantalla,fuente_small,f"Dificultad: {dificultad_actual}",GRIS_AZUL,ALTO//2+58)
        dibujar_texto_centro(pantalla,fuente_small,"ENTER para volver al menú",(50,65,90),ALTO//2+80)

    elif estado==VICTORIA:
        dibujar_estrellas(pantalla,timer,centro_estrellas,radio_estrellas)
        dibujar_fogata(pantalla,ANCHO//2,ALTO//2+40,timer)
        dibujar_texto_centro(pantalla,fuente_grande,"WX-78 sobrevivió.",FUEGO,ALTO//2-100)
        dibujar_texto_centro(pantalla,fuente_sub,"Los supervivientes han llegado.",LUNA,ALTO//2-30)
        dibujar_texto_centro(pantalla,fuente_sub,f"Puntos: {puntaje}",AMBAR,ALTO//2+20)
        dibujar_texto_centro(pantalla,fuente_small,f"Dificultad: {dificultad_actual}",GRIS_AZUL,ALTO//2+48)
        dibujar_texto_centro(pantalla,fuente_small,"ENTER para volver",(50,65,90),ALTO//2+80)

    pygame.display.flip()
