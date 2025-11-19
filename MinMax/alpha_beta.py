# -*- coding: utf-8 -*-
"""
CHAIN REACTION ⚡ - VERSIÓN CORREGIDA (sin bucle infinito)
"""

import numpy as np
import pygame
import sys
import math
import random
import time
from typing import List, Tuple, Optional


class Celda:
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
        """VERSIÓN CORREGIDA con límite de generaciones"""
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
        generacion_num = 0
        MAX_GENERACIONES = 1000  # ← LÍMITE DE SEGURIDAD

        while explosiones and generacion_num < MAX_GENERACIONES:
            generacion_num += 1

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

        if generacion_num >= MAX_GENERACIONES:
            print(f"⚠️ WARNING: Alcanzado límite de {MAX_GENERACIONES} generaciones - posible bucle infinito evitado")

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

        if not tiene_orbes_azul and tiene_orbes_rojo:
            return self.JUGADOR_ROJO
        elif not tiene_orbes_rojo and tiene_orbes_azul:
            return self.JUGADOR_AZUL

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


class ChainReaction:
    def __init__(self, profundidad: int = 4):
        self.PROFUNDIDAD_MAX = profundidad
        self.tablero = Tablero()
        self.turno_actual = Tablero.JUGADOR_AZUL
        self.game_over = False
        self.tiempo_inicio = 0
        self.tiempo_inicio_partida = 0
        self.nodos_evaluados = 0
        self.LIMITE_NODOS = 500
        self.TIEMPO_MAX_IA = 0.3

        self.estadisticas = {
            'partidas_jugadas': 0,
            'victorias_humano': 0,
            'victorias_ia': 0,
            'mayor_cadena': 0,
            'mayor_cadena_sesion': 0,
            'tiempo_total': 0,
            'tiempo_promedio': 0
        }

        self.historial_orbes = {'azul': [], 'rojo': [], 'turnos': []}

    def minimax(self, tablero: Tablero, profundidad: int,
                alpha: float, beta: float, maximizando: bool) -> Tuple[Optional[Tuple[int, int]], float]:
        self.nodos_evaluados += 1

        if self.nodos_evaluados > self.LIMITE_NODOS:
            return (None, tablero.evaluar_posicion(Tablero.JUGADOR_ROJO))

        if time.time() - self.tiempo_inicio > self.TIEMPO_MAX_IA:
            return (None, tablero.evaluar_posicion(Tablero.JUGADOR_ROJO))

        ganador = tablero.hay_ganador()
        jugador = Tablero.JUGADOR_ROJO if maximizando else Tablero.JUGADOR_AZUL
        movimientos_validos = tablero.obtener_movimientos_validos(jugador)

        if ganador is not None:
            return (None, 1000000 if ganador == Tablero.JUGADOR_ROJO else -1000000)

        if profundidad == 0 or not movimientos_validos:
            return (None, tablero.evaluar_posicion(Tablero.JUGADOR_ROJO))

        if len(movimientos_validos) > 2:
            movimientos_con_score = []
            for fila, col in movimientos_validos:
                score = tablero.tablero[fila][col].orbes * 10
                if tablero.tablero[fila][col].orbes == tablero.tablero[fila][col].masa_critica - 1:
                    score += 50
                movimientos_con_score.append((score, fila, col))

            movimientos_con_score.sort(reverse=True)
            movimientos_validos = [(f, c) for _, f, c in movimientos_con_score[:2]]

        if maximizando:
            valor = -math.inf
            mejor_movimiento = movimientos_validos[0] if movimientos_validos else None

            for fila, col in movimientos_validos:
                if self.nodos_evaluados > self.LIMITE_NODOS or time.time() - self.tiempo_inicio > self.TIEMPO_MAX_IA:
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
            mejor_movimiento = movimientos_validos[0] if movimientos_validos else None

            for fila, col in movimientos_validos:
                if self.nodos_evaluados > self.LIMITE_NODOS or time.time() - self.tiempo_inicio > self.TIEMPO_MAX_IA:
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

    def elegir_movimiento_ia(self) -> Optional[Tuple[int, int]]:
        orbes_totales = self.tablero.contar_orbes(Tablero.JUGADOR_AZUL) + \
                        self.tablero.contar_orbes(Tablero.JUGADOR_ROJO)

        movimientos = self.tablero.obtener_movimientos_validos(Tablero.JUGADOR_ROJO)
        if not movimientos:
            return None

        if orbes_totales <= 10:
            self.tiempo_inicio = time.time()
            self.nodos_evaluados = 0

            profundidad = 2 if orbes_totales < 5 else 1
            movimiento, _ = self.minimax(self.tablero, profundidad, -math.inf, math.inf, True)

            tiempo_usado = time.time() - self.tiempo_inicio
            print(f"Minimax: Prof={profundidad}, Nodos={self.nodos_evaluados}, Tiempo={tiempo_usado:.3f}s")

            return movimiento if movimiento else random.choice(movimientos)

        else:
            print(f"Heurística (orbes={orbes_totales})")

            mejor_movimiento = None
            mejor_score = -999999

            for fila, col in movimientos:
                score = 0
                celda = self.tablero.tablero[fila][col]

                if celda.orbes > 0:
                    score += celda.orbes * 100

                if celda.orbes == celda.masa_critica - 1:
                    score += 500

                if score > mejor_score:
                    mejor_score = score
                    mejor_movimiento = (fila, col)

            return mejor_movimiento if mejor_movimiento else random.choice(movimientos)

    def cambiar_turno(self):
        self.turno_actual = Tablero.JUGADOR_ROJO if self.turno_actual == Tablero.JUGADOR_AZUL else Tablero.JUGADOR_AZUL
        self.historial_orbes['azul'].append(self.tablero.contar_orbes(Tablero.JUGADOR_AZUL))
        self.historial_orbes['rojo'].append(self.tablero.contar_orbes(Tablero.JUGADOR_ROJO))
        self.historial_orbes['turnos'].append(len(self.historial_orbes['azul']))

    def jugar_gui(self):
        pygame.init()

        TEMAS = {
            'clasico': {'nombre': 'Clásico', 'fondo': (255, 255, 255), 'jugador1': (30, 144, 255),
                        'jugador2': (255, 69, 69), 'acento': (255, 140, 0), 'panel': (245, 245, 245),
                        'texto': (0, 0, 0), 'texto_suave': (100, 100, 100), 'victoria': (50, 205, 50)}
        }

        temas_lista = list(TEMAS.keys())
        idx_tema = 0
        tema_actual = temas_lista[idx_tema]

        def actualizar_colores():
            return (TEMAS[tema_actual]['fondo'], TEMAS[tema_actual]['jugador1'],
                    TEMAS[tema_actual]['jugador2'], TEMAS[tema_actual]['acento'],
                    TEMAS[tema_actual]['panel'], TEMAS[tema_actual]['texto'],
                    TEMAS[tema_actual]['texto_suave'], TEMAS[tema_actual]['victoria'])

        FONDO, AZUL, ROJO, NARANJA, PANEL, TEXTO, TEXTO_SUAVE, VERDE = actualizar_colores()
        BLANCO, GRIS, GRIS_OSCURO = (255, 255, 255), (200, 200, 200), (100, 100, 100)

        TAM_CELDA, RADIO_ORBE, MARGEN = 100, 14, 60
        PANEL_SUPERIOR, PANEL_DERECHO = 120, 300
        ANCHO = self.tablero.NUM_COLUMNAS * TAM_CELDA + MARGEN * 2 + PANEL_DERECHO
        ALTO = self.tablero.NUM_FILAS * TAM_CELDA + MARGEN * 2 + PANEL_SUPERIOR

        screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("⚡ CHAIN REACTION - SIN BUCLE INFINITO")
        clock = pygame.time.Clock()

        font_titulo = pygame.font.SysFont("Arial", 48, bold=True)
        font_grande = pygame.font.SysFont("Arial", 36, bold=True)
        font_mediana = pygame.font.SysFont("Arial", 24)
        font_pequeña = pygame.font.SysFont("Arial", 18)
        font_mini = pygame.font.SysFont("Arial", 14)

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
            screen.fill(FONDO)
            titulo = font_titulo.render("⚡ CHAIN REACTION", True, NARANJA)
            screen.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 20))

            tema_texto = font_mini.render(f"Tema: {TEMAS[tema_actual]['nombre']} (T)", True, TEXTO_SUAVE)
            screen.blit(tema_texto, (20, 20))

            orbes_azul = self.tablero.contar_orbes(Tablero.JUGADOR_AZUL)
            orbes_rojo = self.tablero.contar_orbes(Tablero.JUGADOR_ROJO)
            score_texto = font_grande.render(f"🔵 {orbes_azul}  -  {orbes_rojo} 🔴", True, TEXTO)
            screen.blit(score_texto, (ANCHO // 2 - score_texto.get_width() // 2, 75))

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
                y_panel += 25
                info2 = font_pequeña.render("Esquinas: 2", True, TEXTO_SUAVE)
                screen.blit(info2, (x_panel, y_panel))
                y_panel += 22
                info3 = font_pequeña.render("Bordes: 3", True, TEXTO_SUAVE)
                screen.blit(info3, (x_panel, y_panel))
                y_panel += 22
                info4 = font_pequeña.render("Centro: 4", True, TEXTO_SUAVE)
                screen.blit(info4, (x_panel, y_panel))

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

            pygame.display.update()

        def obtener_celda_click(pos_mouse):
            x, y = pos_mouse
            col = (x - MARGEN) // TAM_CELDA
            fila = (y - MARGEN - PANEL_SUPERIOR) // TAM_CELDA
            if 0 <= fila < self.tablero.NUM_FILAS and 0 <= col < self.tablero.NUM_COLUMNAS:
                return (fila, col)
            return None

        def animar_explosiones(explosiones_por_generacion):
            """Animación INSTANTÁNEA sin bucles"""
            cadena_actual = len(explosiones_por_generacion)
            if cadena_actual > self.estadisticas['mayor_cadena_sesion']:
                self.estadisticas['mayor_cadena_sesion'] = cadena_actual
            if cadena_actual > self.estadisticas['mayor_cadena']:
                self.estadisticas['mayor_cadena'] = cadena_actual

            if len(explosiones_por_generacion) > 0:
                overlay = pygame.Surface((ANCHO, ALTO))
                overlay.set_alpha(50)
                color_flash = AZUL if self.turno_actual == Tablero.JUGADOR_AZUL else ROJO
                overlay.fill(color_flash)
                screen.blit(overlay, (0, 0))

                if len(explosiones_por_generacion) > 5:
                    mensaje = font_grande.render(f"💥 {len(explosiones_por_generacion)} explosiones", True, BLANCO)
                    screen.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))

                pygame.display.update()
                pygame.time.wait(150)

        def mostrar_pantalla_final(ganador):
            self.estadisticas['partidas_jugadas'] += 1
            tiempo_partida = time.time() - self.tiempo_inicio_partida
            self.estadisticas['tiempo_total'] += tiempo_partida
            self.estadisticas['tiempo_promedio'] = self.estadisticas['tiempo_total'] / self.estadisticas[
                'partidas_jugadas']

            if ganador == Tablero.JUGADOR_AZUL:
                self.estadisticas['victorias_humano'] += 1
            elif ganador == Tablero.JUGADOR_ROJO:
                self.estadisticas['victorias_ia'] += 1

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

            partidas = font_pequeña.render(f"Partidas jugadas: {self.estadisticas['partidas_jugadas']}", True, BLANCO)
            screen.blit(partidas, (ANCHO // 2 - partidas.get_width() // 2, y_stats))
            y_stats += 30

            record = font_pequeña.render(
                f"Récord: {self.estadisticas['victorias_humano']} victorias - {self.estadisticas['victorias_ia']} derrotas",
                True, BLANCO
            )
            screen.blit(record, (ANCHO // 2 - record.get_width() // 2, y_stats))
            y_stats += 30

            if self.estadisticas['mayor_cadena'] > 0:
                cadena = font_pequeña.render(
                    f"Mayor reacción en cadena: {self.estadisticas['mayor_cadena']} explosiones 💥",
                    True, (255, 215, 0)
                )
                screen.blit(cadena, (ANCHO // 2 - cadena.get_width() // 2, y_stats))
                y_stats += 30

            tiempo_texto = font_pequeña.render(
                f"Duración: {int(tiempo_partida)}s | Promedio: {int(self.estadisticas['tiempo_promedio'])}s",
                True, BLANCO
            )
            screen.blit(tiempo_texto, (ANCHO // 2 - tiempo_texto.get_width() // 2, y_stats))

            y_stats += 50
            inst1 = font_pequeña.render("ESPACIO = Nueva | ESC = Salir | T = Tema", True, BLANCO)
            screen.blit(inst1, (ANCHO // 2 - inst1.get_width() // 2, y_stats))

            pygame.display.update()

        self.tiempo_inicio_partida = time.time()
        dibujar_tablero()
        animando = False
        running = True

        while running:
            clock.tick(30)

            ganador = self.tablero.hay_ganador()
            if ganador and not self.game_over:
                self.game_over = True
                mostrar_pantalla_final(ganador)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    idx_tema = (idx_tema + 1) % len(temas_lista)
                    tema_actual = temas_lista[idx_tema]
                    FONDO, AZUL, ROJO, NARANJA, PANEL, TEXTO, TEXTO_SUAVE, VERDE = actualizar_colores()
                    dibujar_tablero()

                if self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.tablero = Tablero()
                            self.turno_actual = Tablero.JUGADOR_AZUL
                            self.game_over = False
                            self.historial_orbes = {'azul': [], 'rojo': [], 'turnos': []}
                            self.tiempo_inicio_partida = time.time()
                            self.estadisticas['mayor_cadena_sesion'] = 0
                            dibujar_tablero()
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN and not animando:
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
                                pygame.display.update()
                                pygame.time.wait(150)

                                ganador_inmediato = self.tablero.hay_ganador()
                                if ganador_inmediato is not None:
                                    self.game_over = True
                                    mostrar_pantalla_final(ganador_inmediato)
                                else:
                                    self.cambiar_turno()

                                animando = False

            if self.turno_actual == Tablero.JUGADOR_ROJO and not self.game_over and not animando:
                if self.tablero.hay_ganador() is not None:
                    continue

                animando = True

                movimiento = self.elegir_movimiento_ia()

                if movimiento:
                    fila, col = movimiento
                    explosiones = self.tablero.colocar_orbe(fila, col, Tablero.JUGADOR_ROJO)

                    if explosiones:
                        animar_explosiones(explosiones)

                    dibujar_tablero()
                    pygame.display.update()
                    pygame.time.wait(120)

                    ganador_inmediato = self.tablero.hay_ganador()
                    if ganador_inmediato is not None:
                        self.game_over = True
                        mostrar_pantalla_final(ganador_inmediato)
                    else:
                        self.cambiar_turno()

                animando = False

            if not animando and not self.game_over:
                dibujar_tablero()

        pygame.quit()


if __name__ == "__main__":
    print("=" * 75)
    print("⚡ CHAIN REACTION - SIN BUCLE INFINITO ⚡")
    print("=" * 75)
    print("\n✅ CORRECCIONES:")
    print("  - Límite de 1000 generaciones en explosiones")
    print("  - Animación instantánea (sin partículas)")
    print("  - Minimax con poda alfa-beta")
    print("=" * 75 + "\n")

    juego = ChainReaction(profundidad=4)
    juego.jugar_gui()