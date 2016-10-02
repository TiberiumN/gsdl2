import math

from .sdllibs import sdl_lib
from .sdlffi import sdl_ffi
from .rect import Rect
from .color import Color
from .sdlconstants import SDL_BYTEORDER, SDL_BIG_ENDIAN, SDL_LIL_ENDIAN


debug = 0


def trunc(d):
    # (((d) >= 0.0) ? (floor(d)) : (ceil(d)))
    return math.floor(d) if d >= 0.0 else math.ceil(d)


def FRAC(z):
    return z - trunc(z)


def INVFRAC(z):
    return 1 - FRAC(z)


def aaline():
    # TODO
    if debug:
        print('gsdl.draw.aaline')


# static PyObject* aaline(PyObject* self, PyObject* arg)
# {
# 	PyObject *surfobj, *colorobj, *start, *end;
# 	SDL_Surface* surf;
# 	float startx, starty, endx, endy;
# 	int top, left, bottom, right;
# 	int blend=1;
# 	float pts[4];
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int anydraw;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OOO|i", &PySurface_Type, &surfobj, &colorobj, &start, &end, &blend))
# 		return NULL;
# 	surf = PySurface_AsSurface(surfobj);
#
# 	if(surf->format->BytesPerPixel !=3 && surf->format->BytesPerPixel != 4)
# 		return RAISE(PyExc_ValueError, "unsupported bit depth for aaline draw (supports 32 & 24 bit)");
#
# 	if(RGBAFromColorObj(colorobj, rgba))
# 		color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
# 	else
# 		return RAISE(PyExc_TypeError, "invalid color argument");
#
# 	if(!TwoFloatsFromObj(start, &startx, &starty))
# 		return RAISE(PyExc_TypeError, "Invalid start position argument");
# 	if(!TwoFloatsFromObj(end, &endx, &endy))
# 		return RAISE(PyExc_TypeError, "Invalid end position argument");
#
# 	if(!PySurface_Lock(surfobj)) return NULL;
#
# 	pts[0] = startx; pts[1] = starty;
# 	pts[2] = endx; pts[3] = endy;
# 	anydraw = clip_and_draw_aaline(surf, &surf->clip_rect, color, pts, blend);
#
# 	if(!PySurface_Unlock(surfobj)) return NULL;
#
# 	/*compute return rect*/
# 	if(!anydraw)
# 		return PyRect_New4(startx, starty, 0, 0);
# 	if(pts[0] < pts[2])
# 	{
# 		left = (int)(pts[0]);
# 		right = (int)(pts[2]);
# 	}
# 	else
# 	{
# 		left = (int)(pts[2]);
# 		right = (int)(pts[0]);
# 	}
# 	if(pts[1] < pts[3])
# 	{
# 		top = (int)(pts[1]);
# 		bottom = (int)(pts[3]);
# 	}
# 	else
# 	{
# 		top = (int)(pts[3]);
# 		bottom = (int)(pts[1]);
# 	}
# 	return PyRect_New4(left, top, right-left+2, bottom-top+2);
# }


def line(surface, color, start_pos, end_pos, width=1):
    # TODO
    if debug:
        print('gsdl.draw.line')
    # PyObject *surfobj, *colorobj, *start, *end;
    # SDL_Surface* surf;
    # int startx, starty, endx, endy;
    startx, starty = start_pos
    endx, endy = end_pos
    # int dx, dy;
    # int rtop, rleft, rwidth, rheight;
    # int width = 1;
    # int pts[4];
    pts = [0] * 4
    # Uint8 rgba[4];
    # Uint32 color;
    # int anydraw;

    # get all the arguments
    surf = surface.sdl_surface

    if surf.format.BytesPerPixel <= 0 or surf.format.BytesPerPixel > 4:
        # TODO: proper exception
        raise Exception("unsupport bit depth for line draw")

    # if(PyInt_Check(colorobj))
    #     color = (Uint32)PyInt_AsLong(colorobj);
    # else if(RGBAFromColorObj(colorobj, rgba))
    #     color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
    # else
    #     return RAISE(PyExc_TypeError, "invalid color argument");

    # if(!TwoIntsFromObj(start, &startx, &starty))
    #     return RAISE(PyExc_TypeError, "Invalid start position argument");
    # if(!TwoIntsFromObj(end, &endx, &endy))
    #     return RAISE(PyExc_TypeError, "Invalid end position argument");

    if width < 1:
        return Rect(startx, starty, 0, 0)

    surface.lock()

    pts[0:2] = startx, starty
    pts[2:4] = endx, endy
    anydraw = clip_and_draw_line_width(surface, surf.clip_rect, color, width, pts)

    surface.unlock()

    # compute return rect
    if not anydraw:
        return Rect(startx, starty, 0, 0)
    rleft = startx if startx < endx else endx
    rtop = starty if starty < endy else endy
    dx = abs(startx - endx)
    dy = abs(starty - endy)
    if dx > dy:
        rwidth = dx + 1
        rheight = dy + width
    else:
        rwidth = dx + width
        rheight = dy + 1

    return Rect(rleft, rtop, rwidth, rheight)


# static PyObject* line(PyObject* self, PyObject* arg)
# {
# 	PyObject *surfobj, *colorobj, *start, *end;
# 	SDL_Surface* surf;
# 	int startx, starty, endx, endy;
# 	int top, left, bottom, right;
# 	int width = 1;
# 	int pts[4];
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int anydraw;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OOO|i", &PySurface_Type, &surfobj, &colorobj, &start, &end, &width))
# 		return NULL;
# 	surf = PySurface_AsSurface(surfobj);
#
# 	if(surf->format->BytesPerPixel <= 0 || surf->format->BytesPerPixel > 4)
# 		return RAISE(PyExc_ValueError, "unsupport bit depth for line draw");
#
# 	if(PyInt_Check(colorobj))
# 		color = (Uint32)PyInt_AsLong(colorobj);
# 	else if(RGBAFromColorObj(colorobj, rgba))
# 		color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
# 	else
# 		return RAISE(PyExc_TypeError, "invalid color argument");
#
# 	if(!TwoIntsFromObj(start, &startx, &starty))
# 		return RAISE(PyExc_TypeError, "Invalid start position argument");
# 	if(!TwoIntsFromObj(end, &endx, &endy))
# 		return RAISE(PyExc_TypeError, "Invalid end position argument");
#
# 	if(width < 1)
# 		return PyRect_New4(startx, starty, 0, 0);
#
#
# 	if(!PySurface_Lock(surfobj)) return NULL;
#
# 	pts[0] = startx; pts[1] = starty;
# 	pts[2] = endx; pts[3] = endy;
# 	anydraw = clip_and_draw_line_width(surf, &surf->clip_rect, color, width, pts);
#
# 	if(!PySurface_Unlock(surfobj)) return NULL;
#
#
# 	/*compute return rect*/
# 	if(!anydraw)
# 		return PyRect_New4(startx, starty, 0, 0);
# 	if(pts[0] < pts[2])
# 	{
# 		left = pts[0];
# 		right = pts[2];
# 	}
# 	else
# 	{
# 		left = pts[2];
# 		right = pts[0];
# 	}
# 	if(pts[1] < pts[3])
# 	{
# 		top = pts[1];
# 		bottom = pts[3];
# 	}
# 	else
# 	{
# 		top = pts[3];
# 		bottom = pts[1];
# 	}
# 	return PyRect_New4(left, top, right-left+1, bottom-top+1);
# }


def aalines():
    # TODO
    if debug:
        print('gsdl.draw.aalines')


# static PyObject* aalines(PyObject* self, PyObject* arg)
# {
# 	PyObject *surfobj, *colorobj, *closedobj, *points, *item;
# 	SDL_Surface* surf;
# 	float x, y;
# 	int top, left, bottom, right;
# 	float pts[4];
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int closed, blend;
# 	int result, loop, length, drawn;
# 	float startx, starty;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OOO|i", &PySurface_Type, &surfobj, &colorobj, &closedobj,
# 		&points, &blend))
# 		return NULL;
# 	surf = PySurface_AsSurface(surfobj);
#
# 	if(surf->format->BytesPerPixel !=3 && surf->format->BytesPerPixel != 4)
# 		return RAISE(PyExc_ValueError, "unsupported bit depth for aaline draw (supports 32 & 24 bit)");
#
# 	if(RGBAFromColorObj(colorobj, rgba))
# 		color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
# 	else
# 		return RAISE(PyExc_TypeError, "invalid color argument");
#
# 	closed = PyObject_IsTrue(closedobj);
#
# 	if(!PySequence_Check(points))
# 		return RAISE(PyExc_TypeError, "points argument must be a sequence of number pairs");
# 	length = PySequence_Length(points);
# 	if(length < 2)
# 		return RAISE(PyExc_ValueError, "points argument must contain more than 1 points");
#
# 	item = PySequence_GetItem(points, 0);
# 	result = TwoFloatsFromObj(item, &x, &y);
# 	Py_DECREF(item);
# 	if(!result) return RAISE(PyExc_TypeError, "points must be number pairs");
#
# 	startx = pts[0] = x;
# 	starty = pts[1] = y;
# 	left = right = (int)x;
# 	top = bottom = (int)y;
#
# 	if(!PySurface_Lock(surfobj)) return NULL;
#
# 	drawn = 1;
# 	for(loop = 1; loop < length; ++loop)
# 	{
# 		item = PySequence_GetItem(points, loop);
# 		result = TwoFloatsFromObj(item, &x, &y);
# 		Py_DECREF(item);
# 		if(!result) continue; /*note, we silently skip over bad points :[ */
# 		++drawn;
# 		pts[0] = startx;
# 		pts[1] = starty;
# 		startx = pts[2] = x;
# 		starty = pts[3] = y;
# 		if(clip_and_draw_aaline(surf, &surf->clip_rect, color, pts, blend))
# 		{
# 			left = MIN((int)MIN(pts[0], pts[2]), left);
# 			top = MIN((int)MIN(pts[1], pts[3]), top);
# 			right = MAX((int)MAX(pts[0], pts[2]), right);
# 			bottom = MAX((int)MAX(pts[1], pts[3]), bottom);
# 		}
# 	}
# 	if(closed && drawn > 2)
# 	{
# 		item = PySequence_GetItem(points, 0);
# 		result = TwoFloatsFromObj(item, &x, &y);
# 		Py_DECREF(item);
# 		if(result)
# 		{
# 			pts[0] = startx;
# 			pts[1] = starty;
# 			pts[2] = x;
# 			pts[3] = y;
# 			clip_and_draw_aaline(surf, &surf->clip_rect, color, pts, blend);
# 		}
# 	}
#
# 	if(!PySurface_Unlock(surfobj)) return NULL;
#
# 	/*compute return rect*/
# 	return PyRect_New4(left, top, right-left+2, bottom-top+2);
# }


def lines(surface, color, closed, pointlist, width=1):
    if debug:
        print('gsdl2.draw.lines')
# 	PyObject *surfobj, *colorobj, *closedobj, *points, *item;
# 	SDL_Surface* surf;
# 	int x, y;
# 	int top, left, bottom, right;
# 	int pts[4], width=1;
    pts = [0] * 4
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int closed;
# 	int result, loop, length, drawn;
# 	int startx, starty;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OOO|i", &PySurface_Type, &surfobj, &colorobj, &closedobj, &points, &width))
# 		return NULL;
# 	surf = PySurface_AsSurface(surfobj);
    surf = surface.sdl_surface

# 	if(surf->format->BytesPerPixel <= 0 || surf->format->BytesPerPixel > 4)
# 		return RAISE(PyExc_ValueError, "unsupport bit depth for line draw");
    if surf.format.BytesPerPixel <= 0 or surf.format.BytesPerPixel > 4:
        # TODO: real exception
        raise Exception("unsupport bit depth for line draw")

# TODO: error checking
# 	if(PyInt_Check(colorobj))
# 		color = (Uint32)PyInt_AsLong(colorobj);
# 	else if(RGBAFromColorObj(colorobj, rgba))
# 		color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
# 	else
# 		return RAISE(PyExc_TypeError, "invalid color argument");
#
# 	closed = PyObject_IsTrue(closedobj);
#
# 	if(!PySequence_Check(points))
# 		return RAISE(PyExc_TypeError, "points argument must be a sequence of number pairs");
# 	length = PySequence_Length(points);
    length = len(pointlist)
