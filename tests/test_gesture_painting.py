import pytest
import numpy as np
from gesture_painting import GesturePainting

def test_initial_state():
    gp = GesturePainting()
    assert gp.canvas_width == 600
    assert gp.canvas_height == 471
    assert gp.current_color_index == 0
    assert np.array_equal(gp.paint_canvas[67:, :, :], np.ones((404, 600, 3), dtype=np.uint8) * 255)

def test_color_selection():
    gp = GesturePainting()
    gp.select_color(200, 30)
    assert gp.current_color_index == 0

    gp.select_color(300, 30)
    assert gp.current_color_index == 1

    gp.select_color(400, 30)
    assert gp.current_color_index == 2

    gp.select_color(550, 30)
    assert gp.current_color_index == 3

def test_clear_canvas():
    gp = GesturePainting()
    gp.clear_canvas()
    assert len(gp.white_points) == 1
    assert len(gp.green_points) == 1
    assert len(gp.red_points) == 1
    assert len(gp.black_points) == 1
    assert gp.white_idx == 0
    assert gp.green_idx == 0
    assert gp.red_idx == 0
    assert gp.black_idx == 0
    assert np.array_equal(gp.paint_canvas[67:, :, :], np.ones((404, 600, 3), dtype=np.uint8) * 255)
