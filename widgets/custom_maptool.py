# -*- coding: utf-8 -*-
# @Author  : llc
# @Time    : 2020/6/7 15:30
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsRectangle, QgsPointXY, QgsWkbTypes
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsVertexMarker


class PointMapTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        super(PointMapTool, self).__init__(canvas)
        self.canvas = canvas
        self.marker = QgsVertexMarker(canvas)
        self.marker.setColor(QColor(0, 0, 255))
        self.marker.setPenWidth(3)

    def canvasPressEvent(self, e):
        self.point = self.toMapCoordinates(e.pos())
        self.marker.setCenter(self.point)

    def deactivate(self):
        super(PointMapTool, self).deactivate()
        self.deactivated.emit()
        self.canvas.scene().removeItem(self.marker)


class LineMapTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        super(LineMapTool, self).__init__(canvas)
        self.canvas = canvas
        self.rubberBand = QgsRubberBand(self.canvas, True)
        self.rubberBand.setColor(QColor(255, 0, 0, 100))
        self.rubberBand.setWidth(3)
        self.reset()

    def reset(self):
        self.points = []
        self.isEmittingPoint = False
        self.rubberBand.reset(True)

    def canvasPressEvent(self, e):
        self.points.append(e.mapPoint())
        self.isEmittingPoint = True

    def canvasReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            # 右键结束
            self.isEmittingPoint = False

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        self.cursor_point = e.mapPoint()
        self.showLine()

    def showLine(self):
        self.rubberBand.reset(QgsWkbTypes.LineGeometry)
        if not self.points:
            return

        for point in self.points:
            self.rubberBand.addPoint(point, False)

        self.rubberBand.addPoint(self.cursor_point)
        self.rubberBand.show()

    def deactivate(self):
        super(LineMapTool, self).deactivate()
        self.deactivated.emit()
        self.reset()


class RectangleMapTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        super(RectangleMapTool, self).__init__(canvas)
        self.canvas = canvas
        self.rubberBand = QgsRubberBand(self.canvas, True)
        self.rubberBand.setColor(QColor(255, 0, 0, 100))
        self.rubberBand.setWidth(1)
        self.reset()

    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(True)

    def canvasPressEvent(self, e):
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showRect(self.startPoint, self.endPoint)

    def canvasReleaseEvent(self, e):
        self.isEmittingPoint = False
        r = self.rectangle()
        if r is not None:
            print("Rectangle:", r.xMinimum(), r.yMinimum(), r.xMaximum(), r.yMaximum())

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return

        self.endPoint = self.toMapCoordinates(e.pos())
        self.showRect(self.startPoint, self.endPoint)

    def showRect(self, startPoint, endPoint):
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return

        point1 = QgsPointXY(startPoint.x(), startPoint.y())
        point2 = QgsPointXY(startPoint.x(), endPoint.y())
        point3 = QgsPointXY(endPoint.x(), endPoint.y())
        point4 = QgsPointXY(endPoint.x(), startPoint.y())

        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)  # true to update canvas
        self.rubberBand.show()

    def rectangle(self):
        if self.startPoint is None or self.endPoint is None:
            return None
        elif self.startPoint.x() == self.endPoint.x() or self.startPoint.y() == self.endPoint.y():
            return None

        return QgsRectangle(self.startPoint, self.endPoint)

    def deactivate(self):
        super(RectangleMapTool, self).deactivate()
        self.deactivated.emit()
        self.reset()


class PolygonMapTool(QgsMapToolEmitPoint):
    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        self.rubberBand.setColor(QColor(255, 0, 0, 100))
        self.rubberBand.setWidth(1)
        self.reset()

    def reset(self):
        self.is_start = False  # 开始绘图
        self.is_vertical = False  # 垂直画线
        self.cursor_point = None
        self.points = []
        self.rubberBand.reset(True)

    def canvasPressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.points.append(self.cursor_point)
            self.is_start = True
        elif event.button() == Qt.RightButton:
            # 右键结束绘制
            if self.is_start:
                self.is_start = False
                self.cursor_point = None
                self.show_polygon()
                self.points = []
            else:
                pass
        else:
            pass

    def canvasMoveEvent(self, event):
        self.cursor_point = event.mapPoint()
        if not self.is_start:
            return
        self.show_polygon()

    def show_polygon(self):
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)  # 防止拖影
        first_point = self.points[0]
        last_point = self.points[-1]
        self.rubberBand.addPoint(first_point, False)
        for point in self.points[1:-1]:
            self.rubberBand.addPoint(point, False)
        if self.cursor_point:
            self.rubberBand.addPoint(QgsPointXY(last_point.x(), last_point.y()), False)
        else:
            self.rubberBand.addPoint(QgsPointXY(last_point.x(), last_point.y()), True)
            self.rubberBand.show()
            return

        self.rubberBand.addPoint(self.cursor_point, True)
        self.rubberBand.show()

    def deactivate(self):
        super(PolygonMapTool, self).deactivate()
        self.deactivated.emit()
        self.reset()