# 	if(length < 2)
# 		return RAISE(PyExc_ValueError, "points argument must contain more than 1 points");
#
# 	item = PySequence_GetItem(points, 0);
# 	result = TwoIntsFromObj(item, &x, &y);
# 	Py_DECREF(item);
# 	if(!result) return RAISE(PyExc_TypeError, "points must be number pairs");
    x, y = pointlist[0]

# 	startx = pts[0] = left = right = x;
# 	starty = pts[1] = top = bottom = y;
    startx = pts[0] = left = right = x
    starty = pts[1] = top = bottom = y

# 	if(width < 1)
# 		return PyRect_New4(left, top, 0, 0);
    if width < 1:
        return Rect(left, top, 0, 0)

# 	if(!PySurface_Lock(surfobj)) return NULL;
    surface.lock()

# 	drawn = 1;
# 	for(loop = 1; loop < length; ++loop)
#   {
    drawn = 1
    for loop in range(length):
# 		item = PySequence_GetItem(points, loop);
# 		result = TwoIntsFromObj(item, &x, &y);
# 		Py_DECREF(item);
# 		if(!result) continue; /*note, we silently skip over bad points :[ */
# 		++drawn;
# 		pts[0] = startx;
# 		pts[1] = starty;
# 		startx = pts[2] = x;
# 		starty = pts[3] = y;
        x, y = pointlist[loop]
        drawn += 1
        pts[0] = startx
        pts[1] = starty
        startx = pts[2] = x
        starty = pts[3] = y

# 		if(clip_and_draw_line_width(surf, &surf->clip_rect, color, width, pts))
# 		{
# 			left = MIN(MIN(pts[0], pts[2]), left);
# 			top = MIN(MIN(pts[1], pts[3]), top);
# 			right = MAX(MAX(pts[0], pts[2]), right);
# 			bottom = MAX(MAX(pts[1], pts[3]), bottom);
# 		}
# 	}
        if clip_and_draw_line_width(surface, surf.clip_rect, color, width, pts):
            left = min(min(pts[0], pts[2]), left)
            top = min(min(pts[1], pts[3]), top)
            right = max(max(pts[0], pts[2]), right)
            bottom = max(max(pts[1], pts[3]), bottom)

# 	if(closed && drawn > 2)
# 	{
# 		item = PySequence_GetItem(points, 0);
# 		result = TwoIntsFromObj(item, &x, &y);
# 		Py_DECREF(item);
# 		if(result)
# 		{
# 			pts[0] = startx;
# 			pts[1] = starty;
# 			pts[2] = x;
# 			pts[3] = y;
# 			clip_and_draw_line_width(surf, &surf->clip_rect, color, width, pts);
# 		}
# 	}
    if closed and drawn > 2:
        x, y = pointlist[0]
        pts[0] = startx
        pts[1] = starty
        pts[2] = x
        pts[3] = y
        clip_and_draw_line_width(surface, surf.clip_rect, color, width, pts)

# 	if(!PySurface_Unlock(surfobj)) return NULL;
    surface.unlock()

# 	/*compute return rect*/
# 	return PyRect_New4(left, top, right-left+1, bottom-top+1);
    return Rect(left, top, right - left + 1, bottom - top + 1)


# static PyObject* lines(PyObject* self, PyObject* arg)
# {
# 	PyObject *surfobj, *colorobj, *closedobj, *points, *item;
# 	SDL_Surface* surf;
# 	int x, y;
# 	int top, left, bottom, right;
# 	int pts[4], width=1;
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int closed;
# 	int result, loop, length, drawn;
# 	int startx, starty;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OOO|i", &PySurface_Type, &surfobj, &colorobj, &closedobj, &points, &width))
# 		return NULL;
# 	surf = PySurface_AsSurface(surfobj);
#
# 	if(surf->format->BytesPerPixel <= 0 || surf->format->BytesPerPixel > 4)
# 		return RAISE(PyExc_ValueError, "unsupport bit depth for line draw");
#
# 	if(PyInt_Check(colorobj))
# 		color = (Uint32)PyInt_AsLong(colorobj);
# 	else if(RGBAFromColorObj(colorobj, rgba))
# 		color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
# 	else
# 		return RAISE(PyExc_TypeError, "invalid color argument");
#
# 	closed = PyObject_IsTrue(closedobj);
#
# 	if(!PySequence_Check(points))
# 		return RAISE(PyExc_TypeError, "points argument must be a sequence of number pairs");
# 	length = PySequence_Length(points);
# 	if(length < 2)
# 		return RAISE(PyExc_ValueError, "points argument must contain more than 1 points");
#
# 	item = PySequence_GetItem(points, 0);
# 	result = TwoIntsFromObj(item, &x, &y);
# 	Py_DECREF(item);
# 	if(!result) return RAISE(PyExc_TypeError, "points must be number pairs");
#
# 	startx = pts[0] = left = right = x;
# 	starty = pts[1] = top = bottom = y;
#
# 	if(width < 1)
# 		return PyRect_New4(left, top, 0, 0);
#
# 	if(!PySurface_Lock(surfobj)) return NULL;
#
# 	drawn = 1;
# 	for(loop = 1; loop < length; ++loop)
# 	{
# 		item = PySequence_GetItem(points, loop);
# 		result = TwoIntsFromObj(item, &x, &y);
# 		Py_DECREF(item);
# 		if(!result) continue; /*note, we silently skip over bad points :[ */
# 		++drawn;
# 		pts[0] = startx;
# 		pts[1] = starty;
# 		startx = pts[2] = x;
# 		starty = pts[3] = y;
# 		if(clip_and_draw_line_width(surf, &surf->clip_rect, color, width, pts))
# 		{
# 			left = MIN(MIN(pts[0], pts[2]), left);
# 			top = MIN(MIN(pts[1], pts[3]), top);
# 			right = MAX(MAX(pts[0], pts[2]), right);
# 			bottom = MAX(MAX(pts[1], pts[3]), bottom);
# 		}
# 	}
# 	if(closed && drawn > 2)
# 	{
# 		item = PySequence_GetItem(points, 0);
# 		result = TwoIntsFromObj(item, &x, &y);
# 		Py_DECREF(item);
# 		if(result)
# 		{
# 			pts[0] = startx;
# 			pts[1] = starty;
# 			pts[2] = x;
# 			pts[3] = y;
# 			clip_and_draw_line_width(surf, &surf->clip_rect, color, width, pts);
# 		}
# 	}
#
#
# 	if(!PySurface_Unlock(surfobj)) return NULL;
#
# 	/*compute return rect*/
# 	return PyRect_New4(left, top, right-left+1, bottom-top+1);
# }


def arc(surface, color, rect, start_angle, stop_angle, width=1):
    # TODO
    if debug:
        print('gsdl.draw.arc')
# 	PyObject *surfobj, *colorobj, *rectobj;
# 	GAME_Rect *rect, temp;
# 	SDL_Surface* surf;
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int width=1, loop, t, l, b, r;
# 	double angle_start, angle_stop;
    surf = surface.sdl_surface

    # get all the arguments
    # if(!PyArg_ParseTuple(arg, "O!OOdd|i", &PySurface_Type, &surfobj, &colorobj, &rectobj,
    #                               &angle_start, &angle_stop, &width))
    #     return NULL;
    # rect = GameRect_FromObject(rectobj, &temp);
    # if(!rect)
    #     return RAISE(PyExc_TypeError, "Invalid recstyle argument");

    # surf = PySurface_AsSurface(surfobj);
    # if(surf->format->BytesPerPixel <= 0 || surf->format->BytesPerPixel > 4)
    #     return RAISE(PyExc_ValueError, "unsupport bit depth for drawing");

    # if(PyInt_Check(colorobj))
    #     color = (Uint32)PyInt_AsLong(colorobj);
    # else if(RGBAFromColorObj(colorobj, rgba))
    #     color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
    # else
    #     return RAISE(PyExc_TypeError, "invalid color argument");

    if width < 0:
        # TODO: proper exception
        raise Exception("negative width")
    if width > rect.w / 2 or width > rect.h / 2:
        # TODO: proper exception
        raise Exception("width greater than ellipse radius")
    # FIXME: this is supposed to be radians?
    # if stop_angle < start_angle:
    #     stop_angle += 360

    surface.lock()

    width = min(width, min(rect.w, rect.h) / 2)
    # for(loop=0; loop<width; ++loop)
    # FIXME: ++loop a bug?
    for loop in range(0, width):
        loop += 1
        draw_arc(surface, rect.x + rect.w / 2, rect.y + rect.h / 2,
                 rect.w / 2 - loop, rect.h / 2 - loop,
                 start_angle, stop_angle, color)

    surface.unlock()

    l = max(rect.x, surf.clip_rect.x)
    t = max(rect.y, surf.clip_rect.y)
    r = min(rect.x + rect.w, surf.clip_rect.x + surf.clip_rect.w)
    b = min(rect.y + rect.h, surf.clip_rect.y + surf.clip_rect.h)
    return Rect(l, t, max(r - l, 0), max(b - t, 0))


# static PyObject* arc(PyObject* self, PyObject* arg)
# {
# 	PyObject *surfobj, *colorobj, *rectobj;
# 	GAME_Rect *rect, temp;
# 	SDL_Surface* surf;
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int width=1, loop, t, l, b, r;
# 	double angle_start, angle_stop;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OOdd|i", &PySurface_Type, &surfobj, &colorobj, &rectobj,
# 			                      &angle_start, &angle_stop, &width))
# 		return NULL;
# 	rect = GameRect_FromObject(rectobj, &temp);
# 	if(!rect)
# 		return RAISE(PyExc_TypeError, "Invalid recstyle argument");
#
# 	surf = PySurface_AsSurface(surfobj);
# 	if(surf->format->BytesPerPixel <= 0 || surf->format->BytesPerPixel > 4)
# 		return RAISE(PyExc_ValueError, "unsupport bit depth for drawing");
#
# 	if(PyInt_Check(colorobj))
# 		color = (Uint32)PyInt_AsLong(colorobj);
# 	else if(RGBAFromColorObj(colorobj, rgba))
# 		color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
# 	else
# 		return RAISE(PyExc_TypeError, "invalid color argument");
#
# 	if ( width < 0 )
# 		return RAISE(PyExc_ValueError, "negative width");
# 	if ( width > rect->w / 2 || width > rect->h / 2 )
# 		return RAISE(PyExc_ValueError, "width greater than ellipse radius");
# 	if ( angle_stop < angle_start )
# 		angle_stop += 360;
#
# 	if(!PySurface_Lock(surfobj)) return NULL;
#
# 	width = MIN(width, MIN(rect->w, rect->h) / 2);
# 	for(loop=0; loop<width; ++loop)
# 	{
# 		draw_arc(surf, rect->x+rect->w/2, rect->y+rect->h/2,
# 			 rect->w/2-loop, rect->h/2-loop,
# 			 angle_start, angle_stop, color);
# 	}
#
# 	if(!PySurface_Unlock(surfobj)) return NULL;
#
# 	l = MAX(rect->x, surf->clip_rect.x);
# 	t = MAX(rect->y, surf->clip_rect.y);
# 	r = MIN(rect->x + rect->w, surf->clip_rect.x + surf->clip_rect.w);
# 	b = MIN(rect->y + rect->h, surf->clip_rect.y + surf->clip_rect.h);
# 	return PyRect_New4(l, t, MAX(r-l, 0), MAX(b-t, 0));
# }


def ellipse(surface, color, rect, width=0):
    # TODO
    if debug:
        print('gsdl.draw.ellipse')
# 	PyObject *surfobj, *colorobj, *rectobj;
# 	GAME_Rect *rect, temp;
# 	SDL_Surface* surf;
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int width=0, loop, t, l, b, r;

    # rect = GameRect_FromObject(rectobj, &temp);
    # if(!rect)
    # 	return RAISE(PyExc_TypeError, "Invalid recstyle argument");

    surf = surface.sdl_surface
    if surf.format.BytesPerPixel <= 0 or surf.format.BytesPerPixel > 4:
        # TODO: proper exception
        raise Exception("unsupport bit depth for drawing")

    if width < 0:
        # TODO: proper exception
        raise Exception("negative width")
    if width > rect.w / 2 or width > rect.h / 2:
        # TODO: proper exception
        raise Exception("width greater than ellipse radius")

    surface.lock()

    if not width:
        draw_fillellipse(surface, rect.x + rect.w / 2, rect.y + rect.h / 2, rect.w / 2, rect.h / 2, color)
    else:
        width = min(width, min(rect.w, rect.h) / 2)
        for loop in range(width):
            draw_ellipse(surface, rect.x + rect.w / 2, rect.y + rect.h / 2, rect.w / 2 - loop, rect.h / 2 - loop, color)

    surface.unlock()

    l = max(rect.x, surf.clip_rect.x)
    t = max(rect.y, surf.clip_rect.y)
    r = min(rect.x + rect.w, surf.clip_rect.x + surf.clip_rect.w)
    b = min(rect.y + rect.h, surf.clip_rect.y + surf.clip_rect.h)
    return Rect(l, t, max(r - l, 0), max(b - t, 0))


