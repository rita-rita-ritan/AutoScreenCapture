import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ret_regions = []
used_display = 0

class RegionWindow(Gtk.ApplicationWindow):
  is_first_select = True
  rectangle_start = (0,0)
  rectangle_end= (0,0)
  monitor_geo = (0,0)

  def __init__(self, app):
    # instantiate
    self.box = Gtk.Box()
    self.d = Gtk.DrawingArea()
    self.box.pack_start(self.d, True, True, 0)
    self.d.set_can_focus(True)
    self.box.set_can_focus(True)

    # decoration
    Gtk.ApplicationWindow.__init__(self, application = app)
    self.set_border_width(0)
    self.set_app_paintable(True)
    self.set_decorated(False)
    self.set_property("skip-taskbar-hint", True)
    self.connect("draw", self.draw)


    # register cbs
    self.connect("button-press-event", self.mouse_press)
    self.connect("button-release-event", self.mouse_release)
    self.connect("motion-notify-event", self.motion_notify)
    self.connect("key-press-event", self.key_press)

    # size/color
    screen = self.get_screen()
    monitor = screen.get_monitor_geometry(used_display)
    visual = screen.get_rgba_visual()
    if visual and screen.is_composited():
      self.set_visual(visual)

    geo_x = monitor.x
    geo_y = monitor.y
    width = screen.width()
    height = screen.height()
    self.d.set_size_request(width, height)
    self.monitor_geo = (geo_x, geo_y)
    self.move(geo_x, geo_y)
    self.fullscreen()

    # show
    self.add(self.box)
    self.show_all()

    self.set_keep_above(True)
    self.grab_focus()

  def return_area(self):
    global ret_regions
    ret_regions = [
      (self.rectangle_start[0] + self.monitor_geo[0], self.rectangle_start[1] + self.monitor_geo[1]),
      (self.rectangle_end[0] + self.monitor_geo[0], self.rectangle_end[1] + self.monitor_geo[1])
      ]
    self.close()

  def key_press(self, widget, context):
    (_, key) = context.get_keycode()
    if key == 36:
      self.return_area()

  def motion_notify(self, widget, context):
    if self.is_first_select:      # dirty workaround for MacOS
      self.is_first_select = False
      self.rectangle_start = (context.x, context.y)
    self.rectangle_end = (context.x, context.y)
    if self.rectangle_start == self.rectangle_end:
      return
    widget.queue_draw()

  def mouse_press(self, widget, context):
    self.rectangle_start = (context.x, context.y)
    self.rectangle_end = (context.x+1, context.y+1)
    widget.queue_draw()

  def mouse_release(self, widget, context):
    self.rectangle_end = (context.x, context.y)
    widget.queue_draw()

  def draw(self, widget, context):
    context.set_source_rgba(0, 0, 0, 0.5)
    context.set_operator(cairo.OPERATOR_SOURCE)
    context.paint()
    context.set_operator(cairo.OPERATOR_OVER)

    context.set_line_width(1)
    context.set_source_rgb(1.0, 1.0, 1.0)
    context.rectangle(self.rectangle_start[0], self.rectangle_start[1], self.rectangle_end[0] - self.rectangle_start[0], self.rectangle_end[1] - self.rectangle_start[1])
    context.stroke()


class RegionSelector(Gtk.Application):
  def __init__(self):
    Gtk.Application.__init__(self, application_id = "github.com.rita-rita-ritan.AutoScreenCapture")

  def do_activate(self):
    RegionWindow(self)

def get_region(monitor):
  global used_display
  used_display = monitor
  app = RegionSelector()
  app.run()
  return ret_regions
