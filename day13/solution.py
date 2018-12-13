from PIL import Image
import re

def draw(tracks):
  width = len(tracks[0])
  height = len(tracks)

  img = Image.new('RGB', (width * 3, height * 3), (50, 50, 50))
  pix = img.load()
  for y in range(height):
    for x in range(width):
      if tracks[y][x] == '|':
        pix[x * 3 + 0, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 0] = (0, 0, 0)
        pix[x * 3 + 2, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 0, y * 3 + 1] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 1] = (0, 0, 0)
        pix[x * 3 + 2, y * 3 + 1] = (255, 255, 255)
        pix[x * 3 + 0, y * 3 + 2] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 2] = (0, 0, 0)
        pix[x * 3 + 2, y * 3 + 2] = (255, 255, 255)
      if tracks[y][x] == '-':
        pix[x * 3 + 0, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 2, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 0, y * 3 + 1] = (0, 0, 0)
        pix[x * 3 + 1, y * 3 + 1] = (0, 0, 0)
        pix[x * 3 + 2, y * 3 + 1] = (0, 0, 0)
        pix[x * 3 + 0, y * 3 + 2] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 2] = (255, 255, 255)
        pix[x * 3 + 2, y * 3 + 2] = (255, 255, 255)
      if tracks[y][x] == '\\':
        pix[x * 3 + 0, y * 3 + 0] = (0, 0, 0)
        pix[x * 3 + 1, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 2, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 0, y * 3 + 1] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 1] = (0, 0, 0)
        pix[x * 3 + 2, y * 3 + 1] = (255, 255, 255)
        pix[x * 3 + 0, y * 3 + 2] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 2] = (255, 255, 255)
        pix[x * 3 + 2, y * 3 + 2] = (0, 0, 0)
      if tracks[y][x] == '/':
        pix[x * 3 + 0, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 2, y * 3 + 0] = (0, 0, 0)
        pix[x * 3 + 0, y * 3 + 1] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 1] = (0, 0, 0)
        pix[x * 3 + 2, y * 3 + 1] = (255, 255, 255)
        pix[x * 3 + 0, y * 3 + 2] = (0, 0, 0)
        pix[x * 3 + 1, y * 3 + 2] = (255, 255, 255)
        pix[x * 3 + 2, y * 3 + 2] = (255, 255, 255)
      if tracks[y][x] == '+':
        pix[x * 3 + 0, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 0] = (0, 0, 0)
        pix[x * 3 + 2, y * 3 + 0] = (255, 255, 255)
        pix[x * 3 + 0, y * 3 + 1] = (0, 0, 0)
        pix[x * 3 + 1, y * 3 + 1] = (0, 0, 0)
        pix[x * 3 + 2, y * 3 + 1] = (0, 0, 0)
        pix[x * 3 + 0, y * 3 + 2] = (255, 255, 255)
        pix[x * 3 + 1, y * 3 + 2] = (0, 0, 0)
        pix[x * 3 + 2, y * 3 + 2] = (255, 255, 255)
  img.save('result.png')

with open('./input.txt') as f:
  tracks = [[x for x in line if x != '\n'] for line in f.readlines()]
  carts = []
  for y in range(len(tracks)):
    for x in range(len(tracks[y])):
      if tracks[y][x] in '^v<>':
        carts.append((y,x,tracks[y][x]))
        if tracks[y][x-1] in '-\\/+' and tracks[y][x+1] in '-\\/+' and tracks[y-1][x] in '|/\\+' and tracks[y+1][x] in '|/\\+':
          tracks[y][x] = '+'
        if tracks[y][x-1] in '-\\/+' and tracks[y][x+1] in '-\\/+':
          tracks[y][x] = '-'
        elif tracks[y-1][x] in '|\\/+' and tracks[y+1][x] in '|\\/+':
          tracks[y][x] = '|'
        elif tracks[y][x-1] in '-\\/':
          tracks[y][x] = '/'
        elif tracks[y][x+1] in '-/\\':
          tracks[y][x] = '\\'
        elif tracks[y+1][x] in '|\\/':
          tracks[y][x] = '/'
        elif tracks[y-1][x] in '|/\\':
          tracks[y][x] = '\\'

  draw(tracks)
  print carts