# static PyObject* ellipse(PyObject* self, PyObject* arg)
# {
# 	PyObject *surfobj, *colorobj, *rectobj;
# 	GAME_Rect *rect, temp;
# 	SDL_Surface* surf;
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int width=0, loop, t, l, b, r;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OO|i", &PySurface_Type, &surfobj, &colorobj, &rectobj, &width))
# 		return NULL;
# 	rect = GameRect_FromObject(rectobj, &temp);
# 	if(!rect)
# 		return RAISE(PyExc_TypeError, "Invalid recstyle argument");
#
# 	surf = PySurface_AsSurface(surfobj);
# 	if(surf->format->BytesPerPixel <= 0 || surf->format->BytesPerPixel > 4)
# 		return RAISE(PyExc_ValueError, "unsupport bit depth for drawing");
#
# 	if(PyInt_Check(colorobj))
# 		color = (Uint32)PyInt_AsLong(colorobj);
# 	else if(RGBAFromColorObj(colorobj, rgba))
# 		color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
# 	else
# 		return RAISE(PyExc_TypeError, "invalid color argument");
#
# 	if ( width < 0 )
# 		return RAISE(PyExc_ValueError, "negative width");
# 	if ( width > rect->w / 2 || width > rect->h / 2 )
# 		return RAISE(PyExc_ValueError, "width greater than ellipse radius");
#
# 	if(!PySurface_Lock(surfobj)) return NULL;
#
# 	if(!width)
# 		draw_fillellipse(surf, (Sint16)(rect->x+rect->w/2), (Sint16)(rect->y+rect->h/2),
# 					(Sint16)(rect->w/2), (Sint16)(rect->h/2), color);
# 	else
# 	{
# 		width = MIN(width, MIN(rect->w, rect->h) / 2);
# 		for(loop=0; loop<width; ++loop)
# 		{
# 			draw_ellipse(surf, rect->x+rect->w/2, rect->y+rect->h/2,
# 						rect->w/2-loop, rect->h/2-loop, color);
# 		}
# 	}
#
# 	if(!PySurface_Unlock(surfobj)) return NULL;
#
# 	l = MAX(rect->x, surf->clip_rect.x);
# 	t = MAX(rect->y, surf->clip_rect.y);
# 	r = MIN(rect->x + rect->w, surf->clip_rect.x + surf->clip_rect.w);
# 	b = MIN(rect->y + rect->h, surf->clip_rect.y + surf->clip_rect.h);
# 	return PyRect_New4(l, t, MAX(r-l, 0), MAX(b-t, 0));
# }


def circle(surface, color, center, radius, width=1):
    if debug:
        print('gsdl.draw.circle')
    surf = surface.sdl_surface
    # rgba = color.sdl_color
    posx, posy = center
    t = l = b = r = 0
    loop = 0

    # surf = PySurface_AsSurface(surfobj);
    if surf.format.BytesPerPixel <= 0 or surf.format.BytesPerPixel > 4:
        raise Exception("unsupport bit depth for drawing")  # TODO

    # TODO
    # if(PyInt_Check(colorobj))
    #     color = (Uint32)PyInt_AsLong(colorobj);
    # else if(RGBAFromColorObj(colorobj, rgba))
    #     color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
    # else
    #     return RAISE(PyExc_TypeError, "invalid color argument");
    # pixel = sdl_lib.SDL_MapRGBA(surf.format, color.r, color.g, color.b, color.a)

    # TODO
    # if ( radius < 0 )
    #     return RAISE(PyExc_ValueError, "negative radius");
    # if ( width < 0 )
    #     return RAISE(PyExc_ValueError, "negative width");
    # if ( width > radius )
    #     return RAISE(PyExc_ValueError, "width greater than radius");

    # if(!PySurface_Lock(surfobj)) return NULL;
    surface.lock()

    if not width:
        draw_fillellipse(surface, posx, posy, radius, radius, color)
    else:
        # for (loop=0; loop<width; ++loop)
        for loop in range(width):
            draw_ellipse(surface, posx, posy, radius - loop, radius - loop, color)

    surface.unlock()

    l = max(posx - radius, surf.clip_rect.x)
    t = max(posy - radius, surf.clip_rect.y)
    r = min(posx + radius, surf.clip_rect.x + surf.clip_rect.w)
    b = min(posy + radius, surf.clip_rect.y + surf.clip_rect.h)
    return Rect(l, t, max(r - l, 0), min(b - t, 0))


def polygon(surface, color, pointlist, width=1):
    if debug:
        print('gsdl2.draw.polygon')
# 	PyObject *surfobj, *colorobj, *points, *item;
# 	SDL_Surface* surf;
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int width=0, length, loop, numpoints;
# 	int *xlist, *ylist;
# 	int x, y, top, left, bottom, right, result;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OO|i", &PySurface_Type, &surfobj, &colorobj, &points, &width))
# 		return NULL;
#
# 	if(width)
# 	{
# 		PyObject *args, *ret;
# 		args = Py_BuildValue("(OOiOi)", surfobj, colorobj, 1, points, width);
# 		if(!args) return NULL;
# 		ret = lines(NULL, args);
# 		Py_DECREF(args);
# 		return ret;
# 	}
    if width:
        ret = lines(surface, color, 1, pointlist, width)
        return ret

# 	surf = PySurface_AsSurface(surfobj);
    surf = surface.sdl_surface

# 	if(surf->format->BytesPerPixel <= 0 || surf->format->BytesPerPixel > 4)
# 		return RAISE(PyExc_ValueError, "unsupport bit depth for line draw");
    if surf.format.BytesPerPixel <= 0 or surf.format.BytesPerPixel > 4:
        # TODO: real exception
        raise Exception("unsupport bit depth for line draw")

# 	if(PyInt_Check(colorobj))
# 		color = (Uint32)PyInt_AsLong(colorobj);
# 	else if(RGBAFromColorObj(colorobj, rgba))
# 		color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
# 	else
# 		return RAISE(PyExc_TypeError, "invalid color argument");

# 	if(!PySequence_Check(points))
# 		return RAISE(PyExc_TypeError, "points argument must be a sequence of number pairs");
# 	length = PySequence_Length(points);
# 	if(length < 3)
# 		return RAISE(PyExc_ValueError, "points argument must contain more than 2 points");
    length = len(pointlist)
    if length < 3:
        # TODO: real exception
        raise Exception("points argument must contain more than 2 points")

# 	item = PySequence_GetItem(points, 0);
# 	result = TwoIntsFromObj(item, &x, &y);
# 	Py_DECREF(item);
# 	if(!result) return RAISE(PyExc_TypeError, "points must be number pairs");
# 	left = right = x;
# 	top = bottom = y;
#
# 	xlist = PyMem_New(int, length);
# 	ylist = PyMem_New(int, length);
    x, y = pointlist[0]
    left = right = x
    top = bottom = y
    xlist = [0] * length
    ylist = [0] * length

# 	numpoints = 0;
# 	for(loop = 0; loop < length; ++loop)
# 	{
# 		item = PySequence_GetItem(points, loop);
# 		result = TwoIntsFromObj(item, &x, &y);
# 		Py_DECREF(item);
# 		if(!result) continue; /*note, we silently skip over bad points :[ */
# 		xlist[numpoints] = x;
# 		ylist[numpoints] = y;
# 		++numpoints;
# 		left = MIN(x, left);
# 		top = MIN(y, top);
# 		right = MAX(x, right);
# 		bottom = MAX(y, bottom);
# 	}
    numpoints = 0
    for loop in range(length):
        x, y = pointlist[loop]
        xlist[numpoints] = x
        ylist[numpoints] = y
        numpoints += 1
        left = min(x, left)
        top = min(y, top)
        right = max(x, right)
        bottom = max(y, bottom)

# 	if(!PySurface_Lock(surfobj))
# 	{
# 		PyMem_Del(xlist); PyMem_Del(ylist);
# 		return NULL;
# 	}
    surface.lock()

# 	draw_fillpoly(surf, xlist, ylist, numpoints, color);
    draw_fillpoly(surface, xlist, ylist, numpoints, color)

# 	PyMem_Del(xlist); PyMem_Del(ylist);
# 	if(!PySurface_Unlock(surfobj))
# 		return NULL;
    surface.unlock()

# 	left = MAX(left, surf->clip_rect.x);
# 	top = MAX(top, surf->clip_rect.y);
# 	right = MIN(right, surf->clip_rect.x + surf->clip_rect.w);
# 	bottom = MIN(bottom, surf->clip_rect.y + surf->clip_rect.h);
# 	return PyRect_New4(left, top, right-left+1, bottom-top+1);
    left = max(left, surf.clip_rect.x)
    top = max(top, surf.clip_rect.y)
    right = min(right, surf.clip_rect.x + surf.clip_rect.w)
    bottom = min(bottom, surf.clip_rect.y + surf.clip_rect.h)

    return Rect(left, top, right - left + 1, bottom - top + 1)


# static PyObject* polygon(PyObject* self, PyObject* arg)
# {
# 	PyObject *surfobj, *colorobj, *points, *item;
# 	SDL_Surface* surf;
# 	Uint8 rgba[4];
# 	Uint32 color;
# 	int width=0, length, loop, numpoints;
# 	int *xlist, *ylist;
# 	int x, y, top, left, bottom, right, result;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OO|i", &PySurface_Type, &surfobj, &colorobj, &points, &width))
# 		return NULL;
#
#
# 	if(width)
# 	{
# 		PyObject *args, *ret;
# 		args = Py_BuildValue("(OOiOi)", surfobj, colorobj, 1, points, width);
# 		if(!args) return NULL;
# 		ret = lines(NULL, args);
# 		Py_DECREF(args);
# 		return ret;
# 	}
#
#
# 	surf = PySurface_AsSurface(surfobj);
#
# 	if(surf->format->BytesPerPixel <= 0 || surf->format->BytesPerPixel > 4)
# 		return RAISE(PyExc_ValueError, "unsupport bit depth for line draw");
#
# 	if(PyInt_Check(colorobj))
# 		color = (Uint32)PyInt_AsLong(colorobj);
# 	else if(RGBAFromColorObj(colorobj, rgba))
# 		color = SDL_MapRGBA(surf->format, rgba[0], rgba[1], rgba[2], rgba[3]);
# 	else
# 		return RAISE(PyExc_TypeError, "invalid color argument");
#
# 	if(!PySequence_Check(points))
# 		return RAISE(PyExc_TypeError, "points argument must be a sequence of number pairs");
# 	length = PySequence_Length(points);
# 	if(length < 3)
# 		return RAISE(PyExc_ValueError, "points argument must contain more than 2 points");
#
#
# 	item = PySequence_GetItem(points, 0);
# 	result = TwoIntsFromObj(item, &x, &y);
# 	Py_DECREF(item);
# 	if(!result) return RAISE(PyExc_TypeError, "points must be number pairs");
# 	left = right = x;
# 	top = bottom = y;
#
# 	xlist = PyMem_New(int, length);
# 	ylist = PyMem_New(int, length);
#
# 	numpoints = 0;
# 	for(loop = 0; loop < length; ++loop)
# 	{
# 		item = PySequence_GetItem(points, loop);
# 		result = TwoIntsFromObj(item, &x, &y);
# 		Py_DECREF(item);
# 		if(!result) continue; /*note, we silently skip over bad points :[ */
# 		xlist[numpoints] = x;
# 		ylist[numpoints] = y;
# 		++numpoints;
# 		left = MIN(x, left);
# 		top = MIN(y, top);
# 		right = MAX(x, right);
# 		bottom = MAX(y, bottom);
# 	}
#
# 	if(!PySurface_Lock(surfobj))
# 	{
# 		PyMem_Del(xlist); PyMem_Del(ylist);
# 		return NULL;
# 	}
#
# 	draw_fillpoly(surf, xlist, ylist, numpoints, color);
#
# 	PyMem_Del(xlist); PyMem_Del(ylist);
# 	if(!PySurface_Unlock(surfobj))
# 		return NULL;
#
# 	left = MAX(left, surf->clip_rect.x);
# 	top = MAX(top, surf->clip_rect.y);
# 	right = MIN(right, surf->clip_rect.x + surf->clip_rect.w);
# 	bottom = MIN(bottom, surf->clip_rect.y + surf->clip_rect.h);
# 	return PyRect_New4(left, top, right-left+1, bottom-top+1);
# }


