"""Модуль, содержащий общие вещи для всех "пауков"."""
import re

#: регулярное выражение, которое отфильтровывает всё, кроме цифр
only_numbers = re.compile(r'\D')
