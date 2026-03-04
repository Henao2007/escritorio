"""Compatibilidad para estilos.

Este módulo reexporta todo desde ``assets.styles`` para que las vistas que
usan ``from views.styles import ...`` sigan funcionando sin cambios.
"""

from assets.styles import *  # noqa: F401,F403