def rect(surface, color, rect, width=1):
    if debug:
        print('gsdl2.draw.rect')
# 	PyObject *surfobj, *colorobj, *rectobj, *points, *args, *ret=NULL;
# 	GAME_Rect* rect, temp;
# 	int t, l, b, r, width=0;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OO|i", &PySurface_Type, &surfobj, &colorobj, &rectobj, &width))
# 		return NULL;
#
# 	if(!(rect = GameRect_FromObject(rectobj, &temp)))
# 		return RAISE(PyExc_TypeError, "Rect argument is invalid");
#
    l = rect.x
    r = rect.right - 1
    t = rect.y
    b = rect.bottom - 1
#
# 	/*build the pointlist*/
# 	points = Py_BuildValue("((ii)(ii)(ii)(ii))", l, t, r, t, r, b, l, b);
    points = (l, t), (r, t), (r, b), (l, b)

# 	args = Py_BuildValue("(OONi)", surfobj, colorobj, points, width);
# 	if(args) ret = polygon(NULL, args);
    ret = polygon(surface, color, points, width)

# 	Py_XDECREF(args);
    return ret


# static PyObject* rect(PyObject* self, PyObject* arg)
# {
# 	PyObject *surfobj, *colorobj, *rectobj, *points, *args, *ret=NULL;
# 	GAME_Rect* rect, temp;
# 	int t, l, b, r, width=0;
#
# 	/*get all the arguments*/
# 	if(!PyArg_ParseTuple(arg, "O!OO|i", &PySurface_Type, &surfobj, &colorobj, &rectobj, &width))
# 		return NULL;
#
# 	if(!(rect = GameRect_FromObject(rectobj, &temp)))
# 		return RAISE(PyExc_TypeError, "Rect argument is invalid");
#
# 	l = rect->x; r = rect->x + rect->w - 1;
# 	t = rect->y; b = rect->y + rect->h - 1;
#
# 	/*build the pointlist*/
# 	points = Py_BuildValue("((ii)(ii)(ii)(ii))", l, t, r, t, r, b, l, b);
#
# 	args = Py_BuildValue("(OONi)", surfobj, colorobj, points, width);
# 	if(args) ret = polygon(NULL, args);
#
# 	Py_XDECREF(args);
# 	return ret;
# }


# internal drawing tools


def clip_and_draw_aaline():
    # TODO
    if debug:
        print('gsdl.draw.clip_and_draw_aaline')


# static int clip_and_draw_aaline(SDL_Surface* surf, SDL_Rect* rect, Uint32 color, float* pts, int blend)
# {
# 	if(!clipaaline(pts, rect->x+1, rect->y+1, rect->x+rect->w-2, rect->y+rect->h-2))
# 		return 0;
# 	drawaaline(surf, color, pts[0], pts[1], pts[2], pts[3], blend);
# 	return 1;
# }


def clip_and_draw_line(surface, clip_rect, color, pts):
    """
    note: clip_rect is sdl_surface.clip_rect, which is a SDL_Rect *
    """
    if debug:
        print('gsdl2.draw.clip_and_draw_line')
    # print('surface={} clip_rect={} color={} pts={}'.format(surface, clip_rect, color, pts))
# 	if(!clipline(pts, rect->x, rect->y, rect->x+rect->w-1, rect->y+rect->h-1))
# 		return 0;
    if not clipline(pts, clip_rect.x, clip_rect.y, clip_rect.x + clip_rect.w - 1, clip_rect.y + clip_rect.h - 1):
        return 0

# 	if(pts[1] == pts[3])
# 		drawhorzline(surf, color, pts[0], pts[1], pts[2]);
# 	else if(pts[0] == pts[2])
# 		drawvertline(surf, color, pts[0], pts[1], pts[3]);
# 	else
# 		drawline(surf, color, pts[0], pts[1], pts[2], pts[3]);
    if pts[1] == pts[3]:
        drawhorzline(surface, color, pts[0], pts[1], pts[2])
    elif pts[0] == pts[2]:
        drawvertline(surface, color, pts[0], pts[1], pts[3])
    else:
        drawline(surface, color, pts[0], pts[1], pts[2], pts[3])

# 	return 1;
    return 1


# static int clip_and_draw_line(SDL_Surface* surf, SDL_Rect* rect, Uint32 color, int* pts)
# {
# 	if(!clipline(pts, rect->x, rect->y, rect->x+rect->w-1, rect->y+rect->h-1))
# 		return 0;
# 	if(pts[1] == pts[3])
# 		drawhorzline(surf, color, pts[0], pts[1], pts[2]);
# 	else if(pts[0] == pts[2])
# 		drawvertline(surf, color, pts[0], pts[1], pts[3]);
# 	else
# 		drawline(surf, color, pts[0], pts[1], pts[2], pts[3]);
# 	return 1;
# }


def clip_and_draw_line_width(surface, clip_rect, color, width, pts):
    """
    note: clip_rect is sdl_surface.clip_rect, which is a SDL_Rect *
    """
    if debug:
        print('gsdl2.draw.clip_and_draw_line_width')
# 	int loop;
# 	int xinc=0, yinc=0;
# 	int newpts[4];
# 	int range[4];
    rng = [0] * 4
# 	int anydrawn = 0;
    anydrawn = 0
#
# 	if(abs(pts[0]-pts[2]) > abs(pts[1]-pts[3]))
# 		yinc = 1;
# 	else
# 		xinc = 1;
    if abs(pts[0] - pts[2]) > abs(pts[1] - pts[3]):
        yinc = 1
    else:
        xinc = 1

# 	memcpy(newpts, pts, sizeof(int)*4);
    newpts = list(pts)

# 	if(clip_and_draw_line(surf, rect, color, newpts))
# 	{
# 		anydrawn = 1;
# 		memcpy(range, newpts, sizeof(int)*4);
# 	}
# 	else
# 	{
# 		range[0] = range[1] = 10000;
# 		range[2] = range[3] = -10000;
# 	}
    if clip_and_draw_line(surface, clip_rect, color, newpts):
        anydrawn = 1
        rng = list(newpts)
    else:
        rng[0] = rng[1] = 10000
        rng[2] = rng[3] = -10000

# 	for(loop = 1; loop < width; loop += 2)
# 	{
    for loop in range(1, width, 2):
