# -*- coding: utf-8 -*-
"""
CHAIN REACTION ⚡ - EXPLOSIONES SIMBÓLICAS Y AMBIENTADAS
Las explosiones ahora aparecen de forma elegante sin sobrecargar
"""

import pygame
import sys
import math
import random
import time
import threading
from typing import List, Tuple, Optional


class Celda:
    """Representa una celda del tablero con orbes"""

    def __init__(self, masa_critica: int):
        self.orbes = 0
        self.color = 0
        self.masa_critica = masa_critica

    def agregar_orbe(self, color: int):
        self.orbes += 1
        self.color = color

    def esta_critica(self) -> bool:
        return self.orbes >= self.masa_critica

    def explotar(self) -> int:
        color = self.color
        self.orbes = 0
        self.color = 0
        return color

    def esta_vacia(self) -> bool:
        return self.orbes == 0


class Tablero:
    """Gestiona el tablero 5x5 y la lógica del juego"""

    NUM_FILAS = 5
    NUM_COLUMNAS = 5
    VACIO = 0
    JUGADOR_AZUL = 1
    JUGADOR_ROJO = 2

    def __init__(self):
        self.tablero = []
        self._inicializar_tablero()
        self.primer_movimiento_azul = True
        self.primer_movimiento_rojo = True

    def _inicializar_tablero(self):
        self.tablero = []
        for fila in range(self.NUM_FILAS):
            fila_celdas = []
            for col in range(self.NUM_COLUMNAS):
                masa_critica = self._calcular_masa_critica(fila, col)
                fila_celdas.append(Celda(masa_critica))
            self.tablero.append(fila_celdas)

    def _calcular_masa_critica(self, fila: int, col: int) -> int:
        es_esquina = (fila in [0, self.NUM_FILAS - 1]) and (col in [0, self.NUM_COLUMNAS - 1])
        es_borde = (fila in [0, self.NUM_FILAS - 1]) or (col in [0, self.NUM_COLUMNAS - 1])

        if es_esquina:
            return 2
        elif es_borde:
            return 3
        else:
            return 4

    def copia(self):
        nuevo = Tablero()
        nuevo.primer_movimiento_azul = self.primer_movimiento_azul
        nuevo.primer_movimiento_rojo = self.primer_movimiento_rojo

        for fila in range(self.NUM_FILAS):
            for col in range(self.NUM_COLUMNAS):
                nuevo.tablero[fila][col].orbes = self.tablero[fila][col].orbes
                nuevo.tablero[fila][col].color = self.tablero[fila][col].color

        return nuevo

    def obtener_adyacentes(self, fila: int, col: int) -> List[Tuple[int, int]]:
        adyacentes = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for df, dc in direcciones:
            nueva_fila = fila + df
            nueva_col = col + dc
            if 0 <= nueva_fila < self.NUM_FILAS and 0 <= nueva_col < self.NUM_COLUMNAS:
                adyacentes.append((nueva_fila, nueva_col))

        return adyacentes

    def colocar_orbe(self, fila: int, col: int, jugador: int) -> List[List[Tuple[int, int]]]:
        """Coloca orbe y retorna explosiones por generación"""
        celda = self.tablero[fila][col]
        if not celda.esta_vacia() and celda.color != jugador:
            return []

        if jugador == self.JUGADOR_AZUL:
            self.primer_movimiento_azul = False
        else:
            self.primer_movimiento_rojo = False

        self.tablero[fila][col].agregar_orbe(jugador)

        explosiones_por_generacion = []
        explosiones = [(fila, col)]
        max_iteraciones = 100
        iteracion = 0

        while explosiones and iteracion < max_iteraciones:
            iteracion += 1
            nueva_generacion = []
            explosiones_actuales = []

            for exp_fila, exp_col in explosiones:
                if self.tablero[exp_fila][exp_col].esta_critica():
                    explosiones_actuales.append((exp_fila, exp_col))

            if explosiones_actuales:
                explosiones_por_generacion.append(explosiones_actuales)

            for exp_fila, exp_col in explosiones_actuales:
                color_explosion = self.tablero[exp_fila][exp_col].explotar()

                for adj_fila, adj_col in self.obtener_adyacentes(exp_fila, exp_col):
                    self.tablero[adj_fila][adj_col].agregar_orbe(color_explosion)

                    if self.tablero[adj_fila][adj_col].esta_critica():
                        if (adj_fila, adj_col) not in nueva_generacion:
                            nueva_generacion.append((adj_fila, adj_col))

            explosiones = nueva_generacion

        return explosiones_por_generacion

    def movimiento_valido(self, fila: int, col: int, jugador: int) -> bool:
        if not (0 <= fila < self.NUM_FILAS and 0 <= col < self.NUM_COLUMNAS):
            return False

        celda = self.tablero[fila][col]
        return celda.esta_vacia() or celda.color == jugador

    def obtener_movimientos_validos(self, jugador: int) -> List[Tuple[int, int]]:
        movimientos = []

        for fila in range(self.NUM_FILAS):
            for col in range(self.NUM_COLUMNAS):
                if self.movimiento_valido(fila, col, jugador):
                    movimientos.append((fila, col))

        return movimientos

    def contar_orbes(self, jugador: int) -> int:
        total = 0
        for fila in range(self.NUM_FILAS):
            for col in range(self.NUM_COLUMNAS):
                if self.tablero[fila][col].color == jugador:
                    total += self.tablero[fila][col].orbes
        return total

    def contar_celdas(self, jugador: int) -> int:
        total = 0
        for fila in range(self.NUM_FILAS):
            for col in range(self.NUM_COLUMNAS):
                if self.tablero[fila][col].color == jugador:
                    total += 1
        return total

    def hay_ganador(self) -> Optional[int]:
        """Verifica si hay ganador"""
        if self.primer_movimiento_azul or self.primer_movimiento_rojo:
            return None

        tiene_orbes_azul = False
        tiene_orbes_rojo = False

        for fila in range(self.NUM_FILAS):
            for col in range(self.NUM_COLUMNAS):
                if self.tablero[fila][col].color == self.JUGADOR_AZUL:
                    tiene_orbes_azul = True
                elif self.tablero[fila][col].color == self.JUGADOR_ROJO:
                    tiene_orbes_rojo = True

        if tiene_orbes_azul and not tiene_orbes_rojo:
            return self.JUGADOR_AZUL
        elif tiene_orbes_rojo and not tiene_orbes_azul:
            return self.JUGADOR_ROJO

        return None

    def evaluar_posicion(self, jugador: int) -> float:
        enemigo = self.JUGADOR_ROJO if jugador == self.JUGADOR_AZUL else self.JUGADOR_AZUL
        score = 0

        mis_orbes = self.contar_orbes(jugador)
        orbes_enemigo = self.contar_orbes(enemigo)

        if orbes_enemigo == 0 and mis_orbes > 0:
            return 1000000
        if mis_orbes == 0 and orbes_enemigo > 0:
            return -1000000

        score += (mis_orbes - orbes_enemigo) * 10

        mis_celdas = self.contar_celdas(jugador)
        celdas_enemigo = self.contar_celdas(enemigo)
        score += (mis_celdas - celdas_enemigo) * 15

        esquinas = [(0, 0), (0, self.NUM_COLUMNAS - 1),
                    (self.NUM_FILAS - 1, 0), (self.NUM_FILAS - 1, self.NUM_COLUMNAS - 1)]
        for fila, col in esquinas:
            if self.tablero[fila][col].color == jugador:
                score += 20
            elif self.tablero[fila][col].color == enemigo:
                score -= 20

        return score


