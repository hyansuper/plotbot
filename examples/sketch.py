from linedraw import linedraw
from io import BytesIO

def to_sketch(frame, draw_contours=True, draw_hatch=False, resolution=720, hatch_size = 16, contour_simplify=1):
    bs = BytesIO(frame)
    bs.seek(0)
    frame = linedraw.Image.open(bs)
    w,h = frame.size
    frame = frame.convert("L")
    frame = linedraw.ImageOps.autocontrast(frame,10)
    lines = []
    if draw_contours:
        lines += linedraw.getcontours(frame.resize((int(resolution/contour_simplify),int(resolution/contour_simplify*h/w))),contour_simplify)
    if draw_hatch:
        lines += linedraw.hatch(frame.resize((int(resolution/hatch_size),int(resolution/hatch_size*h/w))),hatch_size)
    lines = linedraw.sortlines(lines)
    return lines