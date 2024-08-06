# app/widgets/fade_widget.py
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty, QEasingCurve

class FadeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(FadeWidget, self).__init__(*args, **kwargs)
        self._opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._opacity_effect)
        self._opacity = 1.0

    def fade_in(self, duration=500):
        self._start_fade(1.0, duration)

    def fade_out(self, duration=500):
        self._start_fade(0.0, duration)

    def _start_fade(self, end_opacity, duration):
        animation = QPropertyAnimation(self._opacity_effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(self._opacity)
        animation.setEndValue(end_opacity)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.finished.connect(self._on_fade_finished)
        animation.start()

    def _on_fade_finished(self):
        if self._opacity == 0.0:
            self.hide()
        elif self._opacity == 1.0:
            self.show()

    @pyqtProperty(float)
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self._opacity_effect.setOpacity(value)