# ════════════════════════════════════════════════════════════════════════════════
# SISTEMA DE EXPLOSIONES SIMBÓLICAS
# ════════════════════════════════════════════════════════════════════════════════

class Particula:
    """Partícula de explosión elegante"""

    def __init__(self, x, y, color):
        self.x, self.y = x, y
        angulo = random.uniform(0, 2 * math.pi)
        velocidad = random.uniform(2, 8)
        self.vx = math.cos(angulo) * velocidad
        self.vy = math.sin(angulo) * velocidad
        self.vida = 30
        self.color = color
        self.tamaño = random.randint(3, 8)

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vida -= 1
        self.tamaño = max(1, self.tamaño - 0.2)

    def dibujar(self, screen):
        if self.vida > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.tamaño))


class Onda:
    """Onda de energía expansiva simbólica"""

    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.radio = 5
        self.radio_max = 60
        self.vida = 15

    def actualizar(self):
        self.radio += 4
        self.vida -= 1

    def dibujar(self, screen):
        if self.vida > 0:
            alpha = int(255 * (self.vida / 15))
            if self.radio < self.radio_max:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radio), 3)


class Destello:
    """Destello luminoso en el centro de la explosión"""

    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.vida = 20
        self.tamaño = 25

    def actualizar(self):
        self.vida -= 1
        self.tamaño = 25 * (self.vida / 20)

    def dibujar(self, screen):
        if self.vida > 0:
            color_claro = tuple(min(255, c + 100) for c in self.color)
            pygame.draw.circle(screen, color_claro, (int(self.x), int(self.y)), int(self.tamaño))


