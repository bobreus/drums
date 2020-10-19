from __future__ import absolute_import

import sys
import pyglet
from pyglet import gl

import imgui
from imgui.integrations.pyglet import create_renderer

W = 440
H = 400
BPM = 120

kick = pyglet.media.load('samples/909/kick.wav', streaming=False)
clap = pyglet.media.load('samples/909/clap.wav', streaming=False)
oh = pyglet.media.load('samples/909/oh.wav', streaming=False)
hat = pyglet.media.load('samples/909/hat.wav', streaming=False)
snare = pyglet.media.load('samples/909/snare.wav', streaming=False)
rim = pyglet.media.load('samples/909/rim.wav', streaming=False)

state_kick = [False] * 16
state_clap = [False] * 16
state_oh = [False] * 16
state_hat = [False] * 16
state_snare = [False] * 16
state_rim = [False] * 16
beat = 0


def buttons(imgui, state, label):
    for i in range(0, 16):
        _, state[i] = imgui.checkbox(f"##{label}{i+1}", state[i])
        if i < 16 - 1:
            imgui.same_line()


def play(dt):
    global beat
    if state_hat[beat]:
        hat.play()
    if state_kick[beat]:
        kick.play()
    if state_clap[beat]:
        clap.play()
    if state_oh[beat]:
        oh.play()
    if state_snare[beat]:
        snare.play()
    if state_rim[beat]:
        rim.play()

    beat += 1
    if beat == 16:
        beat = 0


def main():
    window = pyglet.window.Window(width=W, height=H, resizable=False)
    gl.glClearColor(1, 1, 1, 1)
    imgui.create_context()
    impl = create_renderer(window)
    flags = imgui.WINDOW_NO_RESIZE
    flags |= imgui.WINDOW_NO_MOVE
    flags |= imgui.WINDOW_NO_TITLE_BAR

    def update(dt):
        global beat
        imgui.new_frame()

        imgui.begin("Drums", False, flags)
        imgui.set_window_size(W, H)
        imgui.set_window_position(0, 0)

        imgui.text(f"{BPM} BPM")
        imgui.progress_bar(beat/16, size=(424, 10))

        imgui.text_colored("Kick", 0.2, 1., 0.)
        buttons(imgui, state_kick, "kick")
        imgui.text_colored("Clap", 0.2, 1., 0.)
        buttons(imgui, state_clap, "clap")
        imgui.text_colored("Open Hat", 0.2, 1., 0.)
        buttons(imgui, state_oh, "oh")
        imgui.text_colored("Hat", 0.2, 1., 0.)
        buttons(imgui, state_hat, "hat")
        imgui.text_colored("Snare", 0.2, 1., 0.)
        buttons(imgui, state_snare, "snare")
        imgui.text_colored("Rim", 0.2, 1., 0.)
        buttons(imgui, state_rim, "rim")

        imgui.end()

    def draw(dt):
        update(dt)
        window.clear()
        imgui.render()
        impl.render(imgui.get_draw_data())

    pyglet.clock.schedule_interval(draw, 1/120)
    pyglet.clock.schedule_interval(play, 60/BPM/4)
    pyglet.app.run()
    impl.shutdown()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        BPM = int(args[0])
    main()
