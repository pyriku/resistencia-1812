# -*- coding: utf-8 -*-
###############################################################################
# This file is part of Resistencia Cadiz 1812.                                #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# any later version.                                                          #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
# Copyright (C) 2010, Pablo Recio Quijano, <pablo.recioquijano@alum.uca.es>   #
###############################################################################

"""
This file contains the definition of functions used on the clips environment.
"""

import clips

from resistencia import logger
from resistencia import log_filename
__log__ = logger.getlog('libguadalete.clips_functions', log_filename)


def _file_new_turn (filename, turn):
    """Writes the turn number on a given file.

    Keyword arguments:
    filename -- System path to the file into we want to write
    turn -- Integer with the turn number
    """
    f = open(filename, 'a')
    f.write('tiempo ' + str(turn))
    __log__.debug('Init turn number ' + str(turn) + ' on "' + filename + '"')
    f.close()


def _file_new_piece (filename, team, nid, value, x, y, covered):
    """ Writes a line on the given file with the piece's values

    Keyword arguments:
    filename -- System path to the file into we want to write
    team -- Team identificator. Must be 'A' or 'B'
    nid -- Piece identificator. It deppends of each system expert developer
    value -- Numeric value of the piece.
    x - Position on the X axis.
    y - Position on the Y axis.
    covered - Identifies if the piece is covered for the rival or not.
    """
    line = 'e:' + team + ' n:' + nid + ' p:' + value \
           + ' x:' + x + ' y:' + y + ' d:' + covered + "\n"
    f = open(filename, 'a')
    f.write(line)
    __log__.debug('Writed line "' + line + '" on "' + filename + '"')
    f.close()


def _clips_distancia():
    """Clips distance function definition.

    Allows to load on the CLIPS environment a function to calculate the distance
    between two positions on the board.
    """
    # First function name
    fun_name = 'distancia'
    # Parameters for the function
    fun_param = '?x1 ?y1 ?x2 ?y2'
    # Function body
    fun_body = '(sqrt (+ (* (- ?x1 ?x2) (- ?x1 ?x2))' \
               '(* (- ?y1 ?y2) (- ?y1 ?y2))))'
    clips.BuildFunction(fun_name, fun_param, fun_body)


def _clips_dentro():
    # Function name
    fun_name = 'dentro'
    # Function parameters
    fun_param  = '?x1 ?y1 ?x2 ?y2 ?x ?y'
    # Function body
    fun_body  = '(and (or (<= ?x1 ?x ?x2) (>= ?x1 ?x ?x2))' \
                '(or (<= ?y1 ?y ?y2) (>= ?y1 ?y ?y2)))'
    # Building the function
    clips.BuildFunction(fun_name, fun_param, fun_body)


def _clips_minimo():
    fun_name = 'minimo'
    fun_param = '?n1 ?n2'
    fun_body = '(if (< ?n1 ?n2) then '\
               '?n1 '\
               'else '\
               '?n2)'
    clips.BuildFunction(fun_name, fun_param, fun_body)


def _clips_mov_x():
    fun_name = 'mov-x'
    fun_param = '?m'
    fun_body = '(switch ?m' \
               '(case 1 then 1)' \
               '(case 2 then -1)' \
               '(default 0))'
    clips.BuildFunction(fun_name, fun_param, fun_body)


def _clips_mov_y():
    fun_name = 'mov-y'
    fun_param = '?m'
    fun_body = '(switch ?m' \
               '(case 3 then 1)' \
               '(case 4 then -1)' \
               '(default 0))'
    clips.BuildFunction(fun_name, fun_param, fun_body)


def _clips_mov_valido():
    fun_name = 'mov-valido'
    fun_param = '?dim ?m ?x ?y'
    fun_body = '(and (> (+ ?x (mov-x ?m)) 0) (<= (+ ?x (mov-x ?m)) ?dim)' \
               '(> (+ ?y (mov-y ?m)) 0) (<= (+ ?y (mov-y ?m)) ?dim))'
    clips.BuildFunction(fun_name, fun_param, fun_body)


def _clips_valor():
    fun_name = 'valor'
    fun_param = '?descubierto'
    fun_body = '(if (= 0 ?descubierto) then ' \
               '"?" ' \
               'else ' \
               '" ")'
    clips.BuildFunction(fun_name, fun_param, fun_body)


def _clips_simetrico():
    fun_name = 'simetrico'
    fun_param  = '?m'
    fun_body  = '(switch ?m' \
                '(case 1 then 2)' \
                '(case 2 then 1)' \
                '(case 3 then 4)' \
                '(case 4 then 3)' \
                '(default 0))'
    clips.BuildFunction(fun_name, fun_param, fun_body)


def _clips_sim():
    fun_name = 'sim'
    fun_param = '?p'
    fun_body  = '(- 9 ?p)'
    clips.BuildFunction(fun_name, fun_param, fun_body)


def _clips_turno():
    fun_name = 'turno'
    fun_param = '?ti ?ta'
    fun_body = '(if (= (mod (- ?ti ?ta) 2) 1) then ' \
               '"A" ' \
               'else ' \
               '"B") '
    clips.BuildFunction(fun_name, fun_param, fun_body)

# This list contains all the functions that initializes something on clips
__functions__ = {'distancia': _clips_distancia,
                 'dentro': _clips_dentro,
                 'minimo': _clips_minimo,
                 'mov-x': _clips_mov_x,
                 'mov-y': _clips_mov_y,
                 'mov-valido': _clips_mov_valido,
                 'valor': _clips_valor,
                 'simetrico': _clips_simetrico,
                 'sim': _clips_sim,
                 'turno': _clips_turno}

def init_module():
    """This function initialize the clips function of this module. You shouldn't
    add functions to the module after init it.
    """
    clips.RegisterPythonFunction(_file_new_turn, 'a-fichero-tiempo')
    clips.RegisterPythonFunction(_file_new_piece, 'a-fichero-jugador')

    for k, f in __functions__:
        f()

def add_clips_function(function):
    """Add some user-defined function to this module, so it will be loaded on
    the clips environment once the module is initialize.

    Keywords arguments:
    function -- Must be a function that build a function on PyCLIPS as
    clips.BuildFunction(fun_name, fun_param, fun_body)
    """
    # TODO - Do some checks that 'function' is an initialization of a
    #        clips function.

    key = function[0]
    f = function[1]
    
    __functions__[key] = f

def remove_clips_function(function_key):
    """Remove a function of this module.
    """
    # TODO - Catch exception if the function is not on the list
    del __functions__[function_key]
