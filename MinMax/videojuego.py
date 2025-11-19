#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTHELLO / REVERSI - Pygame GUI Moderna + IA (Minimax con dificultad adaptativa)
Desarrollado por: RJL08
"""
import pygame
import sys
import time
import math
import random
import threading
from typing import List, Tuple, Optional, Dict

# ---------- Configuración ----------
TAMAÑO_TABLERO = 8
CASILLA = 75  # Tamaño de cada casilla
MARGEN_SUPERIOR = 180  # Espacio para header
MARGEN_LATERAL = 160  # Espacio lateral mejorado
ANCHO = TAMAÑO_TABLERO * CASILLA + MARGEN_LATERAL * 2
ALTO = TAMAÑO_TABLERO * CASILLA + MARGEN_SUPERIOR + 120
FPS = 60

# Jugadores
VACIO = 0
NEGRO = 1
BLANCO = 2

# Paleta de colores moderna
FONDO = (26, 32, 44)
VERDE_TABLERO = (34, 139, 34)
GRID = (25, 111, 25)
FONDO_TARJETA = (45, 55, 72)
TEXTO = (247, 250, 252)
TEXTO_SECUNDARIO = (160, 174, 192)
ACENTO = (66, 153, 225)
ACENTO_HOVER = (49, 130, 206)
EXITO = (72, 187, 120)
ADVERTENCIA = (237, 137, 54)
PELIGRO = (245, 101, 101)
COLOR_NEGRO = (20, 20, 20)
COLOR_BLANCO = (245, 245, 245)
SOMBRA = (0, 0, 0, 40)

# Parámetros IA
PROFUNDIDAD_MAX_INICIO = 1
PROFUNDIDAD_MAX_MEDIO = 2
PROFUNDIDAD_MAX_FINAL = 3
LIMITE_TIEMPO = 0.8

# Direcciones para búsqueda
DIRECCIONES = [(-1, -1), (-1, 0), (-1, 1),
               (0, -1), (0, 1),
               (1, -1), (1, 0), (1, 1)]


# ---------- Lógica del juego ----------

def inicializar_tablero() -> List[List[int]]:
    """Crea el tablero inicial con las 4 fichas centrales"""
    tablero = [[VACIO] * TAMAÑO_TABLERO for _ in range(TAMAÑO_TABLERO)]
    mitad = TAMAÑO_TABLERO // 2
    tablero[mitad - 1][mitad - 1] = BLANCO
    tablero[mitad][mitad] = BLANCO
    tablero[mitad - 1][mitad] = NEGRO
    tablero[mitad][mitad - 1] = NEGRO
    return tablero


def dentro(fila: int, columna: int) -> bool:
    """Verifica si una posición está dentro del tablero"""
    return 0 <= fila < TAMAÑO_TABLERO and 0 <= columna < TAMAÑO_TABLERO


def movimientos_validos(tablero: List[List[int]], jugador: int) -> List[Tuple[int, int]]:
    """Encuentra todos los movimientos válidos para un jugador"""
    movimientos = []
    oponente = NEGRO if jugador == BLANCO else BLANCO

    for fila in range(TAMAÑO_TABLERO):
        for columna in range(TAMAÑO_TABLERO):
            if tablero[fila][columna] != VACIO:
                continue

            valido = False
            for df, dc in DIRECCIONES:
                f, c = fila + df, columna + dc
                encontro_oponente = False

                while dentro(f, c) and tablero[f][c] == oponente:
                    encontro_oponente = True
                    f += df
                    c += dc

                if encontro_oponente and dentro(f, c) and tablero[f][c] == jugador:
                    valido = True
                    break

            if valido:
                movimientos.append((fila, columna))

    return movimientos


def aplicar_movimiento(tablero: List[List[int]], movimiento: Tuple[int, int], jugador: int) -> List[List[int]]:
    """Aplica un movimiento y voltea las fichas capturadas"""
    fila, columna = movimiento
    nuevo_tablero = [fila[:] for fila in tablero]
    nuevo_tablero[fila][columna] = jugador
    oponente = NEGRO if jugador == BLANCO else BLANCO

    for df, dc in DIRECCIONES:
        f, c = fila + df, columna + dc
        fichas_voltear = []

        while dentro(f, c) and nuevo_tablero[f][c] == oponente:
            fichas_voltear.append((f, c))
            f += df
            c += dc

        if fichas_voltear and dentro(f, c) and nuevo_tablero[f][c] == jugador:
            for fv, cv in fichas_voltear:
                nuevo_tablero[fv][cv] = jugador

    return nuevo_tablero


def contar_puntuacion(tablero: List[List[int]]) -> Tuple[int, int]:
    """Cuenta las fichas de cada jugador"""
    fichas_negras = sum(1 for f in range(TAMAÑO_TABLERO) for c in range(TAMAÑO_TABLERO) if tablero[f][c] == NEGRO)
    fichas_blancas = sum(1 for f in range(TAMAÑO_TABLERO) for c in range(TAMAÑO_TABLERO) if tablero[f][c] == BLANCO)
    return fichas_negras, fichas_blancas


def juego_terminado(tablero: List[List[int]]) -> bool:
    """Verifica si el juego ha terminado"""
    return not movimientos_validos(tablero, NEGRO) and not movimientos_validos(tablero, BLANCO)


def contar_casillas_ocupadas(tablero: List[List[int]]) -> int:
    """Cuenta cuántas casillas están ocupadas"""
    return sum(1 for f in range(TAMAÑO_TABLERO) for c in range(TAMAÑO_TABLERO) if tablero[f][c] != VACIO)


def calcular_profundidad_dinamica(tablero: List[List[int]]) -> int:
    """Calcula la profundidad de búsqueda según la fase del juego"""
    # Cuenta cuántas casillas del tablero están ocupadas (tienen fichas)
    ocupadas = contar_casillas_ocupadas(tablero)

    # Calcula el total de casillas del tablero (8x8 = 64)
    total_casillas = TAMAÑO_TABLERO * TAMAÑO_TABLERO

    # Calcula el porcentaje de casillas ocupadas dividiendo ocupadas entre el total
    porcentaje_lleno = ocupadas / total_casillas

    # Si menos del 35% del tablero está ocupado (fase inicial del juego)
    if porcentaje_lleno < 0.35:
        # Retorna profundidad baja (búsqueda rápida) = 1
        return PROFUNDIDAD_MAX_INICIO
    # Si está ocupado entre 35% y 70% (fase media del juego)
    elif porcentaje_lleno < 0.70:
        # Retorna profundidad media (búsqueda moderada) = 2
        return PROFUNDIDAD_MAX_MEDIO
    # Si está ocupado más del 70% (fase final del juego)
    else:
        # Retorna profundidad alta (búsqueda profunda) = 3
        return PROFUNDIDAD_MAX_FINAL


def heuristica(tablero: List[List[int]], jugador: int) -> float:
    """Función de evaluación heurística"""
    mi_color = BLANCO
    oponente = NEGRO

    mis_fichas = sum(1 for f in range(TAMAÑO_TABLERO) for c in range(TAMAÑO_TABLERO) if tablero[f][c] == mi_color)
    fichas_oponente = sum(1 for f in range(TAMAÑO_TABLERO) for c in range(TAMAÑO_TABLERO) if tablero[f][c] == oponente)
    diferencia_fichas = mis_fichas - fichas_oponente

    esquinas = [(0, 0), (0, TAMAÑO_TABLERO - 1), (TAMAÑO_TABLERO - 1, 0), (TAMAÑO_TABLERO - 1, TAMAÑO_TABLERO - 1)]
    puntuacion_esquinas = 0
    for (f, c) in esquinas:
        if tablero[f][c] == mi_color:
            puntuacion_esquinas += 15
        elif tablero[f][c] == oponente:
            puntuacion_esquinas -= 15

    return diferencia_fichas * 1.0 + puntuacion_esquinas * 0.8


def minimax(tablero: List[List[int]], profundidad: int, alfa: float, beta: float,
            maximizando: bool, color_jugador: int, tiempo_fin: float,
            cache: Dict = None) -> Tuple[Optional[Tuple[int, int]], float, bool]:
    """Algoritmo Minimax con poda Alpha-Beta"""
    if time.time() > tiempo_fin:
        return None, heuristica(tablero, BLANCO), True

    if cache is None:
        cache = {}

    if profundidad == 0 or juego_terminado(tablero):
        return None, heuristica(tablero, BLANCO), False

    clave = tuple(x for fila in tablero for x in fila)
    clave = (clave, profundidad, maximizando)
    if cache and clave in cache:
        return None, cache[clave], False

    jugador_actual = BLANCO if maximizando else NEGRO
    movimientos = movimientos_validos(tablero, jugador_actual)

    if not movimientos:
        _, puntuacion, timeout = minimax(tablero, profundidad - 1, alfa, beta, not maximizando, color_jugador,
                                         tiempo_fin, cache)
        return None, puntuacion, timeout

    def clave_movimiento(m):
        f, c = m
        if (f, c) in [(0, 0), (0, TAMAÑO_TABLERO - 1), (TAMAÑO_TABLERO - 1, 0),
                      (TAMAÑO_TABLERO - 1, TAMAÑO_TABLERO - 1)]:
            return -100
        return abs(f - TAMAÑO_TABLERO / 2) + abs(c - TAMAÑO_TABLERO / 2)

    movimientos.sort(key=clave_movimiento)
    mejor_movimiento = None

    if maximizando:
        valor = -math.inf
        for mov in movimientos:
            if time.time() > tiempo_fin:
                return None, heuristica(tablero, BLANCO), True
            nuevo_tablero = aplicar_movimiento(tablero, mov, jugador_actual)
            _, puntuacion, timeout = minimax(nuevo_tablero, profundidad - 1, alfa, beta, False, color_jugador,
                                             tiempo_fin, cache)
            if timeout:
                return None, puntuacion, True
            if puntuacion > valor:
                valor = puntuacion
                mejor_movimiento = mov
            alfa = max(alfa, valor)
            if alfa >= beta:
                break
    else:
        valor = math.inf
        for mov in movimientos:
            if time.time() > tiempo_fin:
                return None, heuristica(tablero, BLANCO), True
            nuevo_tablero = aplicar_movimiento(tablero, mov, jugador_actual)
            _, puntuacion, timeout = minimax(nuevo_tablero, profundidad - 1, alfa, beta, True, color_jugador,
                                             tiempo_fin, cache)
            if timeout:
                return None, puntuacion, True
            if puntuacion < valor:
                valor = puntuacion
                mejor_movimiento = mov
            beta = min(beta, valor)
            if alfa >= beta:
                break

    if cache is not None:
        cache[clave] = valor
    return mejor_movimiento, valor, False


class TrabajadorIA(threading.Thread):
    """Thread worker para la IA"""

    def __init__(self, tablero: List[List[int]], limite_tiempo: float, profundidad_max: int):
        super().__init__()
        self.tablero = [fila[:] for fila in tablero]
        self.limite_tiempo = limite_tiempo
        self.profundidad_max = profundidad_max
        self.mejor_movimiento: Optional[Tuple[int, int]] = None
        self.mejor_puntuacion: float = -math.inf
        self.timeout = False
        self.daemon = True
        self._debe_parar = False

    def run(self):
        tiempo_fin = time.time() + self.limite_tiempo
        cache: Dict = {}

        for profundidad in range(1, self.profundidad_max + 1):
            if time.time() >= tiempo_fin or self._debe_parar:
                break
            movimiento, puntuacion, timeout = minimax(self.tablero, profundidad, -math.inf, math.inf, True, BLANCO,
                                                      tiempo_fin, cache)
            if timeout:
                self.timeout = True
                break
            if movimiento is not None:
                self.mejor_movimiento = movimiento
                self.mejor_puntuacion = puntuacion
            if abs(puntuacion) > 1e6:
                break

    def detener(self):
        self._debe_parar = True


# ---------- UI Moderna ----------

def dibujar_rectangulo_redondeado(superficie, color, rect, radio=10):
    """Dibuja un rectángulo con bordes redondeados"""
    pygame.draw.rect(superficie, color, rect, border_radius=radio)


def dibujar_tarjeta(superficie, x, y, ancho, alto, color=FONDO_TARJETA, radio=12):
    """Dibuja una tarjeta moderna con sombra"""
    # Sombra
    superficie_sombra = pygame.Surface((ancho + 4, alto + 4), pygame.SRCALPHA)
    dibujar_rectangulo_redondeado(superficie_sombra, SOMBRA, (0, 0, ancho + 4, alto + 4), radio)
    superficie.blit(superficie_sombra, (x - 2, y - 2))
    # Tarjeta
    dibujar_rectangulo_redondeado(superficie, color, (x, y, ancho, alto), radio)


def dibujar_barra_progreso(superficie, x, y, ancho, alto, porcentaje, color=ACENTO):
    """Dibuja una barra de progreso"""
    # Fondo
    dibujar_rectangulo_redondeado(superficie, (30, 40, 52), (x, y, ancho, alto), 6)
    # Progreso
    if porcentaje > 0:
        ancho_progreso = int(ancho * min(porcentaje, 1.0))
        dibujar_rectangulo_redondeado(superficie, color, (x, y, ancho_progreso, alto), 6)


def dibujar_tablero_moderno(pantalla, tablero, movimientos_validos_param=None, fuente=None, pensando=False,
                            mostrar_ayuda=True, celda_hover=None):
    """Dibuja el tablero con diseño moderno"""
    pantalla.fill(FONDO)

    # Header con título
    fuente_titulo = pygame.font.SysFont("Arial", 42, bold=True)
    titulo = fuente_titulo.render("OTHELLO", True, TEXTO)
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))

    fuente_subtitulo = pygame.font.SysFont("Arial", 16)
    subtitulo = fuente_subtitulo.render("Juego de Reversi", True, TEXTO_SECUNDARIO)
    pantalla.blit(subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, 68))

    # Panel de información superior
    info_y = 100
    ocupadas = contar_casillas_ocupadas(tablero)
    porcentaje = ocupadas / 64

    # Barra de progreso del juego
    dibujar_tarjeta(pantalla, MARGEN_LATERAL, info_y, ANCHO - MARGEN_LATERAL * 2, 60)

    fuente_fase = pygame.font.SysFont("Arial", 14, bold=True)
    if porcentaje < 0.35:
        fase = "INICIO"
        color_fase = EXITO
    elif porcentaje < 0.70:
        fase = "MEDIO JUEGO"
        color_fase = ADVERTENCIA
    else:
        fase = "FINAL"
        color_fase = PELIGRO

    texto_fase = fuente_fase.render(f"Fase: {fase}", True, color_fase)
    pantalla.blit(texto_fase, (MARGEN_LATERAL + 15, info_y + 12))

    dibujar_barra_progreso(pantalla, MARGEN_LATERAL + 15, info_y + 35, ANCHO - MARGEN_LATERAL * 2 - 30, 12,
                           porcentaje, color_fase)

    # Offset del tablero
    tablero_x = MARGEN_LATERAL
    tablero_y = MARGEN_SUPERIOR

    # Dibuja tarjeta del tablero con sombra
    dibujar_tarjeta(pantalla, tablero_x - 10, tablero_y - 10,
                    TAMAÑO_TABLERO * CASILLA + 20, TAMAÑO_TABLERO * CASILLA + 20, VERDE_TABLERO, 15)

    # Dibuja grid del tablero
    for fila in range(TAMAÑO_TABLERO):
        for columna in range(TAMAÑO_TABLERO):
            x = tablero_x + columna * CASILLA
            y = tablero_y + fila * CASILLA

            # Efecto hover
            if celda_hover and celda_hover == (fila, columna) and movimientos_validos_param and (fila,
                                                                                                 columna) in movimientos_validos_param:
                superficie_hover = pygame.Surface((CASILLA, CASILLA), pygame.SRCALPHA)
                superficie_hover.fill((255, 255, 255, 30))
                pantalla.blit(superficie_hover, (x, y))

            pygame.draw.rect(pantalla, GRID, (x, y, CASILLA, CASILLA), 1)

            valor = tablero[fila][columna]
            centro_x = x + CASILLA // 2
            centro_y = y + CASILLA // 2

            if valor == NEGRO:
                # Sombra de la ficha
                pygame.draw.circle(pantalla, (0, 0, 0, 60), (centro_x + 2, centro_y + 2), CASILLA // 2 - 8)
                # Ficha negra con gradiente simulado
                pygame.draw.circle(pantalla, COLOR_NEGRO, (centro_x, centro_y), CASILLA // 2 - 8)
                pygame.draw.circle(pantalla, (50, 50, 50), (centro_x - 5, centro_y - 5), 8)
            elif valor == BLANCO:
                # Sombra de la ficha
                pygame.draw.circle(pantalla, (0, 0, 0, 60), (centro_x + 2, centro_y + 2), CASILLA // 2 - 8)
                # Ficha blanca con gradiente simulado
                pygame.draw.circle(pantalla, COLOR_BLANCO, (centro_x, centro_y), CASILLA // 2 - 8)
                pygame.draw.circle(pantalla, (255, 255, 255), (centro_x - 5, centro_y - 5), 8)

    # Movimientos válidos con animación
    if movimientos_validos_param:
        pulso = abs(math.sin(time.time() * 3)) * 0.3 + 0.7
        for (fila, columna) in movimientos_validos_param:
            cx = tablero_x + columna * CASILLA + CASILLA // 2
            cy = tablero_y + fila * CASILLA + CASILLA // 2
            radio = int(14 * pulso)
            # Anillo exterior
            pygame.draw.circle(pantalla, (255, 215, 0, 100), (cx, cy), radio + 4)
            # Círculo interior
            pygame.draw.circle(pantalla, (255, 215, 0), (cx, cy), radio, 3)

    # Paneles laterales con puntuación
    puntos_negros, puntos_blancos = contar_puntuacion(tablero)

    # Panel jugador (izquierda)
    tarjeta_jugador_y = tablero_y
    dibujar_tarjeta(pantalla, 10, tarjeta_jugador_y, MARGEN_LATERAL - 20, 140)

    fuente_jugador = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_puntos = pygame.font.SysFont("Arial", 36, bold=True)

    # Jugador negro
    texto_jugador = fuente_jugador.render("TÚ", True, TEXTO_SECUNDARIO)
    pantalla.blit(texto_jugador, (20, tarjeta_jugador_y + 15))

    pygame.draw.circle(pantalla, COLOR_NEGRO, (40, tarjeta_jugador_y + 55), 18)
    pygame.draw.circle(pantalla, (50, 50, 50), (35, tarjeta_jugador_y + 50), 6)

    texto_puntos = fuente_puntos.render(str(puntos_negros), True, TEXTO)
    pantalla.blit(texto_puntos, (20, tarjeta_jugador_y + 85))

    # Panel IA (debajo del jugador)
    tarjeta_ia_y = tarjeta_jugador_y + 160
    dibujar_tarjeta(pantalla, 10, tarjeta_ia_y, MARGEN_LATERAL - 20, 140)

    texto_ia = fuente_jugador.render("IA", True, TEXTO_SECUNDARIO)
    pantalla.blit(texto_ia, (20, tarjeta_ia_y + 15))

    pygame.draw.circle(pantalla, COLOR_BLANCO, (40, tarjeta_ia_y + 55), 18)
    pygame.draw.circle(pantalla, (255, 255, 255), (35, tarjeta_ia_y + 50), 6)

    texto_puntos_ia = fuente_puntos.render(str(puntos_blancos), True, TEXTO)
    pantalla.blit(texto_puntos_ia, (20, tarjeta_ia_y + 85))

    # Panel de ayuda (derecha) - MEJORADO
    if mostrar_ayuda:
        ayuda_x = ANCHO - MARGEN_LATERAL + 10
        ayuda_y = tablero_y
        ancho_ayuda = MARGEN_LATERAL - 20
        alto_ayuda = 340  # Aumentado para más espacio

        dibujar_tarjeta(pantalla, ayuda_x, ayuda_y, ancho_ayuda, alto_ayuda)

        fuente_titulo_ayuda = pygame.font.SysFont("Arial", 13, bold=True)
        fuente_texto_ayuda = pygame.font.SysFont("Arial", 10)

        titulo_ayuda = fuente_titulo_ayuda.render("AYUDA", True, ACENTO)
        pantalla.blit(titulo_ayuda, (ayuda_x + 10, ayuda_y + 10))

        ayudas = [
            ("Objetivo:", ADVERTENCIA),
            ("Tener más fichas al", TEXTO_SECUNDARIO),
            ("final del juego", TEXTO_SECUNDARIO),
            ("", None),
            ("Regla principal:", ADVERTENCIA),
            ("Captura fichas", TEXTO_SECUNDARIO),
            ("encerrándolas entre", TEXTO_SECUNDARIO),
            ("tus propias fichas", TEXTO_SECUNDARIO),
            ("", None),
            ("Esquinas:", ADVERTENCIA),
            ("¡Muy valiosas!", EXITO),
            ("No pueden ser", TEXTO_SECUNDARIO),
            ("capturadas", TEXTO_SECUNDARIO),
            ("", None),
            ("Controles:", ADVERTENCIA),
            ("R - Reiniciar", TEXTO_SECUNDARIO),
            ("H - Ocultar ayuda", TEXTO_SECUNDARIO),
            ("ESC - Salir", TEXTO_SECUNDARIO),
        ]

        y_offset = 35
        espaciado_linea = 18

        for texto, color in ayudas:
            if texto == "":
                y_offset += 5  # Espacio extra entre secciones
            elif color == ADVERTENCIA or color == EXITO:
                t = fuente_titulo_ayuda.render(texto, True, color)
                pantalla.blit(t, (ayuda_x + 10, ayuda_y + y_offset))
                y_offset += espaciado_linea
            else:
                t = fuente_texto_ayuda.render(texto, True, color)
                pantalla.blit(t, (ayuda_x + 15, ayuda_y + y_offset))
                y_offset += espaciado_linea

    # Controles (parte inferior)
    controles_y = ALTO - 70
    fuente_control = pygame.font.SysFont("Arial", 12)

    controles = [
        ("R", "Reiniciar"),
        ("H", "Ayuda" if mostrar_ayuda else "Mostrar ayuda"),
        ("ESC", "Salir"),
    ]

    control_x = MARGEN_LATERAL
    for tecla, descripcion in controles:
        # Tecla
        dibujar_rectangulo_redondeado(pantalla, FONDO_TARJETA, (control_x, controles_y, 35, 25), 5)
        texto_tecla = fuente_control.render(tecla, True, ACENTO)
        pantalla.blit(texto_tecla, (control_x + 18 - texto_tecla.get_width() // 2, controles_y + 5))

        # Descripción
        texto_desc = fuente_control.render(descripcion, True, TEXTO_SECUNDARIO)
        pantalla.blit(texto_desc, (control_x + 40, controles_y + 6))

        control_x += 165

    # Overlay de pensamiento
    if pensando:
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        pantalla.blit(overlay, (0, 0))

        # Card de pensamiento
        ancho_pensando = 300
        alto_pensando = 100
        x_pensando = ANCHO // 2 - ancho_pensando // 2
        y_pensando = ALTO // 2 - alto_pensando // 2

        dibujar_tarjeta(pantalla, x_pensando, y_pensando, ancho_pensando, alto_pensando)

        fuente_pensando = pygame.font.SysFont("Arial", 24, bold=True)
        texto_pensando = fuente_pensando.render("IA Pensando...", True, ACENTO)
        pantalla.blit(texto_pensando,
                      (x_pensando + ancho_pensando // 2 - texto_pensando.get_width() // 2, y_pensando + 30))

        # Spinner animado
        angulo_spinner = (time.time() * 200) % 360
        spinner_x = x_pensando + ancho_pensando // 2
        spinner_y = y_pensando + 70
        for i in range(8):
            angulo = math.radians(angulo_spinner + i * 45)
            alpha = int(255 * (i / 8))
            fin_x = spinner_x + math.cos(angulo) * 15
            fin_y = spinner_y + math.sin(angulo) * 15
            pygame.draw.circle(pantalla, (*ACENTO[:3], alpha) if len(ACENTO) == 3 else ACENTO,
                               (int(fin_x), int(fin_y)), 3)

    pygame.display.flip()


def convertir_click_a_celda(posicion) -> Optional[Tuple[int, int]]:
    """Convierte click del mouse a coordenadas del tablero"""
    x, y = posicion
    tablero_x = MARGEN_LATERAL
    tablero_y = MARGEN_SUPERIOR

    if x < tablero_x or x >= tablero_x + TAMAÑO_TABLERO * CASILLA:
        return None
    if y < tablero_y or y >= tablero_y + TAMAÑO_TABLERO * CASILLA:
        return None

    columna = (x - tablero_x) // CASILLA
    fila = (y - tablero_y) // CASILLA

    if 0 <= fila < TAMAÑO_TABLERO and 0 <= columna < TAMAÑO_TABLERO:
        return (fila, columna)
    return None


def main():
    """Bucle principal del juego"""
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Othello - Interfaz Moderna")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 26, bold=True)

    tablero = inicializar_tablero()
    turno_jugador = NEGRO
    trabajador_ia = None
    pensando = False
    mostrar_ayuda = True
    celda_hover = None

    ejecutando = True
    while ejecutando:
        reloj.tick(FPS)

        # Detectar hover
        posicion_mouse = pygame.mouse.get_pos()
        celda_hover = convertir_click_a_celda(posicion_mouse)

        movimientos_validos_actual = movimientos_validos(tablero, turno_jugador)
        movs_mostrar = movimientos_validos_actual if turno_jugador == NEGRO else None

        dibujar_tablero_moderno(pantalla, tablero, movimientos_validos_param=movs_mostrar, fuente=fuente,
                                pensando=pensando, mostrar_ayuda=mostrar_ayuda, celda_hover=celda_hover)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                if trabajador_ia and trabajador_ia.is_alive():
                    trabajador_ia.detener()
                break

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                    if trabajador_ia and trabajador_ia.is_alive():
                        trabajador_ia.detener()
                    break

                if evento.key == pygame.K_r:
                    if trabajador_ia and trabajador_ia.is_alive():
                        trabajador_ia.detener()
                    tablero = inicializar_tablero()
                    turno_jugador = NEGRO
                    pensando = False
                    trabajador_ia = None

                if evento.key == pygame.K_h:
                    mostrar_ayuda = not mostrar_ayuda

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if turno_jugador == NEGRO and not pensando:
                    celda = convertir_click_a_celda(evento.pos)
                    if celda and celda in movimientos_validos_actual:
                        tablero = aplicar_movimiento(tablero, celda, NEGRO)
                        turno_jugador = BLANCO
                        if trabajador_ia and trabajador_ia.is_alive():
                            trabajador_ia.detener()
                            trabajador_ia = None

        if juego_terminado(tablero):
            negras, blancas = contar_puntuacion(tablero)
            dibujar_tablero_moderno(pantalla, tablero, fuente=fuente, pensando=False, mostrar_ayuda=mostrar_ayuda)

            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            pantalla.blit(overlay, (0, 0))

            # Card de resultado
            ancho_resultado = 400
            alto_resultado = 280
            x_resultado = ANCHO // 2 - ancho_resultado // 2
            y_resultado = ALTO // 2 - alto_resultado // 2

            dibujar_tarjeta(pantalla, x_resultado, y_resultado, ancho_resultado, alto_resultado)

            if negras > blancas:
                mensaje = "¡GANASTE!"
                color = EXITO
            elif blancas > negras:
                mensaje = "IA GANA"
                color = PELIGRO
            else:
                mensaje = "EMPATE"
                color = ADVERTENCIA

            fuente_grande = pygame.font.SysFont("Arial", 48, bold=True)
            texto_grande = fuente_grande.render(mensaje, True, color)
            pantalla.blit(texto_grande,
                          (x_resultado + ancho_resultado // 2 - texto_grande.get_width() // 2, y_resultado + 30))

            fuente_resultado = pygame.font.SysFont("Arial", 36)
            texto_resultado = fuente_resultado.render(f"{negras} - {blancas}", True, TEXTO)
            pantalla.blit(texto_resultado,
                          (x_resultado + ancho_resultado // 2 - texto_resultado.get_width() // 2, y_resultado + 100))

            fuente_pequeña = pygame.font.SysFont("Arial", 18)
            texto_pequeño = fuente_pequeña.render("Pulsa R para reiniciar", True, TEXTO_SECUNDARIO)
            pantalla.blit(texto_pequeño,
                          (x_resultado + ancho_resultado // 2 - texto_pequeño.get_width() // 2, y_resultado + 160))

            pygame.display.flip()
            time.sleep(0.2)
            continue

        if turno_jugador == BLANCO and not pensando and movimientos_validos(tablero, BLANCO):
            profundidad = calcular_profundidad_dinamica(tablero)
            trabajador_ia = TrabajadorIA(tablero, limite_tiempo=LIMITE_TIEMPO, profundidad_max=profundidad)
            pensando = True
            trabajador_ia.start()

        if trabajador_ia and trabajador_ia.is_alive():
            pass
        elif trabajador_ia and not trabajador_ia.is_alive() and pensando:
            pensando = False
            elegido = trabajador_ia.mejor_movimiento
            if elegido is None:
                opciones = movimientos_validos(tablero, BLANCO)
                elegido = random.choice(opciones) if opciones else None
            if elegido:
                tablero = aplicar_movimiento(tablero, elegido, BLANCO)
            turno_jugador = NEGRO
            trabajador_ia = None

        if turno_jugador == BLANCO and not movimientos_validos(tablero, BLANCO) and not juego_terminado(tablero):
            turno_jugador = NEGRO

        if turno_jugador == NEGRO and not movimientos_validos(tablero, NEGRO) and not juego_terminado(tablero):
            turno_jugador = BLANCO

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()