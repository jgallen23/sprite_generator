#!/usr/bin/env python
import os
import sys
import yaml
import Image

ROOT = os.getcwd()

def read_config(config_file):
    config = yaml.load(file(config_file))

    def parse_sprite_config(sprite_config):
        max_width = 0
        height = 0
        for image in sprite_config['images']:
            image['image'] = Image.open(os.path.join(sprite_config['base_dir'], image['file']))
            image['size'] = image['image'].size
            if image.has_key('top_padding'):
                height += image['top_padding']
            image['y_position'] = height

            height += image['size'][1]

            if image.has_key('bottom_padding'):
                height += image['bottom_padding']

            if image['size'][0] > max_width:
                max_width = image['size'][0]

        sprite_config['width'] = max_width
        sprite_config['height'] = height

    for sprite_config in config['sprites']:
        sprite_config['stylesheet_dir'] = config['stylesheet_dir']
        sprite_config['sprite_dir'] = config['sprite_dir']
        sprite_config['sprite_path'] = config['sprite_path']
        parse_sprite_config(sprite_config)

    return config

def create_sprites(config):
    for sprite_config in config['sprites']:
        create_sprite(sprite_config)

def create_sprite(sprite_config):
    current_y = 0
    img = Image.new('RGBA', (sprite_config['width'], sprite_config['height']))
    for image in sprite_config['images']:
        if image.has_key('align'):
            if image['align'] == "right":
                x = sprite_config['width'] - image['size'][0]
            if image['align'] == "center":
                x = (sprite_config['width'] - image['size'][0])/2
        else:
            x = 0
        img.paste(image['image'], (x, image['y_position']))
    path = "%s/%s.png" % (sprite_config['sprite_dir'], sprite_config['name'])
    img.save(path, quality = 100)

def create_stylesheets(config):
    for sprite_config in config['sprites']:
        create_stylesheet(sprite_config)

def create_stylesheet(sprite_config):
    f = open('%s/%s.css' % (sprite_config['stylesheet_dir'], sprite_config['name']), 'w')
    css = "%s { background: url(%s/%s.png) no-repeat %s %spx; }\n"
    for image in sprite_config['images']:
        if image.has_key('align'):
            x = image['align']
        else:
            x = 0
        y = -float(image['y_position'])
        if sprite_config.has_key('scale'):
            y = y * sprite_config['scale']
        if sprite_config.has_key('offset_y'):
            y += sprite_config['offset_y']
        if x == 0 and sprite_config.has_key('offset_x'):
            x += sprite_config['offset_x']
            x = str(x) + "px"
        f.write(css % (image['selector'], sprite_config['sprite_path'], sprite_config['name'], x, y))
    f.close()

def main(args):
    if len(args) == 0:
        config_file = "config.yaml"
    else:
        config_file = args[0]
    config = read_config(config_file)
    create_sprites(config)
    create_stylesheets(config)

if __name__ == "__main__": main(sys.argv[1:])