# 		newpts[0] = pts[0] + xinc*(loop/2+1);
# 		newpts[1] = pts[1] + yinc*(loop/2+1);
# 		newpts[2] = pts[2] + xinc*(loop/2+1);
# 		newpts[3] = pts[3] + yinc*(loop/2+1);
        newpts[0] = pts[0] + xinc * (loop // 2 + 1)
        newpts[1] = pts[1] + yinc * (loop // 2 + 1)
        newpts[2] = pts[2] + xinc * (loop // 2 + 1)
        newpts[3] = pts[3] + yinc * (loop // 2 + 1)

# 		if(clip_and_draw_line(surf, rect, color, newpts))
# 		{
# 			anydrawn = 1;
# 			range[0] = MIN(newpts[0], range[0]);
# 			range[1] = MIN(newpts[1], range[1]);
# 			range[2] = MAX(newpts[2], range[2]);
# 			range[3] = MAX(newpts[3], range[3]);
# 		}
        if clip_and_draw_line(surface, clip_rect, color, newpts):
            anydrawn = 1
            rng[0] = min(newpts[0], rng[0])
            rng[1] = min(newpts[1], rng[1])
            rng[2] = max(newpts[2], rng[2])
            rng[3] = max(newpts[3], rng[3])

# 		if(loop+1<width)
# 		{
# 			newpts[0] = pts[0] - xinc*(loop/2+1);
# 			newpts[1] = pts[1] - yinc*(loop/2+1);
# 			newpts[2] = pts[2] - xinc*(loop/2+1);
# 			newpts[3] = pts[3] - yinc*(loop/2+1);
        if loop + 1 < width:
            newpts[0] = pts[0] - xinc * (loop // 2 + 1)
            newpts[1] = pts[1] - yinc * (loop // 2 + 1)
            newpts[2] = pts[2] - xinc * (loop // 2 + 1)
            newpts[3] = pts[3] - yinc * (loop // 2 + 1)

# 			if(clip_and_draw_line(surf, rect, color, newpts))
# 			{
# 				anydrawn = 1;
# 				range[0] = MIN(newpts[0], range[0]);
# 				range[1] = MIN(newpts[1], range[1]);
# 				range[2] = MAX(newpts[2], range[2]);
# 				range[3] = MAX(newpts[3], range[3]);
            if clip_and_draw_line(surface, clip_rect, color, newpts):
                anydrawn = 1
                rng[0] = min(newpts[0], rng[0])
                rng[1] = min(newpts[1], rng[1])
                rng[2] = max(newpts[2], rng[2])
                rng[3] = max(newpts[3], rng[3])

# 	if(anydrawn)
# 		memcpy(pts, range, sizeof(int)*4);
    if anydrawn:
        for i, v in enumerate(rng):
            pts[i] = v

# 	return anydrawn;
    return anydrawn


# static int clip_and_draw_line_width(SDL_Surface* surf, SDL_Rect* rect, Uint32 color, int width, int* pts)
# {
# 	int loop;
# 	int xinc=0, yinc=0;
# 	int newpts[4];
# 	int range[4];
# 	int anydrawn = 0;
#
# 	if(abs(pts[0]-pts[2]) > abs(pts[1]-pts[3]))
# 		yinc = 1;
# 	else
# 		xinc = 1;
#
# 	memcpy(newpts, pts, sizeof(int)*4);
# 	if(clip_and_draw_line(surf, rect, color, newpts))
# 	{
# 		anydrawn = 1;
# 		memcpy(range, newpts, sizeof(int)*4);
# 	}
# 	else
# 	{
# 		range[0] = range[1] = 10000;
# 		range[2] = range[3] = -10000;
# 	}
#
# 	for(loop = 1; loop < width; loop += 2)
# 	{
# 		newpts[0] = pts[0] + xinc*(loop/2+1);
# 		newpts[1] = pts[1] + yinc*(loop/2+1);
# 		newpts[2] = pts[2] + xinc*(loop/2+1);
# 		newpts[3] = pts[3] + yinc*(loop/2+1);
# 		if(clip_and_draw_line(surf, rect, color, newpts))
# 		{
# 			anydrawn = 1;
# 			range[0] = MIN(newpts[0], range[0]);
# 			range[1] = MIN(newpts[1], range[1]);
# 			range[2] = MAX(newpts[2], range[2]);
# 			range[3] = MAX(newpts[3], range[3]);
# 		}
# 		if(loop+1<width)
# 		{
# 			newpts[0] = pts[0] - xinc*(loop/2+1);
# 			newpts[1] = pts[1] - yinc*(loop/2+1);
# 			newpts[2] = pts[2] - xinc*(loop/2+1);
# 			newpts[3] = pts[3] - yinc*(loop/2+1);
# 			if(clip_and_draw_line(surf, rect, color, newpts))
# 			{
# 				anydrawn = 1;
# 				range[0] = MIN(newpts[0], range[0]);
# 				range[1] = MIN(newpts[1], range[1]);
# 				range[2] = MAX(newpts[2], range[2]);
# 				range[3] = MAX(newpts[3], range[3]);
# 			}
# 		}
# 	}
# 	if(anydrawn)
# 		memcpy(pts, range, sizeof(int)*4);
# 	return anydrawn;
# }


# this line clipping based heavily off of code from
# http://www.ncsa.uiuc.edu/Vis/Graphics/src/clipCohSuth.c
LEFT_EDGE = 0x1
RIGHT_EDGE = 0x2
BOTTOM_EDGE = 0x4
TOP_EDGE = 0x8

def INSIDE(a):
    return not a


def REJECT(a, b):
    return a & b


def ACCEPT(a, b):
    return not a | b


def encode(x, y, left, top, right, bottom):
    code = 0
    if x < left:
        code |= LEFT_EDGE
    if x > right:
        code |= RIGHT_EDGE
    if y < top:
        code |= TOP_EDGE
    if y > bottom:
        code |= BOTTOM_EDGE

    return code


# static int encode(int x, int y, int left, int top, int right, int bottom)
# {
# 	int code = 0;
# 	if(x < left)  code |= LEFT_EDGE;
# 	if(x > right) code |= RIGHT_EDGE;
# 	if(y < top)   code |= TOP_EDGE;
# 	if(y > bottom)code |= BOTTOM_EDGE;
# 	return code;
# }


def encodeFloat():
    # TODO
    pass


# static int encodeFloat(float x, float y, int left, int top, int right, int bottom)
# {
# 	int code = 0;
# 	if(x < left)  code |= LEFT_EDGE;
# 	if(x > right) code |= RIGHT_EDGE;
# 	if(y < top)   code |= TOP_EDGE;
# 	if(y > bottom)code |= BOTTOM_EDGE;
# 	return code;
# }


def clipaaline():
    # TODO
    if debug:
        print('gsdl.draw.clipaaline')


# static int clipaaline(float* pts, int left, int top, int right, int bottom)
# {
# 	float x1 = pts[0];
# 	float y1 = pts[1];
# 	float x2 = pts[2];
# 	float y2 = pts[3];
# 	int code1, code2;
# 	int draw = 0;
# 	float swaptmp;
# 	int intswaptmp;
# 	float m; /*slope*/
#
# 	while(1) {
# 		code1 = encodeFloat(x1, y1, left, top, right, bottom);
# 		code2 = encodeFloat(x2, y2, left, top, right, bottom);
# 		if(ACCEPT(code1, code2)) {
# 			draw = 1;
# 			break;
# 		}
# 		else if(REJECT(code1, code2)) {
# 			break;
# 		}
# 		else {
# 			if(INSIDE(code1)) {
# 				swaptmp = x2; x2 = x1; x1 = swaptmp;
# 				swaptmp = y2; y2 = y1; y1 = swaptmp;
# 				intswaptmp = code2; code2 = code1; code1 = intswaptmp;
# 			}
# 			if(x2 != x1)
# 				m = (y2 - y1) / (x2 - x1);
# 			else
# 				m = 1.0f;
# 			if(code1 & LEFT_EDGE) {
# 				y1 += ((float)left - x1) * m;
# 				x1 = (float)left;
# 			}
# 			else if(code1 & RIGHT_EDGE) {
# 				y1 += ((float)right - x1) * m;
# 				x1 = (float)right;
# 			}
# 			else if(code1 & BOTTOM_EDGE) {
# 				if(x2 != x1)
# 					x1 += ((float)bottom - y1) / m;
# 				y1 = (float)bottom;
# 			}
# 			else if(code1 & TOP_EDGE) {
# 				if(x2 != x1)
# 					x1 += ((float)top - y1) / m;
# 				y1 = (float)top;
# 			}
# 		}
# 	}
# 	if(draw) {
# 		pts[0] = x1; pts[1] = y1;
# 		pts[2] = x2; pts[3] = y2;
# 	}
# 	return draw;
# }


def clipline(pts, left, top, right, bottom):
    if debug:
        print('sdl2.draw.clipline')
    # print('pts={} l,t,r,b={}'.format(pts, (left, top, right, bottom)))
# 	int x1 = pts[0];
# 	int y1 = pts[1];
# 	int x2 = pts[2];
# 	int y2 = pts[3];
    x1 = pts[0]
    y1 = pts[1]
    x2 = pts[2]
    y2 = pts[3]

# 	int code1, code2;
# 	int draw = 0;
    draw = 0
# 	int swaptmp;
# 	float m; /*slope*/
#
# 	while(1)
# 	{
# 		code1 = encode(x1, y1, left, top, right, bottom);
# 		code2 = encode(x2, y2, left, top, right, bottom);
    while 1:
        code1 = encode(x1, y1, left, top, right, bottom)
        code2 = encode(x2, y2, left, top, right, bottom)

# 		if(ACCEPT(code1, code2)) {
# 			draw = 1;
# 			break;
# 		}
        if ACCEPT(code1, code2):
            draw = 1
            break

# 		else if(REJECT(code1, code2))
# 			break;
        elif REJECT(code1, code2):
            break

# 		else {
# 			if(INSIDE(code1)) {
# 				swaptmp = x2; x2 = x1; x1 = swaptmp;
# 				swaptmp = y2; y2 = y1; y1 = swaptmp;
# 				swaptmp = code2; code2 = code1; code1 = swaptmp;
# 			}
        else:
            if INSIDE(code1):
                swaptmp = x2
                x2 = x1
                x1 = swaptmp

                swaptmp = y2
                y2 = y1
                y1 = swaptmp

                swaptmp = code2
                code2 = code1
                code1 = swaptmp

# 			if(x2 != x1)
# 				m = (y2 - y1) / (float)(x2 - x1);
# 			else
# 				m = 1.0f;
            if x2 != x1:
                m = (y2 - y1) / float(x2 - x1)
            else:
                m = 1.0

# 			if(code1 & LEFT_EDGE) {
# 				y1 += (int)((left - x1) * m);
# 				x1 = left;
# 			}
            if code1 & LEFT_EDGE:
                y1 += int((left - x1) * m)
                x1 = left

# 			else if(code1 & RIGHT_EDGE) {
# 				y1 += (int)((right - x1) * m);
# 				x1 = right;
# 			}
            elif code1 & RIGHT_EDGE:
                y1 += int((right - x1) * m)
                x1 = right

# 			else if(code1 & BOTTOM_EDGE) {
# 				if(x2 != x1)
# 					x1 += (int)((bottom - y1) / m);
# 				y1 = bottom;
# 			}
            elif code1 & BOTTOM_EDGE:
                if x2 != x1:
                    x1 += int((bottom - y1) / m)
                y1 = bottom

# 			else if(code1 & TOP_EDGE) {
# 				if(x2 != x1)
# 					x1 += (int)((top - y1) / m);
# 				y1 = top;
            elif code1 & TOP_EDGE:
                if x2 != x1:
                    x1 += int((top - y1) / m)
                y1 = top

# 	if(draw) {
# 		pts[0] = x1; pts[1] = y1;
# 		pts[2] = x2; pts[3] = y2;
# 	}
    if draw:
        pts[0] = x1
        pts[1] = y1
        pts[2] = x2
        pts[3] = y2

# 	return draw;
    return draw


# static int clipline(int* pts, int left, int top, int right, int bottom)
# {
# 	int x1 = pts[0];
# 	int y1 = pts[1];
# 	int x2 = pts[2];
# 	int y2 = pts[3];
# 	int code1, code2;
# 	int draw = 0;
# 	int swaptmp;
# 	float m; /*slope*/
#
# 	while(1)
# 	{
# 		code1 = encode(x1, y1, left, top, right, bottom);
# 		code2 = encode(x2, y2, left, top, right, bottom);
# 		if(ACCEPT(code1, code2)) {
# 			draw = 1;
# 			break;
# 		}
# 		else if(REJECT(code1, code2))
# 			break;
# 		else {
# 			if(INSIDE(code1)) {
# 				swaptmp = x2; x2 = x1; x1 = swaptmp;
# 				swaptmp = y2; y2 = y1; y1 = swaptmp;
# 				swaptmp = code2; code2 = code1; code1 = swaptmp;
# 			}
# 			if(x2 != x1)
# 				m = (y2 - y1) / (float)(x2 - x1);
# 			else
# 				m = 1.0f;
# 			if(code1 & LEFT_EDGE) {
# 				y1 += (int)((left - x1) * m);
# 				x1 = left;
# 			}
# 			else if(code1 & RIGHT_EDGE) {
# 				y1 += (int)((right - x1) * m);
# 				x1 = right;
# 			}
# 			else if(code1 & BOTTOM_EDGE) {
# 				if(x2 != x1)
# 					x1 += (int)((bottom - y1) / m);
# 				y1 = bottom;
# 			}
# 			else if(code1 & TOP_EDGE) {
# 				if(x2 != x1)
# 					x1 += (int)((top - y1) / m);
# 				y1 = top;
# 			}
# 		}
# 	}
# 	if(draw) {
# 		pts[0] = x1; pts[1] = y1;
# 		pts[2] = x2; pts[3] = y2;
# 	}
# 	return draw;
# }


def set_at(surf, x, y, color):
    # TODO: untested, currently unused
    """note: surf is SDL_Surface *, color is SDL_Color *"""
# 	SDL_PixelFormat* format = surf->format;
# 	Uint8* pixels = (Uint8*)surf->pixels;
# 	Uint8* byte_buf, rgb[4];

    clip_rect = surf.clip_rect
    if x < clip_rect.x or x >= clip_rect.x + clip_rect.w or y < clip_rect.y or y >= clip_rect.y + clip_rect.h:
        return 0

    bpp = surf.format.BytesPerPixel
    if bpp == 1:
        pixels = sdl_ffi.cast('Uint8 *', surf.pixels)
        pixels += y * surf.pitch + x
        pixels[0] = color
    elif bpp == 2:
        pixels = sdl_ffi.cast('Uint16 *', surf.pixels)
        pixels += y * surf.pitch + x
        pixels[0] = color
    elif bpp == 4:
        pixels = sdl_ffi.cast('Uint32 *', surf.pixels)
        pixels += y * surf.pitch + x
        pixels[0] = color
    else:
        pixels = sdl_ffi.cast('Uint8 *', surf.pixels)
        rgb = sdl_ffi.new('Uint8 [4]')
        c = sdl_ffi.cast('Uint32 *', color)
        sdl_lib.SDL_GetRGB(c[0], surf.format, rgb, rgb + 1, rgb + 2)
        byte_buf = (pixels + y * surf.pitch) + x * 3
        if SDL_BYTEORDER == SDL_BIG_ENDIAN:
            byte_buf[0] = rgb[0]
            byte_buf[1] = rgb[1]
            byte_buf[2] = rgb[2]
        else:
            byte_buf[2] = rgb[0]
            byte_buf[1] = rgb[1]
            byte_buf[0] = rgb[2]

    return 1


# static int set_at(SDL_Surface* surf, int x, int y, Uint32 color)
# {
# 	SDL_PixelFormat* format = surf->format;
# 	Uint8* pixels = (Uint8*)surf->pixels;
# 	Uint8* byte_buf, rgb[4];
#
# 	if(x < surf->clip_rect.x || x >= surf->clip_rect.x + surf->clip_rect.w ||
# 				y < surf->clip_rect.y || y >= surf->clip_rect.y + surf->clip_rect.h)
# 	return 0;
#
# 	switch(format->BytesPerPixel)
# 	{
# 		case 1:
# 			*((Uint8*)pixels + y * surf->pitch + x) = (Uint8)color;
# 			break;
# 		case 2:
# 			*((Uint16*)(pixels + y * surf->pitch) + x) = (Uint16)color;
# 			break;
# 		case 4:
# 			*((Uint32*)(pixels + y * surf->pitch) + x) = color;
# /*			  *((Uint32*)(pixels + y * surf->pitch) + x) =
# 				 ~(*((Uint32*)(pixels + y * surf->pitch) + x)) * 31;
# */			  break;
# 		default:/*case 3:*/
# 			SDL_GetRGB(color, format, rgb, rgb+1, rgb+2);
# 			byte_buf = (Uint8*)(pixels + y * surf->pitch) + x * 3;
# #if (SDL_BYTEORDER == SDL_LIL_ENDIAN)
#                         *(byte_buf + (format->Rshift >> 3)) = rgb[0];
#                         *(byte_buf + (format->Gshift >> 3)) = rgb[1];
#                         *(byte_buf + (format->Bshift >> 3)) = rgb[2];
# #else
#                         *(byte_buf + 2 - (format->Rshift >> 3)) = rgb[0];
#                         *(byte_buf + 2 - (format->Gshift >> 3)) = rgb[1];
#                         *(byte_buf + 2 - (format->Bshift >> 3)) = rgb[2];
# #endif
# 			break;
# 	}
# 	return 1;
# }


def DRAWPIX32():
    # TODO
    pass


# #define DRAWPIX32(pixel,colorptr,br,blend) \
# 	if(SDL_BYTEORDER == SDL_BIG_ENDIAN) color <<= 8; \
#         if(blend) { \
#                 int x; \
#                 float nbr = 1.0-br; \
#                 x = colorptr[0]*br+pixel[0]*nbr; \
#                 pixel[0]= (x>254) ? 255: x; \
#                 x = colorptr[1]*br+pixel[1]*nbr; \
#                 pixel[1]= (x>254) ? 255: x; \
#                 x = colorptr[2]*br+pixel[2]*nbr; \
#                 pixel[2]= (x>254) ? 255: x; \
#                 if(hasalpha) pixel[3] = pixel[0]+(br*255) - (pixel[3]*br); \
#         } else { \
#                 pixel[0]=(Uint8)(colorptr[0]*br); \
#                 pixel[1]=(Uint8)(colorptr[1]*br); \
#                 pixel[2]=(Uint8)(colorptr[2]*br); \
#                 if(hasalpha) pixel[3] = br*255; \
# 	}


def drawaaline():
    # TODO
    if debug:
        print('gsdl.draw.draw_aaline')


# /* Adapted from http://freespace.virgin.net/hugo.elias/graphics/x_wuline.htm */
# static void drawaaline(SDL_Surface* surf, Uint32 color, float x1, float y1, float x2, float y2, int blend) {
# 	float grad, xd, yd;
#    	float xgap, ygap, xend, yend, xf, yf;
# 	float brightness1, brightness2;
# 	float swaptmp;
# 	int x, y, ix1, ix2, iy1, iy2;
# 	int pixx, pixy;
# 	Uint8* pixel;
# 	Uint8* pm = (Uint8*)surf->pixels;
# 	Uint8* colorptr = (Uint8*)&color;
#         const int hasalpha = surf->format->Amask;
#
#         pixx = surf->format->BytesPerPixel;
# 	pixy = surf->pitch;
#
# 	xd = x2-x1;
# 	yd = y2-y1;
#
#         if (xd == 0 && yd == 0)
#         {
#             /* Single point. Due to the nature of the aaline clipping, this
#              * is less exact than the normal line. */
#             set_at (surf, x1, y1, color);
#             return;
#         }
#
# 	if(fabs(xd)>fabs(yd)) {
# 		if(x1>x2) {
# 			swaptmp=x1; x1=x2; x2=swaptmp;
# 			swaptmp=y1; y1=y2; y2=swaptmp;
# 			xd = (x2-x1);
# 			yd = (y2-y1);
# 		}
# 		grad = yd/xd;
# 		xend = trunc(x1)+0.5; /* This makes more sense than trunc(x1+0.5) */
# 		yend = y1+grad*(xend-x1);
# 		xgap = INVFRAC(x1);
# 		ix1 = (int)xend;
# 		iy1 = (int)yend;
# 		yf = yend+grad;
# 		brightness1 = INVFRAC(yend) * xgap;
# 		brightness2 =    FRAC(yend) * xgap;
# 		pixel = pm + pixx * ix1 + pixy * iy1;
# 		DRAWPIX32(pixel, colorptr, brightness1, blend)
# 		pixel += pixy;
# 		DRAWPIX32(pixel, colorptr, brightness2, blend)
# 		xend = trunc(x2)+0.5;
# 		yend = y2+grad*(xend-x2);
# 		xgap =    FRAC(x2); /* this also differs from Hugo's description. */
# 		ix2 = (int)xend;
# 		iy2 = (int)yend;
# 		brightness1 = INVFRAC(yend) * xgap;
# 		brightness2 =    FRAC(yend) * xgap;
# 		pixel = pm + pixx * ix2 + pixy * iy2;
# 		DRAWPIX32(pixel, colorptr, brightness1, blend)
# 		pixel += pixy;
# 		DRAWPIX32(pixel, colorptr, brightness2, blend)
# 		for(x=ix1+1; x<ix2; ++x) {
# 			brightness1=INVFRAC(yf);
# 			brightness2=   FRAC(yf);
# 			pixel = pm + pixx * x + pixy * (int)yf;
# 			DRAWPIX32(pixel, colorptr, brightness1, blend)
# 			pixel += pixy;
# 			DRAWPIX32(pixel, colorptr, brightness2, blend)
# 			yf += grad;
# 		}
# 	}
# 	else {
# 		if(y1>y2) {
# 			swaptmp=y1; y1=y2; y2=swaptmp;
# 			swaptmp=x1; x1=x2; x2=swaptmp;
# 			yd = (y2-y1);
# 			xd = (x2-x1);
# 		}
# 		grad = xd/yd;
# 		yend = trunc(y1)+0.5;  /* This makes more sense than trunc(x1+0.5) */
# 		xend = x1+grad*(yend-y1);
# 		ygap = INVFRAC(y1);
# 		iy1 = (int)yend;
# 		ix1 = (int)xend;
# 		xf = xend+grad;
# 		brightness1 = INVFRAC(xend) * ygap;
# 		brightness2 =    FRAC(xend) * ygap;
# 		pixel = pm + pixx * ix1 + pixy * iy1;
# 		DRAWPIX32(pixel, colorptr, brightness1, blend)
# 		pixel += pixx;
# 		DRAWPIX32(pixel, colorptr, brightness2, blend)
# 		yend = trunc(y2)+0.5;
# 		xend = x2+grad*(yend-y2);
# 		ygap = FRAC(y2);
# 		iy2 = (int)yend;
# 		ix2 = (int)xend;
# 		brightness1 = INVFRAC(xend) * ygap;
# 		brightness2 =    FRAC(xend) * ygap;
# 		pixel = pm + pixx * ix2 + pixy * iy2;
# 		DRAWPIX32(pixel, colorptr, brightness1, blend)
# 		pixel += pixx;
# 		DRAWPIX32(pixel, colorptr, brightness2, blend)
# 		for(y=iy1+1; y<iy2; ++y) {
# 			brightness1=INVFRAC(xf);
# 			brightness2=   FRAC(xf);
# 			pixel = pm + pixx * (int)xf + pixy * y;
# 			DRAWPIX32(pixel, colorptr, brightness1, blend)
# 			pixel += pixx;
# 			DRAWPIX32(pixel, colorptr, brightness2, blend)
# 			xf += grad;
# 		}
# 	}
# }


def drawline(surface, color, x1, y1, x2, y2):
    if debug:
        print('gsdl2.draw.drawline')
    # print('surface={} color={} points={}'.format(surface, color, (x1, y1, x2, y2)))
# 	int deltax, deltay, signx, signy;
# 	int pixx, pixy;
# 	int x = 0, y = 0;
    y = 0
# 	int swaptmp;
# 	Uint8 *pixel;
# 	Uint8 *colorptr;
    colorptr = color.sdl_color
#
# 	deltax = x2 - x1;
# 	deltay = y2 - y1;
# 	signx = (deltax < 0) ? -1 : 1;
# 	signy = (deltay < 0) ? -1 : 1;
# 	deltax = signx * deltax + 1;
# 	deltay = signy * deltay + 1;
    deltax = x2 - x1
    deltay = y2 - y1
    signx = -1 if deltax < 0 else 1
    signy = -1 if deltay < 0 else 1
    deltax = signx * deltax + 1
    deltay = signy * deltay + 1

    surf = surface.sdl_surface

# 	pixx = surf->format->BytesPerPixel;
# 	pixy = surf->pitch;
# 	pixel = ((Uint8*)surf->pixels) + pixx * x1 + pixy * y1;
    pixx = surf.format.BytesPerPixel
    pixy = surf.pitch
    pixel = surf.pixels + pixx * x1 + pixy * y1

# 	pixx *= signx;
# 	pixy *= signy;
# 	if(deltax < deltay) /*swap axis if rise > run*/
# 	{
# 		swaptmp = deltax; deltax = deltay; deltay = swaptmp;
# 		swaptmp = pixx; pixx = pixy; pixy = swaptmp;
# 	}
    pixx *= signx
    pixy *= signy
    if deltax < deltay:  # swap axis if rise > run
        swaptmp = deltax
        deltax = deltay
        deltay = swaptmp

        swaptmp = pixx
        pixx = pixy
        pixy = swaptmp

# 	switch(surf->format->BytesPerPixel)
# 	{
# 	case 1:
# 		for(; x < deltax; x++, pixel += pixx) {
# 			*pixel = (Uint8)color;
# 			y += deltay; if(y >= deltax) {y -= deltax; pixel += pixy;}
# 		}break;
    if surf.format.BytesPerPixel == 1:
        pixel8 = sdl_ffi.cast('Uint8 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        cp = sdl_ffi.new('Uint8 []', [int(c)])
        for x in range(deltax):
            pixel8[0] = cp[0]
            y += deltay
            if y >= deltax:
                y -= deltax
                pixel8 += pixy
            pixel8 += pixx

# 	case 2:
# 		for(; x < deltax; x++, pixel += pixx) {
# 			*(Uint16*)pixel = (Uint16)color;
# 			y += deltay; if(y >= deltax) {y -= deltax; pixel += pixy;}
# 		}break;
    elif surf.format.BytesPerPixel == 2:
        pixel16 = sdl_ffi.cast('Uint16 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        cp = sdl_ffi.new('Uint16 []', [int(c)])
        for x in range(deltax):
            pixel16[0] = cp[0]
            y += deltay
            if y >= deltax:
                y -= deltax
                pixel16 += pixy // 2
            pixel16 += pixx // 2

# 	case 3:
# 		if(SDL_BYTEORDER == SDL_BIG_ENDIAN) color <<= 8;
# 		colorptr = (Uint8*)&color;
# 		for(; x < deltax; x++, pixel += pixx) {
# 			pixel[0] = colorptr[0];
# 			pixel[1] = colorptr[1];
# 			pixel[2] = colorptr[2];
# 			y += deltay; if(y >= deltax) {y -= deltax; pixel += pixy;}
# 		}break;
    elif surf.format.BytesPerPixel == 3:
        pixel8 = sdl_ffi.cast('Uint8 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        # TODO: test me
        if SDL_BYTEORDER == SDL_BIG_ENDIAN:
            c <<= 8
        cp = sdl_ffi.new('Uint32 []', [int(c)])
        rgba = sdl_ffi.cast('Uint8 *', cp)
        for x in range(deltax):
            pixel8[0] = rgba[0]
            pixel8[1] = rgba[1]
            pixel8[2] = rgba[2]
            y += deltay
            if y >= deltax:
                y -= deltax
                pixel8 += pixy
            pixel8 += pixx

# 	default: /*case 4*/
# 		for(; x < deltax; x++, pixel += pixx) {
# 	        *(Uint32*)pixel = (Uint32)color;
# 			y += deltay; if(y >= deltax) {y -= deltax; pixel += pixy;}
    else:  # case 4
        pixel32 = sdl_ffi.cast('Uint32 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        cp = sdl_ffi.new('Uint32 []', [int(c)])
        for x in range(deltax):
            pixel32[0] = cp[0]
            y += deltay
            if y >= deltax:
                y -= deltax
                pixel32 += pixy // 4
            pixel32 += pixx // 4


# /*here's my sdl'ized version of bresenham*/
# static void drawline(SDL_Surface* surf, Uint32 color, int x1, int y1, int x2, int y2)
# {
# 	int deltax, deltay, signx, signy;
# 	int pixx, pixy;
# 	int x = 0, y = 0;
# 	int swaptmp;
# 	Uint8 *pixel;
# 	Uint8 *colorptr;
#
# 	deltax = x2 - x1;
# 	deltay = y2 - y1;
# 	signx = (deltax < 0) ? -1 : 1;
# 	signy = (deltay < 0) ? -1 : 1;
# 	deltax = signx * deltax + 1;
# 	deltay = signy * deltay + 1;
#
# 	pixx = surf->format->BytesPerPixel;
# 	pixy = surf->pitch;
# 	pixel = ((Uint8*)surf->pixels) + pixx * x1 + pixy * y1;
#
# 	pixx *= signx;
# 	pixy *= signy;
# 	if(deltax < deltay) /*swap axis if rise > run*/
# 	{
# 		swaptmp = deltax; deltax = deltay; deltay = swaptmp;
# 		swaptmp = pixx; pixx = pixy; pixy = swaptmp;
# 	}
#
# 	switch(surf->format->BytesPerPixel)
# 	{
# 	case 1:
# 		for(; x < deltax; x++, pixel += pixx) {
# 			*pixel = (Uint8)color;
# 			y += deltay; if(y >= deltax) {y -= deltax; pixel += pixy;}
# 		}break;
# 	case 2:
# 		for(; x < deltax; x++, pixel += pixx) {
# 			*(Uint16*)pixel = (Uint16)color;
# 			y += deltay; if(y >= deltax) {y -= deltax; pixel += pixy;}
# 		}break;
# 	case 3:
# 		if(SDL_BYTEORDER == SDL_BIG_ENDIAN) color <<= 8;
# 		colorptr = (Uint8*)&color;
# 		for(; x < deltax; x++, pixel += pixx) {
# 			pixel[0] = colorptr[0];
# 			pixel[1] = colorptr[1];
# 			pixel[2] = colorptr[2];
# 			y += deltay; if(y >= deltax) {y -= deltax; pixel += pixy;}
# 		}break;
# 	default: /*case 4*/
# 		for(; x < deltax; x++, pixel += pixx) {
# 	        *(Uint32*)pixel = (Uint32)color;
# 			y += deltay; if(y >= deltax) {y -= deltax; pixel += pixy;}
# 		}break;
# 	}
# }


def drawhorzline(surface, color, x1, y1, x2):
    if debug:
        print('gsdl.draw.drawhorzline')
    colorptr = color.sdl_color

    set_at = surface.set_at
    surf = surface.sdl_surface

    if x1 == x2:
        set_at((x1, y1), color)
        return

    pixel = sdl_ffi.cast('Uint8 *', surf.pixels) + surf.pitch * y1
    if x1 < x2:
        end = pixel + x2 * surf.format.BytesPerPixel
        pixel += x1 * surf.format.BytesPerPixel
    else:
        end = pixel + x1 * surf.format.BytesPerPixel
        pixel += x2 * surf.format.BytesPerPixel

    if surf.format.BytesPerPixel == 1:
        pixel8 = sdl_ffi.cast('Uint8 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        cp = sdl_ffi.new('Uint8 []', [int(c)])
        # for(; pixel <= end; ++pixel) {
        while pixel8 <= end:
            pixel8[0] = cp[0]
            # TODO: ++pixel is bug in the original code?
            pixel8 += 1
    elif surf.format.BytesPerPixel == 2:
        pixel16 = sdl_ffi.cast('Uint16 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        cp = sdl_ffi.new('Uint16 []', [int(c)])
        # for(; pixel <= end; pixel+=2) {
        while pixel16 <= end:
            pixel16[0] = cp[0]
            pixel16 += 1
    elif surf.format.BytesPerPixel == 3:
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        # TODO: test me
        if SDL_BYTEORDER == SDL_BIG_ENDIAN:
            c <<= 8
        cp = sdl_ffi.new('Uint32 []', [int(c)])
        rgba = sdl_ffi.cast('Uint8 *', cp)
        # for(; pixel <= end; pixel+=3) {
        while pixel <= end:
            pixel[0] = rgba[0]
            pixel[1] = rgba[1]
            pixel[2] = rgba[2]
            pixel += 3
    else:  # case 4
        pixel32 = sdl_ffi.cast('Uint32 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        cp = sdl_ffi.new('Uint32 []', [int(c)])
        # for(; pixel <= end; pixel+=4) {
        while pixel32 <= end:
            pixel32[0] = cp[0]
            pixel32 += 1


def drawhorzlineclip(surface, color, x1, y1, x2):
    if debug:
        print('gsdl.draw.drawhorzlineclip')
    surf = surface.sdl_surface
    set_at = surface.set_at

    if y1 < surf.clip_rect.y or y1 >= surf.clip_rect.y + surf.clip_rect.h:
        return

    if x2 < x1:
        temp = x1
        x1 = x2
        x2 = temp

    x1 = max(x1, surf.clip_rect.x)
    x2 = min(x2, surf.clip_rect.x + surf.clip_rect.w - 1)

    if x2 < surf.clip_rect.x or x1 >= surf.clip_rect.x + surf.clip_rect.w:
        return

    if x1 == x2:
        set_at((x1, y1), color)
    else:
        drawhorzline(surface, color, x1, y1, x2)


def drawvertline(surface, color, x1, y1, y2):
    if debug:
        print('gsdl.draw.drawvertline')
    pixel = end = 0
    colorptr = color.sdl_color
    surf = surface.sdl_surface
    pitch = surf.pitch

    set_at = surface.set_at

    if y1 == y2:
        set_at(surf, x1, y1, color)
        return

    pixel = surf.pixels + x1 * surf.format.BytesPerPixel
    if y1 < y2:
        end = pixel + surf.pitch * y2
        pixel += surf.pitch * y1
    else:
        end = pixel + surf.pitch * y1
        pixel += surf.pitch * y2

    if surf.format.BytesPerPixel == 1:
        pixel8 = sdl_ffi.cast('Uint8 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        cp = sdl_ffi.new('Uint8 []', [int(c)])
        while pixel8 <= end:
            pixel8[0] = cp[0]
            pixel8 += pitch
    elif surf.format.BytesPerPixel == 2:
        pixel16 = sdl_ffi.cast('Uint16 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        cp = sdl_ffi.new('Uint16 []', [int(c)])
        while pixel16 <= end:
            pixel16[0] = cp[0]
            pixel16 += pitch // 2
    elif surf.format.BytesPerPixel == 3:
        pixel8 = sdl_ffi.cast('Uint8 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        # TODO: test me
        if SDL_BYTEORDER == SDL_BIG_ENDIAN:
            c <<= 8
        cp = sdl_ffi.new('Uint32 []', [int(c)])
        rgba = sdl_ffi.cast('Uint8 *', cp)
        while pixel8 <= end:
            pixel8[0] = rgba[0]
            pixel8[1] = rgba[1]
            pixel8[2] = rgba[2]
            pixel8 += pitch
    else:  # case 4
        pixel32 = sdl_ffi.cast('Uint32 *', pixel)
        c = sdl_lib.SDL_MapRGBA(surf.format, colorptr.r, colorptr.g, colorptr.b, colorptr.a)
        cp = sdl_ffi.new('Uint32 []', [int(c)])
        while pixel32 <= end:
            pixel32[0] = cp[0]
            pixel32 += pitch // 4


def drawvertlineclip(surface, color, x1, y1, y2):
    if debug:
        print('gsdl.draw.drawvertlineclip')
    surf = surface.sdl_surface
    set_at = surface.set_at

    if x1 < surf.clip_rect.x or x1 >= surf.clip_rect.x + surf.clip_rect.w:
        return
    if y2 < y1:
        temp = y1
        y1 = y2
        y2 = temp
    y1 = max(y1, surf.clip_rect.y)
    y2 = min(y2, surf.clip_rect.y + surf.clip_rect.h - 1)
    if y2 - y1 < 1:
        set_at(x1, y1, color)
    else:
        drawvertline(surface, color, x1, y1, y2)


def draw_arc(surface, x, y, radius1, radius2, angle_start, angle_stop, color):
    # TODO
    if debug:
        print('gsdl.draw.drawarc')

    # Angle step in rad
    if radius1 < radius2:
        if radius1 < 1.0e-4:
            a_step = 1.0
        else:
            a_step = math.asin(2.0 / radius1)
    else:
        if radius2 < 1.0e-4:
            a_step = 1.0
        else:
            a_step = math.asin(2.0 / radius2)

    if a_step < 0.05:
        a_step = 0.05

    x_last = int(x + math.cos(angle_start) * radius1)
    y_last = int(y - math.sin(angle_start) * radius2)
    # for(a=angle_start+a_step; a<=angle_stop; a+=a_step) {
    a = angle_start + a_step
    while a <= angle_stop:
        points = [0] * 4
        x_next = int(x + math.cos(a) * radius1)
        y_next = int(y - math.sin(a) * radius2)
        points[0] = x_last
        points[1] = y_last
        points[2] = x_next
        points[3] = y_next
        clip_and_draw_line(surface, surface.sdl_surface.clip_rect, color, points)
        x_last = x_next
        y_last = y_next

        a += a_step


# static void draw_arc(SDL_Surface *dst, int x, int y, int radius1, int radius2,
#                      double angle_start, double angle_stop, Uint32 color)
# {
#     double aStep;            // Angle Step (rad)
#     double a;                // Current Angle (rad)
#     int x_last, x_next, y_last, y_next;
#
#     // Angle step in rad
#     if (radius1<radius2) {
#         if (radius1<1.0e-4) {
#             aStep=1.0;
#         } else {
#             aStep=asin(2.0/radius1);
#         }
#     } else {
#         if (radius2<1.0e-4) {
#             aStep=1.0;
#         } else {
#             aStep=asin(2.0/radius2);
#         }
#     }
#
#     if(aStep<0.05) {
#         aStep = 0.05;
#     }
#
#     x_last = x+cos(angle_start)*radius1;
#     y_last = y-sin(angle_start)*radius2;
#     for(a=angle_start+aStep; a<=angle_stop; a+=aStep) {
#       int points[4];
#       x_next = x+cos(a)*radius1;
#       y_next = y-sin(a)*radius2;
#       points[0] = x_last; points[1] = y_last;
#       points[2] = x_next; points[3] = y_next;
#       clip_and_draw_line(dst, &dst->clip_rect, color, points);
#       x_last = x_next;
#       y_last = y_next;
#     }
# }


def draw_ellipse(surface, x, y, rx, ry, color):
    if debug:
        print('gsdl.draw.draw_ellipse')
    # int ix, iy;
    # int h, i, j, k;
    # int oh, oi, oj, ok;
    # int xmh, xph, ypk, ymk;
    # int xmi, xpi, ymj, ypj;
    # int xmj, xpj, ymi, ypi;
    # int xmk, xpk, ymh, yph;

    # TODO: this is slow; it converts the color to a format-pixel each call
    def set_at(x, y, c):
        surf_set_at((x, y), c)

    surf_set_at = surface.set_at

    if rx == 0 and ry == 0:  # Special case - draw a single pixel
        set_at(x, y, color)
        return

    if rx == 0:  # Special case for rx=0 - draw a vline
        drawvertlineclip(surface, color, x, y - ry, y + ry)
        return

    if ry == 0:  # Special case for ry=0 - draw a hline
        drawhorzlineclip(surface, color, x - rx, y, x + rx)
        return

    # Init vars
    oh = oi = oj = ok = 0xFFFF
    if rx > ry:
        ix = 0
        iy = rx * 64
        # do {
        h = (ix + 16) >> 6
        i = (iy + 16) >> 6
        while i > h:
            j = (h * ry) / rx
            k = (i * ry) / rx

            if ok != k and oj != k or oj != j and ok != j or k != j:
                xph = x + h - 1
                xmh = x - h
                if k > 0:
                    ypk = y + k - 1
                    ymk = y - k
                    if h > 0:
                        set_at(xmh, ypk, color)
                        set_at(xmh, ymk, color)
                    set_at(xph, ypk, color)
                    set_at(xph, ymk, color)
                ok = k
                xpi = x + i - 1
                xmi = x - i
                if j > 0:
                    ypj = y + j - 1
                    ymj = y - j
                    set_at(xmi, ypj, color)
                    set_at(xpi, ypj, color)
                    set_at(xmi, ymj, color)
                    set_at(xpi, ymj, color)
                oj = j
            ix += iy / rx
            iy -= ix / rx

            h = (ix + 16) >> 6
            i = (iy + 16) >> 6
        # } while (i > h);
    else:
        ix = 0
        iy = ry * 64
        # do {
        h = (ix + 32) >> 6
        i = (iy + 32) >> 6
        while i > h:
            j = (h * rx) / ry
            k = (i * rx) / ry

            if oi != i and oh != i or oh != h and oi != h and i != h:
                xmj = x - j
                xpj = x + j - 1
                if i > 0:
                    ypi = y + i - 1
                    ymi = y - i
                    if j > 0:
                        set_at(xmj, ypi, color)
                        set_at(xmj, ymi, color)
                    set_at(xpj, ypi, color)
                    set_at(xpj, ymi, color)
                oi = i
                xmk = x - k
                xpk = x + k - 1
                if h > 0:
                    yph = y + h - 1
                    ymh = y - h
                    set_at(xmk, yph, color)
                    set_at(xpk, yph, color)
                    set_at(xmk, ymh, color)
                    set_at(xpk, ymh, color)
                oh = h
            ix += iy / ry
            iy -= ix / ry

            h = (ix + 32) >> 6
            i = (iy + 32) >> 6
        # } while(i > h);


def draw_fillellipse(surface, x, y, rx, ry, color):
    # FIXME: this has a bug somewhere; there are two unfilled line down the horiz center
    # surf = gsdl2.Surface((128, 128), depth=depth)
    # rect = surf.get_rect()
    # x1 = 0
    # y1 = surf.get_height() // 2
    # y2 = surf.get_width()
    # gsdl2.draw.circle(surf, gsdl2.Color('red'), rect.center, rect.w // 2, width)
    if debug:
        print('gsdl.draw.draw_fillellipse')
# 	int ix, iy;
# 	int h, i, j, k;
# 	int oh, oi, oj, ok;

    set_at = surface.set_at

# 	if (rx==0 && ry==0) {  /* Special case - draw a single pixel */
# 		set_at( dst, x, y, color);
# 		return;
# 	}
    if rx == 0 and ry == 0:  # Special case - draw a single pixel
        set_at((x, y), color)
        return

# 	if (rx==0) { /* Special case for rx=0 - draw a vline */
# 		drawvertlineclip( dst, color, x, (Sint16)(y-ry), (Sint16)(y+ry) );
# 		return;
# 	}
    if rx == 0:  # Special case for rx=0 - draw a vline
        drawvertlineclip(surface, color, y - ry, y + ry)
        return

# 	if (ry==0) { /* Special case for ry=0 - draw a hline */
# 		drawhorzlineclip( dst, color, (Sint16)(x-rx), y, (Sint16)(x+rx) );
# 		return;
# 	}
    if ry == 0:  # Special case for ry=0 - draw a hline
        drawhorzlineclip(surface, color, x - rx, y, x + rx)
        return

# 	/* Init vars */
# 	oh = oi = oj = ok = 0xFFFF;
    # Init vars
    oh = oi = oj = ok = 0

# 	/* Draw */
# 	if (rx >= ry) {
# 		ix = 0;
# 		iy = rx * 64;
    # Draw
    if rx >= ry:
        ix = 0
        iy = rx * 64

# 		do {
# 			h = (ix + 8) >> 6;
# 			i = (iy + 8) >> 6;
# 			j = (h * ry) / rx;
# 			k = (i * ry) / rx;
        i_gt_h = True
        while i_gt_h:
            h = (ix + 8) >> 6
            i = (iy + 8) >> 6
            j = (h * ry) / rx
            k = (i * ry) / rx
# 			if ((ok!=k) && (oj!=k) && (k<ry)) {
# 				drawhorzlineclip(dst, color, x-h, y-k-1, x+h-1);
# 				drawhorzlineclip(dst, color, x-h, y+k, x+h-1);
# 				ok=k;
# 			}
            if ok != k and oj != k and k < ry:
                drawhorzlineclip(surface, color, x - h, y - k - 1, x + h - 1)
                drawhorzlineclip(surface, color, x - h, y + k, x + h - 1)
                ok = k
# 			if ((oj!=j) && (ok!=j) && (k!=j))  {
# 				drawhorzlineclip(dst, color, x-i, y+j, x+i-1);
# 				drawhorzlineclip(dst, color, x-i, y-j-1, x+i-1);
# 				oj=j;
# 			}
            if oj != j and ok != j and k != j:
                drawhorzlineclip(surface, color, x - i, y + j, x + i - 1)
                drawhorzlineclip(surface, color, x - i, y - j - 1, x + i - 1)
                oj = j
# 			ix = ix + iy / rx;
# 			iy = iy - ix / rx;
            ix += iy / rx
            iy -= ix / rx
#
# 		} while (i > h);
            i_gt_h = i > h

# 	} else {
    else:
# 		ix = 0;
# 		iy = ry * 64;
        ix = 0
        iy = ry * 64

# 		do {
# 			h = (ix + 8) >> 6;
# 			i = (iy + 8) >> 6;
# 			j = (h * rx) / ry;
# 			k = (i * rx) / ry;
        i_gt_h = True
        while i_gt_h:
            h = (ix + 8) >> 6
            i = (iy + 8) >> 6
            j = (h * rx) / ry
            k = (i * rx) / ry

# 			if ((oi!=i) && (oh!=i) && (i<ry)) {
# 				drawhorzlineclip(dst, color, x-j, y+i, x+j-1);
# 				drawhorzlineclip(dst, color, x-j, y-i-1, x+j-1);
# 				oi=i;
# 			}
            if oi != i and oh != i and i < ry:
                drawhorzlineclip(surface, color, x - j, y + i, x + j - 1)
                drawhorzlineclip(surface, color, x - j, y - i - 1, x + j - 1)
                oi = i

# 			if ((oh!=h) && (oi!=h) && (i!=h)) {
# 				drawhorzlineclip(dst, color, x-k, y+h, x+k-1);
# 				drawhorzlineclip(dst, color, x-k, y-h-1, x+k-1);
# 				oh=h;
# 			}
            if oh != h and oi != h and i != h:
                drawhorzlineclip(surface, color, x - k, y + h, x + k - 1)
                drawhorzlineclip(surface, color, x - k, y - h - 1, x + k - 1)
                oh = h

# 			ix = ix + iy / ry;
# 			iy = iy - ix / ry;
            ix += iy / ry
            iy -= ix / ry

# 		} while(i > h);
            i_gt_h = i > h


# static void draw_fillellipse(SDL_Surface *dst, int x, int y, int rx, int ry, Uint32 color)
# {
# 	int ix, iy;
# 	int h, i, j, k;
# 	int oh, oi, oj, ok;
#
# 	if (rx==0 && ry==0) {  /* Special case - draw a single pixel */
# 		set_at( dst, x, y, color);
# 		return;
# 	}
# 	if (rx==0) { /* Special case for rx=0 - draw a vline */
# 		drawvertlineclip( dst, color, x, (Sint16)(y-ry), (Sint16)(y+ry) );
# 		return;
# 	}
# 	if (ry==0) { /* Special case for ry=0 - draw a hline */
# 		drawhorzlineclip( dst, color, (Sint16)(x-rx), y, (Sint16)(x+rx) );
# 		return;
# 	}
#
# 	/* Init vars */
# 	oh = oi = oj = ok = 0xFFFF;
#
# 	/* Draw */
# 	if (rx >= ry) {
# 		ix = 0;
# 		iy = rx * 64;
#
# 		do {
# 			h = (ix + 8) >> 6;
# 			i = (iy + 8) >> 6;
# 			j = (h * ry) / rx;
# 			k = (i * ry) / rx;
# 			if ((ok!=k) && (oj!=k) && (k<ry)) {
# 				drawhorzlineclip(dst, color, x-h, y-k-1, x+h-1);
# 				drawhorzlineclip(dst, color, x-h, y+k, x+h-1);
# 				ok=k;
# 			}
# 			if ((oj!=j) && (ok!=j) && (k!=j))  {
# 				drawhorzlineclip(dst, color, x-i, y+j, x+i-1);
# 				drawhorzlineclip(dst, color, x-i, y-j-1, x+i-1);
# 				oj=j;
# 			}
# 			ix = ix + iy / rx;
# 			iy = iy - ix / rx;
#
# 		} while (i > h);
# 	} else {
# 		ix = 0;
# 		iy = ry * 64;
#
# 		do {
# 			h = (ix + 8) >> 6;
# 			i = (iy + 8) >> 6;
# 			j = (h * rx) / ry;
# 			k = (i * rx) / ry;
#
# 			if ((oi!=i) && (oh!=i) && (i<ry)) {
# 				drawhorzlineclip(dst, color, x-j, y+i, x+j-1);
# 				drawhorzlineclip(dst, color, x-j, y-i-1, x+j-1);
# 				oi=i;
# 			}
# 			if ((oh!=h) && (oi!=h) && (i!=h)) {
# 				drawhorzlineclip(dst, color, x-k, y+h, x+k-1);
# 				drawhorzlineclip(dst, color, x-k, y-h-1, x+k-1);
# 				oh=h;
# 			}
#
# 			ix = ix + iy / ry;
# 			iy = iy - ix / ry;
#
# 		} while(i > h);
# 	}
# }


def compare_int(a, b):
    return a - b


def draw_fillpoly(surface, vx, vy, n, color):
    if debug:
        print('gsdl.draw.draw_fillpoly')
# 	int i;
# 	int y;
# 	int miny, maxy;
# 	int x1, y1;
# 	int x2, y2;
# 	int ind1, ind2;
# 	int ints;
# 	int *polyints = PyMem_New(int, n);
# 	if (polyints == NULL) {
# 		PyErr_NoMemory();
# 		return;
# 	}
    polyints = [0] * n

# Determine Y maxima
# 	miny = vy[0];
# 	maxy = vy[0];
# 	for (i=1; (i < n); i++)
# 	{
# 		miny = MIN(miny, vy[i]);
# 		maxy = MAX(maxy, vy[i]);
# 	}
    miny = reduce(min, vy)
    maxy = reduce(max, vy)

# Draw, scanning y
# 	for(y=miny; (y <= maxy); y++) {
# 		ints = 0;
    for y in range(miny, maxy + 1):
        ints = 0
# 		for (i=0; (i < n); i++) {
        for i in range(n):
# 			if (!i) {
# 				ind1 = n-1;
# 				ind2 = 0;
# 			} else {
# 				ind1 = i-1;
# 				ind2 = i;
# 			}
            if not i:
                ind1 = n - 1
                ind2 = 0
            else:
                ind1 = i - 1
                ind2 = i
# 			y1 = vy[ind1];
# 			y2 = vy[ind2];
            y1 = vy[ind1]
            y2 = vy[ind2]
# 			if (y1 < y2) {
# 				x1 = vx[ind1];
# 				x2 = vx[ind2];
# 			} else if (y1 > y2) {
# 				y2 = vy[ind1];
# 				y1 = vy[ind2];
# 				x2 = vx[ind1];
# 				x1 = vx[ind2];
# 			} else {
# 				continue;
# 			}
            if y1 < y2:
                x1 = vx[ind1]
                x2 = vx[ind2]
            elif y1 > y2:
                y2 = vy[ind1]
                y1 = vy[ind2]
                x2 = vx[ind1]
                x1 = vx[ind2]
# 			if ((y >= y1) && (y < y2)) {
# 				polyints[ints++] = (y-y1) * (x2-x1) / (y2-y1) + x1;
# 			} else if ((y == maxy) && (y > y1) && (y <= y2)) {
# 				polyints[ints++] = (y-y1) * (x2-x1) / (y2-y1) + x1;
# 			}
            if y1 <= y < y2:
                polyints[ints] = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                ints += 1
            elif y == maxy and y1 < y <= y2:
                polyints[ints] = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                ints += 1
# 		}
# 		qsort(polyints, ints, sizeof(int), compare_int);
#
# 		for (i=0; (i<ints); i+=2) {
# 			drawhorzlineclip(dst, color, polyints[i], y, polyints[i+1]);
        for i in range(0, ints, 2):
            drawhorzlineclip(surface, color, polyints[i], y, polyints[i + 1])


# static void draw_fillpoly(SDL_Surface *dst, int *vx, int *vy, int n, Uint32 color)
# {
# 	int i;
# 	int y;
# 	int miny, maxy;
# 	int x1, y1;
# 	int x2, y2;
# 	int ind1, ind2;
# 	int ints;
# 	int *polyints = PyMem_New(int, n);
# 	if (polyints == NULL) {
# 		PyErr_NoMemory();
# 		return;
# 	}
#
#
# 	/* Determine Y maxima */
# 	miny = vy[0];
# 	maxy = vy[0];
# 	for (i=1; (i < n); i++)
# 	{
# 		miny = MIN(miny, vy[i]);
# 		maxy = MAX(maxy, vy[i]);
# 	}
#
# 	/* Draw, scanning y */
# 	for(y=miny; (y <= maxy); y++) {
# 		ints = 0;
# 		for (i=0; (i < n); i++) {
# 			if (!i) {
# 				ind1 = n-1;
# 				ind2 = 0;
# 			} else {
# 				ind1 = i-1;
# 				ind2 = i;
# 			}
# 			y1 = vy[ind1];
# 			y2 = vy[ind2];
# 			if (y1 < y2) {
# 				x1 = vx[ind1];
# 				x2 = vx[ind2];
# 			} else if (y1 > y2) {
# 				y2 = vy[ind1];
# 				y1 = vy[ind2];
# 				x2 = vx[ind1];
# 				x1 = vx[ind2];
# 			} else {
# 				continue;
# 			}
# 			if ((y >= y1) && (y < y2)) {
# 				polyints[ints++] = (y-y1) * (x2-x1) / (y2-y1) + x1;
# 			} else if ((y == maxy) && (y > y1) && (y <= y2)) {
# 				polyints[ints++] = (y-y1) * (x2-x1) / (y2-y1) + x1;
# 			}
# 		}
# 		qsort(polyints, ints, sizeof(int), compare_int);
#
# 		for (i=0; (i<ints); i+=2) {
# 			drawhorzlineclip(dst, color, polyints[i], y, polyints[i+1]);
# 		}
# 	}
# 	PyMem_Free(polyints);
# }