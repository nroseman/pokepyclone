from os import walk
import pygame

def import_file_dict(path):
    surf_dict = {}

    for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    surf_dict[name] = []
            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    file_path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(file_path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    surf_dict[key].append(surf)
    return surf_dict
