#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
import random

def random_room(p_list):
	a_list=random.sample(p_list,2)
	for i in a_list:
		sys.stdout.write(i+' ')
		p_list.remove(i)
	print
	return p_list

p_list=['ÇÇÈñ½Ü','ÕÔË§Áì','ÓíÌÎ','ÑîÎÀÎº','Íõ³É','»ÆÀÚ','ÎâĞ¡»ª','ºú²ı¸Õ']
random_room(p_list)
random_room(p_list)
random_room(p_list)
random_room(p_list)