class ChainReaction:
    """Motor principal del juego con IA"""

    PROFUNDIDAD_MAX = 4
    TIEMPO_MAX_IA = 1.2

    def __init__(self, profundidad: int = 4):
        self.PROFUNDIDAD_MAX = profundidad
        self.tablero = Tablero()
        self.turno_actual = Tablero.JUGADOR_AZUL
        self.game_over = False
        self.tiempo_inicio = 0
        self.tiempo_inicio_partida = 0

        self.estadisticas = {
            'partidas_jugadas': 0,
            'victorias_humano': 0,
            'victorias_ia': 0,
            'mayor_cadena': 0,
            'mayor_cadena_sesion': 0,
            'tiempo_total': 0,
            'tiempo_promedio': 0
        }

        self.historial_orbes = {
            'azul': [],
            'rojo': [],
            'turnos': []
        }

    def minimax(self, tablero: Tablero, profundidad: int,
                alpha: float, beta: float, maximizando: bool) -> Tuple[Optional[Tuple[int, int]], float]:
        """Minimax con alpha-beta pruning"""
        if hasattr(self, 'tiempo_inicio') and time.time() - self.tiempo_inicio > self.TIEMPO_MAX_IA:
            return (None, tablero.evaluar_posicion(Tablero.JUGADOR_ROJO))

        ganador = tablero.hay_ganador()
        jugador = Tablero.JUGADOR_ROJO if maximizando else Tablero.JUGADOR_AZUL
        movimientos_validos = tablero.obtener_movimientos_validos(jugador)

        if ganador is not None:
            if ganador == Tablero.JUGADOR_ROJO:
                return (None, 1000000)
            else:
                return (None, -1000000)

        if profundidad == 0 or not movimientos_validos:
            return (None, tablero.evaluar_posicion(Tablero.JUGADOR_ROJO))

        if len(movimientos_validos) > 8:
            movimientos_con_orbes = []
            for fila, col in movimientos_validos:
                if tablero.tablero[fila][col].orbes > 0:
                    movimientos_con_orbes.append((tablero.tablero[fila][col].orbes, fila, col))

            movimientos_con_orbes.sort(reverse=True)
            movimientos_validos = [(f, c) for _, f, c in movimientos_con_orbes[:4]]

            if len(movimientos_validos) < 3:
                restantes = [m for m in tablero.obtener_movimientos_validos(jugador) if m not in movimientos_validos]
                if restantes:
                    movimientos_validos.extend(random.sample(restantes, min(2, len(restantes))))

        if maximizando:
            valor = -math.inf
            mejor_movimiento = random.choice(movimientos_validos) if movimientos_validos else None

            for fila, col in movimientos_validos:
                if time.time() - self.tiempo_inicio > self.TIEMPO_MAX_IA:
                    break

                copia_tablero = tablero.copia()
                copia_tablero.colocar_orbe(fila, col, Tablero.JUGADOR_ROJO)
                _, nuevo_score = self.minimax(copia_tablero, profundidad - 1, alpha, beta, False)

                if nuevo_score > valor:
                    valor = nuevo_score
                    mejor_movimiento = (fila, col)

                alpha = max(alpha, valor)
                if alpha >= beta:
                    break

            return mejor_movimiento, valor
        else:
            valor = math.inf
            mejor_movimiento = random.choice(movimientos_validos) if movimientos_validos else None

            for fila, col in movimientos_validos:
                if time.time() - self.tiempo_inicio > self.TIEMPO_MAX_IA:
                    break

                copia_tablero = tablero.copia()
                copia_tablero.colocar_orbe(fila, col, Tablero.JUGADOR_AZUL)
                _, nuevo_score = self.minimax(copia_tablero, profundidad - 1, alpha, beta, True)

                if nuevo_score < valor:
                    valor = nuevo_score
                    mejor_movimiento = (fila, col)

                beta = min(beta, valor)
                if alpha >= beta:
                    break

            return mejor_movimiento, valor

    def cambiar_turno(self):
        self.turno_actual = Tablero.JUGADOR_ROJO if self.turno_actual == Tablero.JUGADOR_AZUL else Tablero.JUGADOR_AZUL
        self.historial_orbes['azul'].append(self.tablero.contar_orbes(Tablero.JUGADOR_AZUL))
        self.historial_orbes['rojo'].append(self.tablero.contar_orbes(Tablero.JUGADOR_ROJO))
        self.historial_orbes['turnos'].append(len(self.historial_orbes['azul']))

    def obtener_profundidad_dinamica(self) -> int:
        orbes_totales = self.tablero.contar_orbes(Tablero.JUGADOR_AZUL) + \
                        self.tablero.contar_orbes(Tablero.JUGADOR_ROJO)
        celdas_ocupadas = self.tablero.contar_celdas(Tablero.JUGADOR_AZUL) + \
                          self.tablero.contar_celdas(Tablero.JUGADOR_ROJO)

        if orbes_totales > 20 or celdas_ocupadas > 16:
            return 1
        elif orbes_totales > 12 or celdas_ocupadas > 10:
            return 2
        elif orbes_totales < 6:
            return 3
        else:
            return 2

    def jugar_gui(self):
        """Modo gráfico COMPLETO CON EXPLOSIONES SIMBÓLICAS"""
        pygame.init()

        # ════════════════════════════════════════════════════════════════════════════════
        # TEMAS DE COLOR
        # ════════════════════════════════════════════════════════════════════════════════
        TEMAS = {
            'clasico': {
                'nombre': 'Clásico',
                'fondo': (255, 255, 255),
                'jugador1': (30, 144, 255),
                'jugador2': (255, 69, 69),
                'acento': (255, 140, 0),
                'panel': (245, 245, 245),
                'texto': (0, 0, 0),
                'texto_suave': (100, 100, 100),
                'victoria': (50, 205, 50)
            },
            'neon': {
                'nombre': 'Neón',
                'fondo': (20, 20, 40),
                'jugador1': (0, 255, 255),
                'jugador2': (255, 0, 255),
                'acento': (0, 255, 0),
                'panel': (30, 30, 50),
                'texto': (255, 255, 255),
                'texto_suave': (180, 180, 200),
                'victoria': (0, 255, 0)
            },
            'naturaleza': {
                'nombre': 'Naturaleza',
                'fondo': (245, 245, 220),
                'jugador1': (34, 139, 34),
                'jugador2': (139, 69, 19),
                'acento': (255, 215, 0),
                'panel': (240, 255, 240),
                'texto': (0, 50, 0),
                'texto_suave': (85, 107, 47),
                'victoria': (50, 205, 50)
            },
            'oceano': {
                'nombre': 'Océano',
                'fondo': (240, 248, 255),
                'jugador1': (0, 105, 148),
                'jugador2': (255, 127, 80),
                'acento': (70, 130, 180),
                'panel': (230, 240, 250),
                'texto': (0, 0, 139),
                'texto_suave': (100, 149, 237),
                'victoria': (50, 205, 50)
            },
            'fuego': {
                'nombre': 'Fuego',
                'fondo': (40, 40, 40),
                'jugador1': (255, 140, 0),
                'jugador2': (220, 20, 60),
                'acento': (255, 215, 0),
                'panel': (50, 50, 50),
                'texto': (255, 255, 255),
                'texto_suave': (200, 200, 200),
                'victoria': (255, 215, 0)
            }
        }

        temas_lista = list(TEMAS.keys())
        idx_tema = 0
        tema_actual = temas_lista[idx_tema]

        def actualizar_colores():
            t = TEMAS[tema_actual]
            return (t['fondo'], t['jugador1'], t['jugador2'], t['acento'],
                    t['panel'], t['texto'], t['texto_suave'], t['victoria'])

        FONDO, AZUL, ROJO, NARANJA, PANEL, TEXTO, TEXTO_SUAVE, VERDE = actualizar_colores()
        BLANCO, GRIS, GRIS_OSCURO = (255, 255, 255), (200, 200, 200), (100, 100, 100)

        # ════════════════════════════════════════════════════════════════════════════════
        # DIMENSIONES
        # ════════════════════════════════════════════════════════════════════════════════
        TAM_CELDA, RADIO_ORBE, MARGEN = 100, 14, 60
        PANEL_SUPERIOR, PANEL_DERECHO = 120, 300
        ANCHO = self.tablero.NUM_COLUMNAS * TAM_CELDA + MARGEN * 2 + PANEL_DERECHO
        ALTO = self.tablero.NUM_FILAS * TAM_CELDA + MARGEN * 2 + PANEL_SUPERIOR

        screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("⚡ CHAIN REACTION - TURBO FIXED")
        clock = pygame.time.Clock()

        # ════════════════════════════════════════════════════════════════════════════════
        # FUENTES
        # ════════════════════════════════════════════════════════════════════════════════
        font_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        font_grande = pygame.font.SysFont("Arial", 36, bold=True)
        font_mediana = pygame.font.SysFont("Arial", 24)
        font_pequeña = pygame.font.SysFont("Arial", 18)
        font_mini = pygame.font.SysFont("Arial", 14)

        # ════════════════════════════════════════════════════════════════════════════════
        # EFECTOS VISUALES
        # ════════════════════════════════════════════════════════════════════════════════
        particulas = []
        ondas = []
        destellos = []

        def crear_explosion_simbolica(x, y, color):
            """
            FIX CRÍTICO: Una sola explosión simbólica por generación
            Combina: ondas + destellos + pocas partículas
            """
            # Ondas expansivas
            for _ in range(2):
                ondas.append(Onda(x, y, color))

            # Destello central
            destellos.append(Destello(x, y, color))

            # Pocas partículas (máximo 5, no 15)
            for _ in range(5):
                particulas.append(Particula(x, y, color))

        def dibujar_orbes_en_celda(x, y, num_orbes, color_orbe):
            color_pygame = AZUL if color_orbe == Tablero.JUGADOR_AZUL else ROJO
            centro_x, centro_y = x + TAM_CELDA // 2, y + TAM_CELDA // 2

            posiciones = {
                1: [(centro_x, centro_y)],
                2: [(centro_x - 18, centro_y - 18), (centro_x + 18, centro_y + 18)],
                3: [(centro_x, centro_y - 18), (centro_x - 18, centro_y + 18), (centro_x + 18, centro_y + 18)],
                4: [(centro_x - 18, centro_y - 18), (centro_x + 18, centro_y - 18),
                    (centro_x - 18, centro_y + 18), (centro_x + 18, centro_y + 18)]
            }

            for pos in posiciones.get(min(num_orbes, 4), []):
                pygame.draw.circle(screen, color_pygame, pos, RADIO_ORBE)
                pygame.draw.circle(screen, BLANCO, pos, RADIO_ORBE, 2)

        def dibujar_grafico_evolucion(x_inicio, y_inicio, ancho, alto):
            if len(self.historial_orbes['turnos']) < 2:
                texto = font_mini.render("Esperando datos...", True, TEXTO_SUAVE)
                screen.blit(texto, (x_inicio + 40, y_inicio + alto // 2))
                return

            pygame.draw.rect(screen, PANEL, (x_inicio, y_inicio, ancho, alto))
            pygame.draw.rect(screen, GRIS_OSCURO, (x_inicio, y_inicio, ancho, alto), 2)

            max_orbes = max(max(self.historial_orbes['azul']), max(self.historial_orbes['rojo']), 1)
            num_puntos = len(self.historial_orbes['turnos'])

            for i in range(5):
                y = y_inicio + (alto // 5) * i
                pygame.draw.line(screen, GRIS, (x_inicio, y), (x_inicio + ancho, y), 1)

            for i in range(1, num_puntos):
                x1 = x_inicio + ((i - 1) / max(num_puntos - 1, 1)) * ancho
                x2 = x_inicio + (i / max(num_puntos - 1, 1)) * ancho

                y1 = y_inicio + alto - (self.historial_orbes['azul'][i - 1] / max_orbes * alto * 0.9)
                y2 = y_inicio + alto - (self.historial_orbes['azul'][i] / max_orbes * alto * 0.9)
                pygame.draw.line(screen, AZUL, (x1, y1), (x2, y2), 3)

                y1_rojo = y_inicio + alto - (self.historial_orbes['rojo'][i - 1] / max_orbes * alto * 0.9)
                y2_rojo = y_inicio + alto - (self.historial_orbes['rojo'][i] / max_orbes * alto * 0.9)
                pygame.draw.line(screen, ROJO, (x1, y1_rojo), (x2, y2_rojo), 3)

            max_label = font_mini.render(f"{int(max_orbes)}", True, TEXTO_SUAVE)
            screen.blit(max_label, (x_inicio + 5, y_inicio + 5))

        def dibujar_tablero():
            nonlocal FONDO, AZUL, ROJO, NARANJA, PANEL, TEXTO, TEXTO_SUAVE, VERDE

            screen.fill(FONDO)

            # Título
            titulo = font_titulo.render("⚡ CHAIN REACTION", True, NARANJA)
            screen.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))

            # Tema actual
            tema_texto = font_mini.render(f"Tema: {TEMAS[tema_actual]['nombre']} (T)", True, TEXTO_SUAVE)
            screen.blit(tema_texto, (20, 20))

            # Score
            orbes_azul = self.tablero.contar_orbes(Tablero.JUGADOR_AZUL)
            orbes_rojo = self.tablero.contar_orbes(Tablero.JUGADOR_ROJO)
            score_texto = font_grande.render(f"🔵 {orbes_azul}  -  {orbes_rojo} 🔴", True, TEXTO)
            screen.blit(score_texto, (ANCHO // 2 - score_texto.get_width() // 2, 75))

            # Panel derecho
            y_panel = PANEL_SUPERIOR + 20
            x_panel = MARGEN + self.tablero.NUM_COLUMNAS * TAM_CELDA + 30

            if not self.game_over:
                turno_texto = "Tu turno" if self.turno_actual == Tablero.JUGADOR_AZUL else "Turno IA"
                color_turno = AZUL if self.turno_actual == Tablero.JUGADOR_AZUL else ROJO
                texto = font_mediana.render(turno_texto, True, color_turno)
                screen.blit(texto, (x_panel, y_panel))

                y_panel += 60
                info = font_pequeña.render("Masa Crítica:", True, TEXTO)
                screen.blit(info, (x_panel, y_panel))
                for i, (label, val) in enumerate([("Esquinas", 2), ("Bordes", 3), ("Centro", 4)]):
                    y_panel += 22
                    screen.blit(font_pequeña.render(f"{label}: {val}", True, TEXTO_SUAVE), (x_panel, y_panel))

                y_panel += 50
                celdas_azul = self.tablero.contar_celdas(Tablero.JUGADOR_AZUL)
                celdas_rojo = self.tablero.contar_celdas(Tablero.JUGADOR_ROJO)
                screen.blit(font_pequeña.render("Celdas:", True, TEXTO), (x_panel, y_panel))
                y_panel += 25
                screen.blit(font_pequeña.render(f"🔵 {celdas_azul}  🔴 {celdas_rojo}", True, TEXTO), (x_panel, y_panel))

                y_panel += 60
                screen.blit(font_pequeña.render("Evolución:", True, TEXTO), (x_panel, y_panel))
                y_panel += 30
                dibujar_grafico_evolucion(x_panel, y_panel, 240, 120)

                y_panel += 140
                screen.blit(font_pequeña.render("Estadísticas:", True, TEXTO), (x_panel, y_panel))
                y_panel += 25
                screen.blit(font_mini.render(f"Partidas: {self.estadisticas['partidas_jugadas']}", True, TEXTO_SUAVE),
                            (x_panel, y_panel))
                y_panel += 20
                screen.blit(font_mini.render(
                    f"Récord: {self.estadisticas['victorias_humano']}V - {self.estadisticas['victorias_ia']}D",
                    True, TEXTO_SUAVE), (x_panel, y_panel))
                y_panel += 20
                if self.estadisticas['mayor_cadena_sesion'] > 0:
                    screen.blit(
                        font_mini.render(f"Mayor cadena: {self.estadisticas['mayor_cadena_sesion']}", True, NARANJA),
                        (x_panel, y_panel))

            # Tablero
            for fila in range(self.tablero.NUM_FILAS):
                for col in range(self.tablero.NUM_COLUMNAS):
                    x = col * TAM_CELDA + MARGEN
                    y = fila * TAM_CELDA + MARGEN + PANEL_SUPERIOR

                    rect = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)
                    pygame.draw.rect(screen, GRIS, rect)
                    pygame.draw.rect(screen, GRIS_OSCURO, rect, 3)

                    masa = self.tablero.tablero[fila][col].masa_critica
                    screen.blit(font_pequeña.render(str(masa), True, GRIS_OSCURO), (x + 5, y + 5))

                    celda = self.tablero.tablero[fila][col]
                    if celda.orbes > 0:
                        dibujar_orbes_en_celda(x, y, celda.orbes, celda.color)

            # ← NUEVA: Dibujar ondas
            for onda in ondas[:]:
                onda.actualizar()
                if onda.vida <= 0:
                    ondas.remove(onda)
                else:
                    onda.dibujar(screen)

            # ← NUEVA: Dibujar destellos
            for destello in destellos[:]:
                destello.actualizar()
                if destello.vida <= 0:
                    destellos.remove(destello)
                else:
                    destello.dibujar(screen)

            # Partículas
            for particula in particulas[:]:
                particula.actualizar()
                if particula.vida <= 0:
                    particulas.remove(particula)
                else:
                    particula.dibujar(screen)

            pygame.display.update()

        def obtener_celda_click(pos_mouse):
            x, y = pos_mouse
            col = (x - MARGEN) // TAM_CELDA
            fila = (y - MARGEN - PANEL_SUPERIOR) // TAM_CELDA
            if 0 <= fila < self.tablero.NUM_FILAS and 0 <= col < self.tablero.NUM_COLUMNAS:
                return (fila, col)
            return None

        def animar_explosiones(explosiones_por_generacion):
            """
            FIX: Ahora crea UNA SOLA explosión simbólica por generación
            No por cada celda, sino como efecto visual global
            """
            cadena_actual = len(explosiones_por_generacion)
            if cadena_actual > self.estadisticas['mayor_cadena_sesion']:
                self.estadisticas['mayor_cadena_sesion'] = cadena_actual
            if cadena_actual > self.estadisticas['mayor_cadena']:
                self.estadisticas['mayor_cadena'] = cadena_actual

            for generacion in explosiones_por_generacion:
                # ← FIX: Calcular centro de masas de todas las explosiones
                x_promedio = sum(col * TAM_CELDA + MARGEN + TAM_CELDA // 2 for _, col in generacion) / len(generacion)
                y_promedio = sum(
                    fila * TAM_CELDA + MARGEN + PANEL_SUPERIOR + TAM_CELDA // 2 for fila, _ in generacion) / len(
                    generacion)

                color = AZUL if self.turno_actual == Tablero.JUGADOR_AZUL else ROJO

                # ← Una sola explosión simbólica en el centro
                crear_explosion_simbolica(x_promedio, y_promedio, color)

                for _ in range(5):
                    dibujar_tablero()
                    clock.tick(60)
                pygame.time.wait(50)

        def mostrar_pantalla_final(ganador):
            """Muestra la pantalla de victoria"""
            self.estadisticas['partidas_jugadas'] += 1
            tiempo_partida = time.time() - self.tiempo_inicio_partida
            self.estadisticas['tiempo_total'] += tiempo_partida
            self.estadisticas['tiempo_promedio'] = self.estadisticas['tiempo_total'] / self.estadisticas[
                'partidas_jugadas']

            if ganador == Tablero.JUGADOR_AZUL:
                self.estadisticas['victorias_humano'] += 1
            elif ganador == Tablero.JUGADOR_ROJO:
                self.estadisticas['victorias_ia'] += 1

            # Loop de pantalla final
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            return True  # Nueva partida
                        elif event.key == pygame.K_ESCAPE:
                            return False  # Salir

                overlay = pygame.Surface((ANCHO, ALTO))
                overlay.set_alpha(200)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))

                texto = font_grande.render("🎉 ¡GANASTE! 🎉" if ganador == Tablero.JUGADOR_AZUL else "🤖 IA GANA 🤖",
                                           True, VERDE if ganador == Tablero.JUGADOR_AZUL else ROJO)
                screen.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 150))

                orbes_azul = self.tablero.contar_orbes(Tablero.JUGADOR_AZUL)
                orbes_rojo = self.tablero.contar_orbes(Tablero.JUGADOR_ROJO)
                score_final = font_mediana.render(f"🔵 {orbes_azul} - {orbes_rojo} 🔴", True, BLANCO)
                screen.blit(score_final, (ANCHO // 2 - score_final.get_width() // 2, ALTO // 2 - 80))

                y_stats = ALTO // 2 - 20
                stats_titulo = font_pequeña.render("═══ ESTADÍSTICAS ═══", True, NARANJA)
                screen.blit(stats_titulo, (ANCHO // 2 - stats_titulo.get_width() // 2, y_stats))
                y_stats += 35

                stats_lines = [
                    f"Partidas jugadas: {self.estadisticas['partidas_jugadas']}",
                    f"Récord: {self.estadisticas['victorias_humano']} victorias - {self.estadisticas['victorias_ia']} derrotas",
                    f"Mayor reacción en cadena: {self.estadisticas['mayor_cadena']} explosiones 💥" if self.estadisticas[
                                                                                                          'mayor_cadena'] > 0 else None,
                    f"Duración: {int(tiempo_partida)}s | Promedio: {int(self.estadisticas['tiempo_promedio'])}s"
                ]

                for line in filter(None, stats_lines):
                    texto_stat = font_pequeña.render(line, True, (255, 215, 0) if "reacción" in line else BLANCO)
                    screen.blit(texto_stat, (ANCHO // 2 - texto_stat.get_width() // 2, y_stats))
                    y_stats += 30

                y_stats += 20
                inst1 = font_pequeña.render("ESPACIO = Nueva | ESC = Salir | T = Tema", True, BLANCO)
                screen.blit(inst1, (ANCHO // 2 - inst1.get_width() // 2, y_stats))

                pygame.display.update()
                clock.tick(30)

        # ════════════════════════════════════════════════════════════════════════════════
        # MAIN LOOP
        # ════════════════════════════════════════════════════════════════════════════════
        self.tiempo_inicio_partida = time.time()
        dibujar_tablero()
        animando = False
        running = True

        while running:
            clock.tick(60)

            ganador = self.tablero.hay_ganador()
            if ganador is not None and not self.game_over:
                self.game_over = True
                continuar = mostrar_pantalla_final(ganador)
                if continuar:
                    self.tablero = Tablero()
                    self.turno_actual = Tablero.JUGADOR_AZUL
                    self.game_over = False
                    self.historial_orbes = {'azul': [], 'rojo': [], 'turnos': []}
                    self.tiempo_inicio_partida = time.time()
                    self.estadisticas['mayor_cadena_sesion'] = 0
                    particulas.clear()
                    ondas.clear()
                    destellos.clear()
                    dibujar_tablero()
                else:
                    running = False
                continue

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    idx_tema = (idx_tema + 1) % len(temas_lista)
                    tema_actual = temas_lista[idx_tema]
                    FONDO, AZUL, ROJO, NARANJA, PANEL, TEXTO, TEXTO_SUAVE, VERDE = actualizar_colores()
                    dibujar_tablero()

                # Click del jugador
                if event.type == pygame.MOUSEBUTTONDOWN and not animando and not self.game_over:
                    if self.turno_actual == Tablero.JUGADOR_AZUL:
                        celda = obtener_celda_click(event.pos)

                        if celda:
                            fila, col = celda

                            if self.tablero.movimiento_valido(fila, col, Tablero.JUGADOR_AZUL):
                                animando = True
                                explosiones = self.tablero.colocar_orbe(fila, col, Tablero.JUGADOR_AZUL)

                                if explosiones:
                                    animar_explosiones(explosiones)

                                dibujar_tablero()

                                ganador_inmediato = self.tablero.hay_ganador()
                                if ganador_inmediato is not None:
                                    self.game_over = True
                                    animando = False
                                else:
                                    self.cambiar_turno()
                                    animando = False

            # Turno IA
            if self.turno_actual == Tablero.JUGADOR_ROJO and not self.game_over and not animando:
                animando = True
                self.tiempo_inicio = time.time()

                movimientos_ia = self.tablero.obtener_movimientos_validos(Tablero.JUGADOR_ROJO)
                if not movimientos_ia:
                    self.game_over = True
                    animando = False
                    continue

                orbes_azul = self.tablero.contar_orbes(Tablero.JUGADOR_AZUL)
                orbes_rojo = self.tablero.contar_orbes(Tablero.JUGADOR_ROJO)
                ratio = orbes_azul / max(orbes_rojo, 1) if orbes_rojo > 0 else 999

                # Modo rápido
                if ratio > 4 or orbes_rojo < 8 or len(movimientos_ia) < 10:
                    overlay = pygame.Surface((ANCHO, ALTO))
                    overlay.set_alpha(150)
                    overlay.fill(FONDO)
                    screen.blit(overlay, (0, 0))
                    mensaje = font_mediana.render("IA último movimiento...", True, ROJO)
                    screen.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))
                    pygame.display.update()

                    movimientos_con_orbes = [(f, c) for f, c in movimientos_ia if self.tablero.tablero[f][c].orbes > 0]
                    movimiento = random.choice(
                        movimientos_con_orbes if movimientos_con_orbes else movimientos_ia) if movimientos_ia else None
                    pygame.time.wait(100)

                else:
                    movimiento_calculado = [None]
                    calculo_terminado = threading.Event()

                    def calcular_movimiento_ia():
                        try:
                            profundidad = self.obtener_profundidad_dinamica()
                            mov, _ = self.minimax(self.tablero, profundidad, -math.inf, math.inf, True)
                            movimiento_calculado[0] = mov
                        except:
                            pass
                        finally:
                            calculo_terminado.set()

                    thread_ia = threading.Thread(target=calcular_movimiento_ia)
                    thread_ia.daemon = True
                    thread_ia.start()

                    tiempo_max = 1.0
                    tiempo_transcurrido = 0

                    while not calculo_terminado.is_set() and tiempo_transcurrido < tiempo_max:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                animando = False
                                break

                        overlay = pygame.Surface((ANCHO, ALTO))
                        overlay.set_alpha(150)
                        overlay.fill(FONDO)
                        screen.blit(overlay, (0, 0))

                        num_puntos = int(tiempo_transcurrido * 3) % 4
                        puntos = "." * num_puntos
                        pensando = font_mediana.render(f"IA pensando{puntos}", True, NARANJA)
                        screen.blit(pensando, (ANCHO // 2 - pensando.get_width() // 2, ALTO // 2))

                        pygame.display.update()
                        clock.tick(30)
                        tiempo_transcurrido = time.time() - self.tiempo_inicio

                    thread_ia.join(timeout=0.2)
                    movimiento = movimiento_calculado[0]

                    if movimiento is None:
                        movimientos = self.tablero.obtener_movimientos_validos(Tablero.JUGADOR_ROJO)
                        movimiento = random.choice(movimientos) if movimientos else None

                if movimiento:
                    fila, col = movimiento
                    explosiones = self.tablero.colocar_orbe(fila, col, Tablero.JUGADOR_ROJO)

                    if explosiones:
                        animar_explosiones(explosiones)

                    dibujar_tablero()

                    ganador_ia = self.tablero.hay_ganador()
                    if ganador_ia is not None:
                        self.game_over = True
                    else:
                        self.cambiar_turno()

                animando = False

            if not animando and not self.game_over:
                dibujar_tablero()

        pygame.quit()


if __name__ == "__main__":
    print("=" * 75)
    print("⚡ CHAIN REACTION - EXPLOSIONES SIMBÓLICAS ⚡")
    print("=" * 75)
    print("\n✨ Mejoras de Explosiones:")
    print("  • Ondas expansivas elegantes")
    print("  • Destellos luminosos")
    print("  • Pocas partículas (no sobrecargadas)")
    print("  • Efecto visual limpio y profesional")
    print("\n🎮 Controles:")
    print("  • CLICK en celda para colocar orbe")
    print("  • T = Cambiar tema")
    print("  • ESPACIO = Nueva partida")
    print("  • ESC = Salir")
    print("\n" + "=" * 75)

    juego = ChainReaction(profundidad=3)
    juego.jugar_gui()