#!/usr/bin/env python3
"""
Генератор иконок для PWA приложения Cinema Paradise
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Создает иконку заданного размера"""
    # Создаем изображение с градиентом
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Рисуем круглый фон с градиентом
    for i in range(size//2):
        alpha = int(255 * (1 - i / (size//2)))
        color = (102, 126, 234, alpha)  # #667eea с прозрачностью
        draw.ellipse([i, i, size-i, size-i], fill=color)
    
    # Добавляем эмодзи кинотеатра
    try:
        # Пытаемся загрузить системный шрифт
        font_size = size // 3
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        # Используем стандартный шрифт
        font = ImageFont.load_default()
    
    # Добавляем текст "🎬"
    text = "🎬"
    # Центрируем текст
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    # Сохраняем файл
    img.save(filename, 'PNG')
    print(f"✅ Создана иконка: {filename} ({size}x{size})")

def main():
    """Создает все необходимые иконки"""
    print("🎨 Генерация иконок для PWA Cinema Paradise...")
    
    # Размеры иконок для PWA
    sizes = [72, 96, 128, 144, 152, 180, 192, 384, 512]
    
    for size in sizes:
        filename = f"icon-{size}.png"
        create_icon(size, filename)
    
    print(f"\n🎉 Создано {len(sizes)} иконок!")
    print("📱 Иконки готовы для PWA приложения")

if __name__ == "__main__":
    main() 